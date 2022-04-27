from django.template.defaulttags import register
from apps.usuarios.models import User


@register.filter
def get_item(id_n):
    return User.objects.filter(id=id_n).get().username

