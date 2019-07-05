# coding=utf-8

from django.template import Library

register = Library()

@register.simple_tag
def numbering(value, index, num):
    count = (value - 1) * num + 1
    return count + index
