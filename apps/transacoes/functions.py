from django.http import FileResponse
import xml.etree.ElementTree as ET
from apps.transacoes.models import Transacao, DataImportacoes
from datetime import datetime


def comandos_csv(request):
    file_h = FileResponse(request.FILES['file_name'])
    comandos = list(file_h.streaming_content)[0].decode('utf-8').split('\n')
    data_padrao = comandos[0][-19:-9].strip()
    if not data_padrao:
        return False, 'O arquivo não pode estar vazio'

    data_validacao = "/".join(data_padrao.split('-')[-1::-1])
    if DataImportacoes.objects.filter(data_transacao=data_validacao).exists():
        return False, 'Data de transação já utilizada'

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
    return True, 'Os arquivos foram salvos com sucesso'


def comandos_xml(request):
    tree = ET.parse(request.FILES['file_name'])
    root = tree.getroot()

    if root.findall("transacao")[0].find('data') is None:
        return False, 'O conteúdo do arquivo não é válido'

    data_padrao = root.findall("transacao")[0].find('data').text[0:10].strip()

    if not root.findall("transacao")[0].find('data').text[0:10]:
        return False, 'O conteúdo do arquivo não é válido'

    data_validacao = "/".join(data_padrao.split('-')[-1::-1])
    if DataImportacoes.objects.filter(data_transacao=data_validacao).exists():
        return False, 'Data de transação já utilizada'

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
            return False, 'O conteúdo do arquivo não é válido'

        if not banco_origem or not agencia_origem or not conta_origem or not banco_destino or not conta_destino or not agencia_destino or not conta_destino or not valor or not data:
            continue
        if data[0:10] != data_padrao:
            continue
        comando = ",".join(
            [banco_origem, agencia_origem, conta_origem, banco_destino, agencia_destino, conta_destino, valor])
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
    return True, 'Os arquivos foram salvos com sucesso'
