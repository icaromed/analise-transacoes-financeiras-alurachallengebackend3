from django.db import models


class Controller(models.Model):
    banco_origem = models.CharField(max_length=50)
    agencia_origem = models.CharField(max_length=50)
    conta_origem = models.CharField(max_length=50)
    banco_destino = models.CharField(max_length=50)
    agencia_destino = models.CharField(max_length=50)
    conta_destino = models.CharField(max_length=50)
    valor_transacao = models.CharField(max_length=50)
    data_hora_transacao = models.CharField(max_length=50)
