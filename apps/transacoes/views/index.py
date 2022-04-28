from django.shortcuts import render, redirect
from django.contrib import messages
from apps.usuarios.functions import *
from ..functions import *
from ..forms import Arquivo


def index(request):
    """renders input for transaction's files and a little menu with the uploaded transactions"""
    if sem_permissao(request):
        return redirect('login')

    todos_objetos = DataImportacoes.objects.all().order_by('-data_transacao')

    if request.method == 'GET':
        context = {
            'form': Arquivo(),
            'todos_objetos': todos_objetos,
        }
        return render(request, 'transacoes/index.html', context)

    elif request.method == 'POST':
        if not request.FILES:
            messages.error(request, 'Nenhum arquivo foi selecionado')
            return redirect('index')
        else:
            nome = request.FILES['file_name'].name

        if nome.endswith('.csv'):
            boolean, mensagem = comandos_csv(request)

        elif nome.endswith('.xml'):
            boolean, mensagem = comandos_xml(request)

        else:
            messages.error(request, 'O arquivo não é do formato .csv ou .xml')
            return redirect('index')

        if boolean:
            messages.success(request, mensagem)
            return redirect('index')
        else:
            messages.error(request, mensagem)
            return redirect('index')
