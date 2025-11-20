from pathlib import Path
from django import template

register = template.Library()


@register.filter
def filename_filter(value):
    """
    Return only the base filename from a FileField/ImageField value.
    """
    if not value:
        return ""

    path_str = getattr(value, "name", value)

    return Path(path_str).name
