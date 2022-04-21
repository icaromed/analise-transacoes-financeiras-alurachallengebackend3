from django.template.defaulttags import register
from transacoes.models import DataImportacoes


@register.filter
def transacoes(data):
    return DataImportacoes.objects.filter(data_transacao=data).get().data_transacao
