from django import template


register = template.Library()


@register.filter
def get_item(item, string):
    return item.get(string, '')
