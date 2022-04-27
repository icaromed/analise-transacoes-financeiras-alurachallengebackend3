from django.shortcuts import render, redirect
from apps.transacoes.models import Transacao


def detalhar(request, data):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.deleted:
        return redirect('login')

    data = f"{data[0:2]}/{data[2:4]}/{data[4:]}"
    data_h = "-".join(reversed(data.split("/")))
    if request.method == 'GET':
        print(data)
        users = Transacao.objects.filter(data_hora_transacao__startswith=data_h)
        return render(request, 'transacoes/detalhar.html', {"data": data, "users": users})
