from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter('dummy')
def dummy(element: BoundField) -> BoundField:
    """Dummy filter for debugging.

    Usage: put a breakpoint inside this filter and use it in a template
    by doing:
        {% load dummy_filter %}
        {% form.field | dummy %}
    """
    return element
