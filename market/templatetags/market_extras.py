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


@register.filter
def filled_stars(rating, max_stars=5):
    """
    Return a range for the number of filled stars.

    """
    try:
        rating = int(rating)
        max_stars = int(max_stars)
    except (TypeError, ValueError):
        return range(0)

    rating = max(0, min(rating, max_stars))
    return range(rating)


@register.filter
def empty_stars(rating, max_stars=5):
    """
    Return a range for the number of empty stars
    (max_stars - rating, never negative).
    """
    try:
        rating = int(rating)
        max_stars = int(max_stars)
    except (TypeError, ValueError):
        return range(0)

    rating = max(0, min(rating, max_stars))
    return range(max_stars - rating)


@register.filter
def get_city(value):
    """
    Extracts the city part from a 'City, State' formatted string.
    Example: 'Essen, NRW' -> 'Essen'
    Returns an empty string if the value is empty or not properly formatted.
    """
    if not value:
        return ""

    parts = value.split(",", 1)
    city = parts[0].strip()
    return city


@register.filter
def get_state(value):
    """
    Extracts the state/region part from a 'City, State' formatted string.
    Example: 'Essen, NRW' -> 'NRW'
    Returns an empty string if the string does not contain a comma or is invalid.
    """
    if not value:
        return ""

    parts = value.split(",", 1)
    if len(parts) < 2:
        return ""

    state = parts[1].strip()
    return state


@register.filter
def user_liked(obj, user):
    """
    Custom filter to check if the given user has liked the specific object.

    - Usage: {% if postitem|user_liked:user %}
    - Returns False if the user is not authenticated.
    - Uses the GenericRelation 'likes' to query for the user's like.
    """

    if not user.is_authenticated:
        return False

    return obj.likes.filter(author=user).exists()


@register.filter
def user_commented(obj, user):
    """
    Custom filter to check if the given user has commented on the specific object.

    - Usage: {% if postitem|user_commented:user %}
    - Returns False if the user is not authenticated.
    - Uses the reverse ForeignKey 'comments' to query.
    """
    if not user.is_authenticated:
        return False

    return obj.comments.filter(author=user).exists()
