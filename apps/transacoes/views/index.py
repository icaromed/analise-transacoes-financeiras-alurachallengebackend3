from django.shortcuts import render, redirect
from django.http import FileResponse
from apps.transacoes.models import Transacao, DataImportacoes
from datetime import datetime
from django.contrib import messages
import xml.etree.ElementTree as ET


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.deleted:
        return redirect('login')

    todos_objetos = DataImportacoes.objects.all().order_by('-data_transacao')

    if request.method == 'GET':
        return render(request, 'transacoes/index.html', {"todos_objetos": todos_objetos})

    elif request.method == 'POST':
        if not request.FILES:
            messages.error(request, 'Nenhum arquivo foi selecionado')
            return redirect('index')
        else:
            nome = request.FILES['file_name'].name

        if nome.endswith('.csv'):
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

                transacao_valida = Transacao.objects.create(banco_origem=comando[0], agencia_origem=comando[1],
                                                             conta_origem=comando[2], banco_destino=comando[3],
                                                             agencia_destino=comando[4], conta_destino=comando[5],
                                                             valor_transacao=comando[6], data_hora_transacao=comando[7])
                transacao_valida.save()
                comandos_efetuados.append(comando)

            importacao = DataImportacoes(data_transacao="/".join(data_padrao.split('-')[-1::-1]),
                                         data_importacao=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'),
                                         id_usuario=request.user.id)
            importacao.save()
            messages.success(request, 'Os arquivos foram salvos com sucesso')
            return render(request, 'transacoes/index.html', {"todos_objetos": todos_objetos})

        elif nome.endswith('.xml'):
            tree = ET.parse(request.FILES['file_name'])
            root = tree.getroot()

            if root.findall("transacao")[0].find('data') is None:
                messages.error(request, 'O conteúdo do arquivo não é válido')
                return redirect('index')

            data_padrao = root.findall("transacao")[0].find('data').text[0:10].strip()

            if not root.findall("transacao")[0].find('data').text[0:10]:
                messages.error(request, 'O conteúdo do arquivo não é válido')
                return redirect('index')

            data_validacao = "/".join(data_padrao.split('-')[-1::-1])
            if DataImportacoes.objects.filter(data_transacao=data_validacao).exists():
                messages.error(request, 'Data de transação já utilizada')
                return redirect('index')

            for transacao in root.findall("transacao"):
                comandos = []
                try:
                    banco_origem = transacao.find('origem').find('banco').text
                    agencia_origem = transacao.find('origem').find('agencia').text
                    conta_origem = transacao.find('origem').find('conta').text
                    banco_destino = transacao.find('destino').find('banco').text
                    agencia_destino = transacao.find('destino').find('agencia').text
                    conta_destino = transacao.find('destino').find('conta').text
                    valor = transacao.find('valor').text
                    data = transacao.find('data').text
                except ValueError:
                    messages.error(request, 'O conteúdo do arquivo não é válido')
                    return redirect('index')
                if not banco_origem or not agencia_origem or not conta_origem or not banco_destino or not conta_destino or not agencia_destino or not conta_destino or not valor or not data:
                    continue
                if data[0:10] != data_padrao:
                    continue
                comando = ",".join([banco_origem, agencia_origem, conta_origem, banco_destino, agencia_destino, conta_destino, valor])
                if comando in comandos:
                    continue
                else:
                    transacao_valida = Transacao.objects.create(banco_origem=banco_origem, agencia_origem=agencia_origem,
                                                                 conta_origem=conta_origem, banco_destino=banco_destino,
                                                                 agencia_destino=agencia_destino, conta_destino=conta_destino,
                                                                 valor_transacao=valor,
                                                                 data_hora_transacao=data)
                    transacao_valida.save()
                    comandos.append(comando)

            importacao = DataImportacoes(data_transacao="/".join(data_padrao.split('-')[-1::-1]),
                                         data_importacao=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'),
                                         id_usuario=request.user.id)
            importacao.save()
            messages.success(request, 'Os arquivos foram salvos com sucesso')
            return render(request, 'transacoes/index.html', {"todos_objetos": todos_objetos})

        elif not nome.endswith('.csv') and not nome.endswith('.xml'):
            messages.error(request, 'O arquivo não é do formato .csv ou .xml')
            return redirect('index')
