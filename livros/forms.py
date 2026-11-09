from django import forms

from .models import Leitura, Resenha

# Campo de data com calendário do navegador (type="date").
# O format garante que a data salva apareça preenchida ao editar.
CAMPO_DATA = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')


class LeituraForm(forms.ModelForm):
    class Meta:
        model = Leitura
        fields = ['status', 'pagina_atual', 'vezes_lida', 'data_inicio', 'data_termino']
        widgets = {'data_inicio': CAMPO_DATA, 'data_termino': CAMPO_DATA}


class ResenhaForm(forms.ModelForm):
    class Meta:
        model = Resenha
        fields = ['nota', 'contexto', 'pontos_fortes', 'pontos_fracos']
        widgets = {
            'nota': forms.NumberInput(attrs={'min': 0, 'max': 10}),
            'contexto': forms.Textarea(attrs={'rows': 3}),
            'pontos_fortes': forms.Textarea(attrs={'rows': 3}),
            'pontos_fracos': forms.Textarea(attrs={'rows': 3}),
        }
