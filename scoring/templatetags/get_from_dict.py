from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter('get_from_dict')
def get_from_dict(value, arg) -> BoundField:
    """Filter to get a value from a dictionary

    Usage:
        {% load get_from_dict %}
        {% some_dict|get_from_dict:key %}
    """
    try:
        result = value[arg]
    except:
        result = 0
    return result
