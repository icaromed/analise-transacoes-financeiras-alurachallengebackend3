from django.template.defaulttags import register
from django.contrib.auth.models import User


@register.filter
def get_item(id_n):
    return User.objects.filter(id=id_n).get().username

