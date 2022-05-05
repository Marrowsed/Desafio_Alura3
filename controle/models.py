from django.db import models
from datetime import datetime

class Controller(models.Model):
    file = models.FileField(upload_to='arquivos/', blank=False)
    enviado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Arquivo: {self.file}"

class Transacao(models.Model):
    banco_origem = models.CharField(max_length=100, blank=False)
    agencia_origem = models.CharField(max_length=4, blank=False)
    conta_origem = models.CharField(max_length=7, blank=False)
    banco_destino = models.CharField(max_length=200, blank=False)
    agencia_destino = models.CharField(max_length=4, blank=False)
    conta_destino = models.CharField(max_length=7, blank=False)
    valor = models.FloatField(blank=False)
    data_transacao = models.DateTimeField(blank=False)
    data_importacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.banco_origem} -> {self.banco_destino} - RS{self.valor} - Data: {self.data_transacao}"

    class Meta:
        verbose_name_plural = "Transações"
