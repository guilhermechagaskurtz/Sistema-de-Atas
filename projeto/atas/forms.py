from django import forms
from curso.models import Curso


class BuscaAtaForm(forms.Form):
    data = forms.CharField(label='Informe dia, ou mês, ou ano', required=False)
    curso = forms.ModelChoiceField(label='Curso', queryset=Curso.objects.all(), required=False)
    conteudo = forms.CharField(label='Pesquise por um determinado conteúdo', required=False)