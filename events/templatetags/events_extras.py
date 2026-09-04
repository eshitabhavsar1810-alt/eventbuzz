from django import template
register = template.Library()

STATUS_LABELS = {
    'coming_soon': 'Coming soon',
    'expire_soon': 'Expire soon',
    'register_before_time': 'Ongoing event',
    'expired': 'Expired',
}


@register.filter
def date_status_label(status):
    return STATUS_LABELS.get(status, status)
