from django import template


register = template.Library()


@register.filter(name='get_index')
def get_index(my_list, i):
    """
    Custom filter that analogue enumerate list in python.
    Use in navbar template.
    """
    return my_list[i]
