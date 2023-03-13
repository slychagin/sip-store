from django import template


register = template.Library()


@register.filter(name='get_range')
def get_range(value):
    """
    Filter returns a list containing range made from given value
    """
    return range(int(value))
