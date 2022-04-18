from django.shortcuts import render, redirect
from django.http import FileResponse
from .models import Controller, DataImportacoes
from datetime import datetime
from django.contrib import messages


def index(request):
    todos_objetos = DataImportacoes.objects.all().order_by('-data_transacao')

    if request.method == 'GET':
        return render(request, 'index.html', {"todos_objetos": todos_objetos})

    elif request.method == 'POST':
        if not request.FILES:
            messages.error(request, 'Nenhum arquivo foi selecionado')
            return redirect('index')
        else:
            nome = request.FILES['file_name'].name

        if not nome.endswith('.csv'):
            messages.error(request, 'O arquivo não é do formato .csv')
            return redirect('index')

        file_h = FileResponse(request.FILES['file_name'])
        comandos = list(file_h.streaming_content)[0].decode('utf-8').split('\n')

        data_padrao = comandos[0][-19:-9].strip()
        if not data_padrao:
            messages.error(request, 'O arquivo não pode estar vazio')
            return redirect('index')

        data_validacao = "/".join(data_padrao.split('-')[-1::-1])
        if DataImportacoes.objects.filter(data_transacao=data_validacao).exists():
            messages.error(request, 'Data de transação já utilizada')
            return redirect('index')

        comandos_efetuados = []
        for pos in range(len(comandos)):
            comando = comandos[pos].split(",")
            if len(comando) != 8:
                continue
            data = comando[-1][:10]

            for item in comando:
                if not item:
                    data = ""
            if data != data_padrao:
                continue
            if comando in comandos_efetuados:
                continue

            transacao_valida = Controller.objects.create(banco_origem=comando[0], agencia_origem=comando[1],
                                                         conta_origem=comando[2], banco_destino=comando[3],
                                                         agencia_destino=comando[4], conta_destino=comando[5],
                                                         valor_transacao=comando[6], data_hora_transacao=comando[7])
            transacao_valida.save()
            comandos_efetuados.append(comando)

        importacao = DataImportacoes(data_transacao="/".join(data_padrao.split('-')[-1::-1]),
                                     data_importacao=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
        importacao.save()
        messages.success(request, 'Os arquivos foram salvos com sucesso')
        return render(request, 'index.html', {"todos_objetos": todos_objetos})
