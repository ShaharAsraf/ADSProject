from django import template

register = template.Library()


@register.filter(name='list_item')
def list_item(l, index):
    return l[index]
