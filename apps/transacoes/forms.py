from django import forms
from tempus_dominus.widgets import DatePicker


class Suspeita(forms.Form):
    data = forms.CharField(label="Selecione o mês para analisar as transações", widget=DatePicker(options={'input_group': True}))

