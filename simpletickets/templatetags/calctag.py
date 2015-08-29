# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.filter(name='porcent')
def porcent(number, total):
    return number * 100 / total
