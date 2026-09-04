"""
Django Admin for EventBuzz with registration count, filters, and past-date validation.
"""
from django.contrib import admin
from django.utils import timezone
from django import forms
from .models import College, Event, Registration, Review


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise forms.ValidationError('Event date cannot be in the past.')
        return date

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get('date')
        time = cleaned.get('time')
        if date and time:
            from datetime import datetime
            event_dt = timezone.make_aware(
                timezone.datetime.combine(date, time),
                timezone.get_current_timezone()
            )
            if event_dt < timezone.now():
                raise forms.ValidationError('Event date and time cannot be in the past.')
        return cleaned


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('title', 'college', 'category', 'date', 'time', 'venue', 'registration_count', 'max_participants')
    list_filter = ('college', 'category', 'date')
    search_fields = ('title', 'description', 'venue')
    date_hierarchy = 'date'

    def registration_count(self, obj):
        return obj.registrations.count()
    registration_count.short_description = 'Registrations'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'contact_number', 'college_name', 'registered_at')
    list_filter = ('event__college', 'event__category')
    search_fields = ('user__username', 'event__title', 'college_name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'rating', 'feedback_preview', 'created_at')
    list_filter = ('rating', 'event__college')

    def feedback_preview(self, obj):
        return (obj.feedback[:50] + '...') if obj.feedback and len(obj.feedback) > 50 else (obj.feedback or '-')
    feedback_preview.short_description = 'Feedback'
