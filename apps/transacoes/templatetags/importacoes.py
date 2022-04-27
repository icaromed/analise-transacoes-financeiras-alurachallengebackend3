from django.template.defaulttags import register
from apps.transacoes.models import DataImportacoes


@register.filter
def importacoes(data):
    return DataImportacoes.objects.filter(data_transacao=data).get().data_importacao[0:18]
