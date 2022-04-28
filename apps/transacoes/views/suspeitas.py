from django.shortcuts import render, redirect
from django.contrib import messages
from apps.transacoes.models import Transacao, ContaSuspeita, AgenciaSuspeita
from apps.usuarios.functions import *
from ..forms import Suspeita


def suspeitas(request):
    """renders the page with the suspect transactions"""
    if sem_permissao(request):
        return redirect('login')
    if request.method == "GET":
        context = {
            "form": Suspeita()
        }
        return render(request, 'transacoes/suspeitas.html', context)
    if request.method == "POST":
        data = request.POST['data']
        if not data:
            messages.error(request, "Selecione o mês e o ano")
            return redirect('suspeitas')

        transacoes_data = Transacao.objects.filter(data_hora_transacao__startswith=data)
        if not bool(transacoes_data):
            messages.error(request, 'Não há transações disponíveis neste mês/ano')
            return redirect('suspeitas')
        context = {
            "data": data,
            "transacoes_suspeitas": transacoes_suspeitas(transacoes_data),
            "contas_suspeitas": movimentacoes_suspeitas(transacoes_data, 'contas'),
            "agencias_suspeitas": movimentacoes_suspeitas(transacoes_data, 'agencias'),
            "form": Suspeita(), # options = {'defaultDate': data}

        }
        return render(request, 'transacoes/suspeitas.html', context)



def transacoes_suspeitas(transacoes_data):
    """checks for existence of suspect transactions based on month's transactions"""
    transacoes = []
    for transacao in transacoes_data:
        if float(transacao.valor_transacao) >= 100000:
            transacoes.append(transacao)
    return transacoes


def movimentacoes_suspeitas(transacoes_data, busca):
    """checks for existence of suspect accounts or agencies based on month's transactions"""
    contas = []

    origem_set = set()
    for transacao in transacoes_data:
        if busca == "contas":
            origem_set.add(transacao.conta_origem)
        elif busca == "agencias":
            origem_set.add(transacao.agencia_origem)

    for item_set in origem_set:
        if busca == "contas":
            transacoes = transacoes_data.filter(conta_origem=item_set)
        elif busca == "agencias":
            transacoes = transacoes_data.filter(agencia_origem=item_set)
        valor = 0
        for transacao_filtrada in transacoes:
            valor += float(transacao_filtrada.valor_transacao)
        if busca == "contas":
            if valor > 1000000:
                contas.append(ContaSuspeita(banco=transacao_filtrada.banco_origem, valor=valor,
                                            agencia=transacao_filtrada.agencia_origem,
                                            conta=transacao_filtrada.conta_origem, movimento="Saída"))
        elif busca == "agencias":
            if valor > 1000000000:
                contas.append(AgenciaSuspeita(banco=transacao_filtrada.banco_origem, valor=valor,
                                              agencia=transacao_filtrada.agencia_origem,
                                              movimento="Saída"))

    destino_set = set()
    for transacao in transacoes_data:
        if busca == "contas":
            origem_set.add(transacao.conta_destino)
        elif busca == "agencias":
            origem_set.add(transacao.agencia_destino)

    for item_set in destino_set:
        if busca == "contas":
            transacoes = transacoes_data.filter(conta_destino=item_set)
        elif busca == "agencias":
            transacoes = transacoes_data.filter(agencia_destino=item_set)
        valor = 0
        for transacao_filtrada in transacoes:
            valor += float(transacao_filtrada.valor_transacao)
        if busca == "contas":
            if valor > 1000000:
                contas.append(ContaSuspeita(banco=transacao_filtrada.banco_origem, valor=valor,
                                            agencia=transacao_filtrada.agencia_origem,
                                            conta=transacao_filtrada.conta_origem, movimento="Entrada"))
        elif busca == "agencias":
            if valor > 1000000000:
                contas.append(AgenciaSuspeita(banco=transacao_filtrada.banco_origem, valor=valor,
                                              agencia=transacao_filtrada.agencia_origem,
                                              movimento="Entrada"))

    return contas
