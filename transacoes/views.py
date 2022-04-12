from django.shortcuts import render
from django.http import FileResponse
from .models import Controller


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

    elif request.method == 'POST':

        nome = request.FILES['file_name']
        tamanho = request.FILES['file_name'].size / 1000000
        if tamanho == 0:
            raise ValueError("O arquivo está vazio")
        print(nome)
        print(tamanho, "megabytes")

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

        request.method = 'GET'
        return render(request, 'index.html')
