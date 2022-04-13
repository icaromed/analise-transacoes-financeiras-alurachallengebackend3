from django.shortcuts import render
from django.http import FileResponse
from .models import Controller, DataImportacoes
from datetime import datetime


def index(request):
    todos_objetos = DataImportacoes.objects.all().order_by('data_transacao')
    if request.method == 'GET':
        return render(request, 'index.html', {"todos_objetos": todos_objetos})

    elif request.method == 'POST':

        nome = request.FILES['file_name']
        tamanho = request.FILES['file_name'].size / 1000000
        print(nome)
        print(tamanho, "megabytes")
        if tamanho == 0:
            raise ValueError("O arquivo está vazio")
        if not nome.__str__().endswith('.csv'):
            raise ValueError("O arquivo não é do formato 'csv'")

        file_h = FileResponse(request.FILES['file_name'])
        comandos = list(file_h.streaming_content)[0].decode('utf-8').split('\n')
        comandos_efetuados = []
        data_padrao = None
        for pos in range(len(comandos)):
            comando = comandos[pos].split(",")
            if len(comando) != 8:
                continue
            if len(comandos_efetuados) == 0:
                data_padrao = comando[-1][:10]
            data = comando[-1][:10]
            for item in comando:
                if not item:
                    data = ""

            if data != data_padrao or comando in comandos_efetuados:
                continue
            transacao_valida = Controller(banco_origem=comando[0], agencia_origem=comando[1], conta_origem=comando[2],
                                          banco_destino=comando[3], agencia_destino=comando[4],
                                          conta_destino=comando[5], valor_transacao=comando[6],
                                          data_hora_transacao=comando[7])
            transacao_valida.save()
            comandos_efetuados.append(comando)
        importacao = DataImportacoes(data_transacao="/".join(data_padrao.split('-')[-1::-1]),
                                     data_importacao=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
        importacao.save()

        request.method = 'GET'
        return render(request, 'index.html', {"todos_objetos": todos_objetos})
