from django.db import models


class Controller(models.Model):
    banco_origem = models.CharField(max_length=150)
    agencia_origem = models.CharField(max_length=150)
    conta_origem = models.CharField(max_length=150)
    banco_destino = models.CharField(max_length=150)
    agencia_destino = models.CharField(max_length=150)
    conta_destino = models.CharField(max_length=150)
    valor_transacao = models.CharField(max_length=150)
    data_hora_transacao = models.CharField(max_length=150)


class DataImportacoes(models.Model):
    data_importacao = models.CharField(max_length=150)
    data_transacao = models.CharField(max_length=150)
    id_usuario = models.CharField(max_length=20)
