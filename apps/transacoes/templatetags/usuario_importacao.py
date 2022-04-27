from django.template.defaulttags import register
from apps.transacoes.models import DataImportacoes
from apps.usuarios.models import User


@register.filter
def usuario_importacao(data):
    id_usuario = DataImportacoes.objects.filter(data_transacao=data).get().id_usuario
    return User.objects.filter(id=id_usuario).get().username
