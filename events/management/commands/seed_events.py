"""
Load sample colleges and events so the site has content on first run.
Run: python manage.py seed_events
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from events.models import College, Event


class Command(BaseCommand):
    help = 'Create sample colleges and upcoming events for demo.'

    def handle(self, *args, **options):
        if College.objects.exists():
            self.stdout.write(self.style.WARNING('Colleges already exist. Skipping seed.'))
            return

        self.stdout.write('Creating sample colleges and events...')

        c1 = College.objects.create(
            name='Tech Institute of Engineering',
            location='Mumbai, Maharashtra'
        )
        c2 = College.objects.create(
            name='Arts & Science College',
            location='Pune, Maharashtra'
        )
        c3 = College.objects.create(
            name='National College of Innovation',
            location='Nashik, Maharashtra'
        )

        base_date = timezone.now().date() + timedelta(days=3)
        events_data = [
            ('TechFest 2025', 'Technical', 'Annual technical festival with hackathons, coding contests, and workshops.', c1, 0, 150),
            ('Code Sprint Hackathon', 'Technical', '24-hour hackathon. Build something cool and win prizes!', c1, 100, 50),
            ('Cultural Night', 'Cultural', 'An evening of music, dance, and performances by students.', c2, 50, 200),
            ('Photography Workshop', 'Workshop', 'Learn basics of photography and editing. Bring your camera or phone.', c2, 0, 30),
            ('Inter-College Cricket', 'Sports', 'Cricket tournament. Register your team or join as individual.', c3, 0, 100),
            ('AI & ML Workshop', 'Technical', 'Hands-on workshop on machine learning with Python.', c3, 200, 40),
        ]

        for i, (title, category, desc, college, fee, max_p) in enumerate(events_data):
            event_date = base_date + timedelta(days=i)
            Event.objects.create(
                title=title,
                category=category,
                description=desc,
                date=event_date,
                time=timezone.now().time().replace(hour=10, minute=0, second=0),
                venue=f'{college.name} Main Hall',
                entry_fee=fee,
                max_participants=max_p,
                college=college,
            )

        self.stdout.write(self.style.SUCCESS(
            f'Created 3 colleges and {len(events_data)} events. Visit the homepage to see them!'
        ))
