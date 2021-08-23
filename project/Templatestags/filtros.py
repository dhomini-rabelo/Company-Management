from django import template

register = template.Library()

@register.filter(name='ano')
def _ano(valor):
    return str(valor)[:4]