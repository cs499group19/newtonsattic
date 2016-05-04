from django import template

register = template.Library()


@register.filter
def get_item(item, string):
    """
    Helper to allow dict lookups in views.
    :param item: dict object
    :param string: key
    :return: the result of `item.get(string, '')`
    """
    return item.get(string, '')
