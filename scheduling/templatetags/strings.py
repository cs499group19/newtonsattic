from django import template

register = template.Library()


@register.filter
def to_str(value):
    """
    Convert value to string

    :param value: any object
    :return: str representation of `value`
    """
    return str(value)
