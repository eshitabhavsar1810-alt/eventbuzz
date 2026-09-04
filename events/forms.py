"""
EventBuzz forms with validation.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Registration, Review, Event


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters.')
        return username


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ('full_name', 'date_of_birth', 'email', 'contact_number', 'college_name')
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Your contact number'}),
            'college_name': forms.TextInput(attrs={'placeholder': 'Your college name'}),
        }

    def clean_full_name(self):
        val = self.cleaned_data.get('full_name', '').strip()
        if not val or len(val) < 2:
            raise forms.ValidationError('Enter your full name.')
        return val

    def clean_contact_number(self):
        val = self.cleaned_data.get('contact_number', '').strip()
        if not val or len(val) < 10:
            raise forms.ValidationError('Enter a valid contact number (at least 10 digits).')
        if not val.replace(' ', '').replace('-', '').replace('+', '').isdigit():
            raise forms.ValidationError('Contact number should contain only digits and + - spaces.')
        return val

    def clean_college_name(self):
        val = self.cleaned_data.get('college_name', '').strip()
        if not val or len(val) < 2:
            raise forms.ValidationError('Enter your college name.')
        return val


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'feedback')
        widgets = {
            'rating': forms.HiddenInput(),
            'feedback': forms.Textarea(attrs={'placeholder': 'Share your experience...', 'rows': 4}),
        }

    def clean_rating(self):
        r = self.cleaned_data.get('rating')
        if r is None or r < 1 or r > 5:
            raise forms.ValidationError('Please select a rating from 1 to 5.')
        return r


class AdminSignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('full_name', 'username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name', '').strip()
        if full_name:
            parts = full_name.split()
            user.first_name = parts[0]
            user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        user.email = self.cleaned_data.get('email')
        user.is_staff = True
        if commit:
            user.save()
        return user


class AdminLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_staff:
            raise forms.ValidationError('This account is not allowed to access the admin dashboard.', code='inactive')


class AdminEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'title',
            'category',
            'date',
            'time',
            'max_participants',
            'college',
            'description',
            'venue',
        )

    def clean(self):
        cleaned_data = super().clean()
        # Prevent changing event name once registrations exist
        if self.instance.pk and self.instance.registrations.exists():
            try:
                original = Event.objects.get(pk=self.instance.pk)
            except Event.DoesNotExist:
                original = None
            if original and cleaned_data.get('title') != original.title:
                self.add_error('title', 'You cannot change the event name after users have registered.')

        reg_deadline = cleaned_data.get('registration_deadline')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        if reg_deadline and date and time:
            event_dt = timezone.make_aware(
                timezone.datetime.combine(date, time),
                timezone.get_current_timezone()
            )
            if reg_deadline > event_dt:
                self.add_error('registration_deadline', 'Registration deadline must be before the event date and time.')

        return cleaned_data
