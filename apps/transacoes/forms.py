from django import forms
from tempus_dominus.widgets import DatePicker


class Suspeita(forms.Form):
    data = forms.CharField(label="Selecione o mês para analisar as transações", widget=DatePicker())


class Arquivo(forms.Form):
    file_name = forms.FileField(allow_empty_file=False)
