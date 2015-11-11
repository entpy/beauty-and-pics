from django import template

register = template.Library()

@register.filter
def str_cat(arg1, arg2):
    """Custom filter to concatenate arg1 with arg2"""
    return str(arg1) + str(arg2)
