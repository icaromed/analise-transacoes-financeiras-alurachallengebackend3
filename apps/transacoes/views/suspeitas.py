from django.shortcuts import render, redirect
from django.contrib import messages
from apps.transacoes.models import Transacao, ContaSuspeita, AgenciaSuspeita


def suspeitas(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.deleted:
        return redirect('login')

    if request.method == "POST":
        data = request.POST['date']
        if not data:
            messages.error(request, "Selecione o mês e o ano")
            return redirect('suspeitas')

        transacoes_data = Transacao.objects.filter(data_hora_transacao__startswith=data)
        if not bool(transacoes_data):
            messages.error(request, 'Não há transações disponíveis neste mês')
            return redirect('suspeitas')
        context = {
            "data": data,
            "transacoes_suspeitas": transacoes_suspeitas(transacoes_data),
            "contas_suspeitas": contas_suspeitas(transacoes_data),
            "agencias_suspeitas": agencias_suspeitas(transacoes_data)
        }
        return render(request, 'transacoes/suspeitas.html', context)
    return render(request, 'transacoes/suspeitas.html')


def transacoes_suspeitas(transacoes_data):

    transacoes = []
    for transacao in transacoes_data:
        if float(transacao.valor_transacao) >= 100000:
            transacoes.append(transacao)
    return transacoes


def contas_suspeitas(transacoes_data):
    contas = []

    contas_origem_set = set()
    for transacao in transacoes_data:
        contas_origem_set.add(transacao.conta_origem)
    for conta in contas_origem_set:
        transacoes = transacoes_data.filter(conta_origem=conta)
        valor = 0
        for transacao_filtrada in transacoes:
            valor += float(transacao_filtrada.valor_transacao)
        if valor > 1000000:
            contas.append(ContaSuspeita(banco=transacao_filtrada.banco_origem, valor=valor, agencia=transacao_filtrada.agencia_origem,
                          conta=transacao_filtrada.conta_origem, movimento="Saída"))

    contas_destino_set = set()
    for transacao in transacoes_data:
        contas_destino_set.add(transacao.conta_destino)
    for conta in contas_destino_set:
        transacoes = transacoes_data.filter(conta_destino=conta)
        valor = 0
        for transacao_filtrada in transacoes:
            valor += float(transacao_filtrada.valor_transacao)
        if valor > 1000000:
            contas.append(ContaSuspeita(banco=transacao_filtrada.banco_destino, valor=valor,
                                        agencia=transacao_filtrada.agencia_destino,
                                        conta=transacao_filtrada.conta_destino, movimento="Entrada"))

    return contas


def agencias_suspeitas(transacoes_data):
    agencias = []

    agencias_origem_set = set()
    for transacao in transacoes_data:
        agencias_origem_set.add(transacao.agencia_origem)
    for agencia in agencias_origem_set:
        transacoes = transacoes_data.filter(agencia_origem=agencia)
        valor = 0
        for transacao_filtrada in transacoes:
            valor += float(transacao_filtrada.valor_transacao)
        if valor > 1000000000:
            agencias.append(AgenciaSuspeita(banco=transacao_filtrada.banco_origem, valor=valor,
                                            agencia=transacao_filtrada.agencia_origem,
                                            movimento="Saída"))

    agencias_destino_set = set()
    for transacao in transacoes_data:
        agencias_destino_set.add(transacao.agencia_destino)
    for agencia in agencias_destino_set:
        transacoes = transacoes_data.filter(agencia_destino=agencia)
        valor = 0
        for transacao_filtrada in transacoes:
            valor += float(transacao_filtrada.valor_transacao)
        if valor > 1000000000:
            agencias.append(AgenciaSuspeita(banco=transacao_filtrada.banco_destino, valor=valor,
                                            agencia=transacao_filtrada.agencia_destino,
                                            movimento="Entrada"))

    return agencias
