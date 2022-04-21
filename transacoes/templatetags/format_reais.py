from django.template.defaulttags import register


@register.filter
def format_reais(valor):
    valor = 'R${:,.2f}'.format(float(valor)).split('.')
    for pos in range(len(valor)):
        valor[pos] = valor[pos].replace(',', '.')
    return ",".join(valor)
