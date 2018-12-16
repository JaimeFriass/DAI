from django import template
from django.utils.safestring import mark_safe
from django.template import Library

import json

register = Library()

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

register = template.Library()

@register.filter(name='get')
def get(d, k):
    return d.get(k, None)