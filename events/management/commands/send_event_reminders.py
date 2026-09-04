from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from events.models import Event


class Command(BaseCommand):
    help = "Send email reminders to users registered for events happening soon."

    def add_arguments(self, parser):
        parser.add_argument(
            "--hours",
            type=int,
            default=24,
            help="Send reminders for events starting within N hours (default: 24).",
        )

    def handle(self, *args, **options):
        hours = options["hours"]
        now = timezone.now()
        window_end = now + timezone.timedelta(hours=hours)

        events = Event.objects.exclude(status="cancelled").all()
        count_emails = 0

        for event in events:
            event_dt = timezone.make_aware(
                timezone.datetime.combine(event.date, event.time),
                timezone.get_current_timezone(),
            )
            if event_dt < now or event_dt > window_end:
                continue

            recipient_list = list(
                event.registrations.select_related("user")
                .exclude(user__email="")
                .values_list("user__email", flat=True)
                .distinct()
            )
            if not recipient_list:
                continue

            try:
                send_mail(
                    subject=f"EventBuzz reminder: {event.title} is coming up",
                    message=(
                        f"Reminder for your upcoming event:\n\n"
                        f"Event: {event.title}\n"
                        f"Date: {event.date}\n"
                        f"Time: {event.time}\n"
                        f"Venue: {event.venue}\n\n"
                        f"See you there!"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipient_list,
                    fail_silently=True,
                )
                count_emails += len(recipient_list)
            except Exception:
                continue

        self.stdout.write(self.style.SUCCESS(f"Reminders processed. Emails queued/sent: {count_emails}"))
