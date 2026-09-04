"""
EventBuzz models: College, Event, Registration, Review.
Includes date-status logic (coming_soon, expire_soon, expired).
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class College(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='colleges/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


CATEGORY_CHOICES = [
    ('Technical', 'Technical'),
    ('Cultural', 'Cultural'),
    ('Workshop', 'Workshop'),
    ('Sports', 'Sports'),
]


EVENT_STATUS_CHOICES = [
    ('upcoming', 'Upcoming'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    branch = models.CharField(max_length=255, blank=True)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    max_participants = models.PositiveIntegerField(default=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='events')
    registration_deadline = models.DateTimeField(blank=True, null=True)
    payment_required = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES, default='upcoming')
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.title

    @property
    def seats_left(self):
        return max(0, self.max_participants - self.registrations.count())

    @property
    def is_full(self):
        return self.registrations.count() >= self.max_participants

    @property
    def is_expired(self):
        """Event is past (date + time)."""
        event_dt = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time),
            timezone.get_current_timezone()
        )
        return timezone.now() > event_dt

    @property
    def date_status(self):
        """
        Returns: 'expired' | 'expire_soon' | 'register_before_time' | 'coming_soon'
        """
        if self.is_expired:
            return 'expired'
        event_dt = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time),
            timezone.get_current_timezone()
        )
        now = timezone.now()
        delta = event_dt - now
        if delta <= timedelta(hours=24):
            return 'expire_soon'  # Less than 24 hours
        if delta <= timedelta(days=3):
            return 'register_before_time'  # Within 3 days
        return 'coming_soon'

    def average_rating(self):
        from django.db.models import Avg
        r = self.reviews.aggregate(Avg('rating'))
        return round(r['rating__avg'] or 0, 1)


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True)
    contact_number = models.CharField(max_length=20)
    college_name = models.CharField(max_length=200)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'event']
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_reviews')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'event']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.rating} stars)"
