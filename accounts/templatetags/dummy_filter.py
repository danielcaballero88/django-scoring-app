from django import template
from django.forms.boundfield import BoundField

register = template.Library()


@register.filter("dummy")
def dummy(element: BoundField) -> BoundField:
    """Dummy filter for debugging.

    Usage: put a breakpoint inside this filter and use it in a template
    by doing:
        {% load dummy_filter %}
        {% form.field | dummy %}
    """
    element.field.widget.attrs["class"] = "asd"
    return element


@register.filter("add_class")
def add_class(element: BoundField, new_classes: str) -> BoundField:
    current_classes = element.field.widget.attrs.get("class", "").split()
    classes = current_classes + new_classes.split()
    element.field.widget.attrs["class"] = " ".join(classes)
    return element


@register.filter("add_placeholder")
def add_placeholder(element: BoundField) -> BoundField:
    element.field.widget.attrs["placeholder"] = element.field.label
    return element
