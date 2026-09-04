"""
EventBuzz views: auth, home, event detail, registration, review.
Excludes expired events from listings; sends email on registration.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.views import redirect_to_login
from functools import wraps
import csv
from .models import College, Event, Registration, Review
from .forms import (
    RegisterForm,
    LoginForm,
    RegistrationForm,
    ReviewForm,
    AdminSignupForm,
    AdminLoginForm,
    AdminEventForm,
)


def _event_datetime(event):
    return timezone.make_aware(
        timezone.datetime.combine(event.date, event.time),
        timezone.get_current_timezone()
    )


def _get_upcoming_events(queryset=None):
    """Return events that are not yet expired (by date+time)."""
    if queryset is None:
        queryset = Event.objects.select_related('college').prefetch_related('registrations', 'reviews')
    result = []
    for e in queryset:
        if not e.is_expired:
            result.append(e)
    return result


def _is_safe_next_url(next_url: str | None) -> bool:
   return bool(next_url) and next_url.startswith('/')


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url=reverse('events:admin_login'))
        if not request.user.is_staff:
            messages.error(request, 'You are not authorized to access the admin dashboard.')
            return redirect('events:home')
        return view_func(request, *args, **kwargs)

    return _wrapped


def _email_recipients_for_new_event():
    return list(
        User.objects.filter(is_staff=False)
        .exclude(email='')
        .values_list('email', flat=True)
        .distinct()
    )


def _email_recipients_for_event_update(event: Event):
    return list(
        event.registrations.select_related('user')
        .exclude(user__email='')
        .values_list('user__email', flat=True)
        .distinct()
    )


def _send_email(subject: str, message: str, recipient_list: list[str]):
    if not recipient_list:
        return
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=True,
        )
    except Exception:
        pass


def register_user(request):
    if request.user.is_authenticated:
        return redirect('events:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('events:home')
        else:
            for field, errors in form.errors.items():
                for err in errors:
                    messages.error(request, err)
    else:
        form = RegisterForm()
    return render(request, 'events/auth.html', {'form': form, 'is_login': False})


def login_user(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('events:admin_dashboard')
        return redirect('events:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # If this is an admin/staff user, send them to the admin dashboard
            if user.is_staff:
                next_url = request.GET.get('next')
                if _is_safe_next_url(next_url):
                    return redirect(next_url)
                return redirect('events:admin_dashboard')
            # Normal student user flow (unchanged)
            next_url = request.GET.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('events:home')
        # form.errors / form.non_field_errors shown in template
    else:
        form = LoginForm()
    return render(request, 'events/auth.html', {'form': form, 'is_login': True})


def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('events:home')


def admin_signup(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('events:admin_dashboard')
        return redirect('events:home')

    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin account created successfully. Please login.')
            return redirect('events:admin_login')
        for errors in form.errors.values():
            for err in errors:
                messages.error(request, err)
    else:
        form = AdminSignupForm()

    return render(request, 'events/admin/auth.html', {'form': form, 'is_login': False})


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('events:admin_dashboard')
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('events:home')

    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            next_url = request.GET.get('next')
            if _is_safe_next_url(next_url):
                return redirect(next_url)
            return redirect('events:admin_dashboard')
    else:
        form = AdminLoginForm()

    return render(request, 'events/admin/auth.html', {'form': form, 'is_login': True})


def admin_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('events:admin_login')


@staff_required
def admin_dashboard(request):
    qs = Event.objects.select_related('college').prefetch_related('registrations').order_by('-created_at')
    status = request.GET.get('status', '').strip()
    q = request.GET.get('q', '').strip()

    if status:
        qs = qs.filter(status=status)
    if q:
        qs = qs.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(venue__icontains=q)
            | Q(college__name__icontains=q)
        )

    return render(request, 'events/admin/dashboard.html', {
        'events': qs[:200],
        'status': status,
        'q': q,
    })


@staff_required
def admin_event_create(request):
    if request.method == 'POST':
        form = AdminEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            recipients = _email_recipients_for_new_event()
            _send_email(
                subject=f'EventBuzz: New event announced - {event.title}',
                message=(
                    f'A new event has been added on EventBuzz:\n\n'
                    f'Event: {event.title}\n'
                    f'Category: {event.category}\n'
                    f'Date: {event.date}\n'
                    f'Time: {event.time}\n'
                    f'Venue: {event.venue}\n'
                    f'\nVisit EventBuzz to register.'
                ),
                recipient_list=recipients,
            )
            messages.success(request, 'Event created successfully.')
            return redirect('events:admin_dashboard')
        for errors in form.errors.values():
            for err in errors:
                messages.error(request, err)
    else:
        form = AdminEventForm()

    return render(request, 'events/admin/event_form.html', {'form': form, 'mode': 'create'})


@staff_required
def admin_event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = AdminEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            updated = form.save()
            recipients = _email_recipients_for_event_update(updated)
            _send_email(
                subject=f'EventBuzz: Event updated - {updated.title}',
                message=(
                    f'Event details were updated:\n\n'
                    f'Event: {updated.title}\n'
                    f'Date: {updated.date}\n'
                    f'Time: {updated.time}\n'
                    f'Venue: {updated.venue}\n'
                    f'Status: {updated.status}\n'
                    f'\nPlease check EventBuzz for the latest details.'
                ),
                recipient_list=recipients,
            )
            messages.success(request, 'Event updated successfully.')
            return redirect('events:admin_dashboard')
        for errors in form.errors.values():
            for err in errors:
                messages.error(request, err)
    else:
        form = AdminEventForm(instance=event)

    return render(request, 'events/admin/event_form.html', {'form': form, 'mode': 'update', 'event': event})


@staff_required
def admin_event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Event "{title}" deleted.')
        return redirect('events:admin_dashboard')
    return render(request, 'events/admin/event_delete.html', {'event': event})


@staff_required
def admin_registrations(request):
    regs = Registration.objects.select_related('user', 'event', 'event__college').order_by('-registered_at')
    events = Event.objects.all().order_by('date', 'time')

    event_id = request.GET.get('event', '').strip()
    q = request.GET.get('q', '').strip()
    if event_id.isdigit():
        regs = regs.filter(event_id=int(event_id))
    if q:
        regs = regs.filter(
            Q(user__username__icontains=q)
            | Q(user__email__icontains=q)
            | Q(user__first_name__icontains=q)
            | Q(user__last_name__icontains=q)
        )

    return render(request, 'events/admin/registrations.html', {
        'registrations': regs[:500],
        'events': events,
        'event_id': event_id,
        'q': q,
    })


@staff_required
def admin_registrations_export(request):
    regs = Registration.objects.select_related('user', 'event', 'event__college').order_by('-registered_at')
    event_id = request.GET.get('event', '').strip()
    q = request.GET.get('q', '').strip()
    if event_id.isdigit():
        regs = regs.filter(event_id=int(event_id))
    if q:
        regs = regs.filter(
            Q(user__username__icontains=q)
            | Q(user__email__icontains=q)
            | Q(user__first_name__icontains=q)
            | Q(user__last_name__icontains=q)
        )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrations.csv"'
    writer = csv.writer(response)
    writer.writerow(['Event', 'Username', 'Full Name', 'Email', 'Contact Number', 'College Name', 'Registered At'])

    for r in regs:
        full_name = f"{r.user.first_name} {r.user.last_name}".strip()
        writer.writerow([
            r.event.title,
            r.user.username,
            full_name,
            r.user.email,
            r.contact_number,
            r.college_name,
            r.registered_at.isoformat(sep=' ', timespec='seconds'),
        ])

    return response


def home(request):
    colleges = College.objects.all()
    all_events = Event.objects.select_related('college').prefetch_related('registrations', 'reviews')
    events = _get_upcoming_events(all_events)
    return render(request, 'events/home.html', {
        'colleges': colleges,
        'events': events,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event.objects.select_related('college').prefetch_related('registrations', 'reviews'), pk=pk)
    user_registered = False
    user_review = None
    if request.user.is_authenticated:
        user_registered = Registration.objects.filter(user=request.user, event=event).exists()
        user_review = Review.objects.filter(user=request.user, event=event).first()
    reviews = event.reviews.select_related('user').order_by('-created_at')[:20]
    avg_rating = event.average_rating()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'user_registered': user_registered,
        'user_review': user_review,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.is_expired:
        messages.error(request, 'This event has already ended.')
        return redirect('events:event_detail', pk=pk)
    if event.is_full:
        messages.error(request, 'This event is full.')
        return redirect('events:event_detail', pk=pk)
    if Registration.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, 'You are already registered for this event.')
        return redirect('events:event_detail', pk=pk)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.user = request.user
            reg.event = event
            reg.save()
            try:
                send_mail(
                    subject=f'EventBuzz: Registration confirmed - {event.title}',
                    message=(
                        f'Hi {request.user.username},\n\n'
                        f'You have successfully registered for:\n'
                        f'Event: {event.title}\n'
                        f'Date: {event.date}\n'
                        f'Time: {event.time}\n'
                        f'Venue: {event.venue}\n\n'
                        f'Thank you for using EventBuzz!'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, 'Registration successful! Check your email for confirmation.')
            return redirect('events:event_review', pk=pk)
        for errors in form.errors.values():
            for err in errors:
                messages.error(request, err)
    else:
        form = RegistrationForm(initial={
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'college_name': request.user.username,
        })
    return render(request, 'events/register.html', {'event': event, 'form': form})


@login_required
def event_review(request, pk):
    event = get_object_or_404(Event.objects.prefetch_related('reviews__user'), pk=pk)
    user_review = Review.objects.filter(user=request.user, event=event).first()
    reviews = event.reviews.select_related('user').order_by('-created_at')
    avg_rating = event.average_rating()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.user = request.user
            rev.event = event
            rev.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('events:event_review', pk=pk)
        for errors in form.errors.values():
            for err in errors:
                messages.error(request, err)
    else:
        form = ReviewForm(instance=user_review)

    return render(request, 'events/review.html', {
        'event': event,
        'form': form,
        'user_review': user_review,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })


@login_required
def my_events(request):
    """Events the user has registered for; links to write review."""
    regs = Registration.objects.filter(user=request.user).select_related('event', 'event__college').order_by('-registered_at')
    return render(request, 'events/my_events.html', {'registrations': regs})


def about(request):
    return render(request, 'events/about.html')


def contact(request):
    return render(request, 'events/contact.html')

def colleges_page(request):
    """Separate page for colleges listing."""
    colleges = College.objects.all()
    return render(request, 'events/colleges.html', {
        'colleges': colleges,
    })

def events_page(request):
    """Separate page for events listing."""
    colleges = College.objects.all()

    # Optional filter: show events only for a specific college if ?college=<id> is provided
    selected_college_id = request.GET.get('college', '').strip()
    selected_college = None

    all_events = Event.objects.select_related('college').prefetch_related('registrations', 'reviews')
    if selected_college_id.isdigit():
        college_pk = int(selected_college_id)
        all_events = all_events.filter(college_id=college_pk)
        selected_college = College.objects.filter(pk=college_pk).first()

    events = _get_upcoming_events(all_events)
    # Get featured events for slider (first 4 upcoming events)
    featured_events = events[:4] if len(events) >= 4 else events
    return render(request, 'events/events.html', {
        'colleges': colleges,
        'events': events,
        'featured_events': featured_events,
        'selected_college_id': selected_college_id,
        'selected_college': selected_college,
    })
