from django import template

register = template.Library()

@register.filter(name='ano')
def _ano(valor):
    return str(valor)[:4]

@register.filter(name='grana')
def _grana(valor):
    value = str(valor)[:-3]
    size = len(value)
    new = []
    count = 0
    for c in range(size-1, -1, -1):
        count += 1
        if count % 3 == 0 and count != size:
            new.append(value[c])
            new.append('.')
        else:
            new.append(value[c])
    return ''.join(new)[::-1] + f',{str(valor)[-2:]}'

@register.filter(name='full')
def _full(full_path):
    return full_path[:-1]

@register.filter(name='capitalize')
def _capitalize(string):
    return string.replace('_',' ').replace('-',' ').capitalize()

@register.filter(name='enumerate')
def _enumerate(iterable):
    return enumerate(iterable)

@register.filter(name='next')
def _next(obj):
    return next(obj)

@register.filter(name='str')
def _str(obj):
    return str(obj)

@register.filter(name='demitido')
def _demitido(request):
    nome = request.GET.get('nome')
    demitido = request.GET.get('demitido')
    p = request.GET.get('p')
    if p is None and nome is None and demitido is None:
        return '?demitido=true'
    elif demitido == '':
        return f'{request.get_full_path()}true' 
    elif demitido == 'true':
        return f'{request.get_full_path()[:-4]}' 
    else:
        return f'{request.get_full_path()}&demitido=true' 

@register.filter(name='code')
def _code(code):
    if code < 2100000000:
        return True
    return False