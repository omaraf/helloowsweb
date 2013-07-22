from django import forms

class Salaform(forms.Form):
    descripcion = forms.CharField(max_length=255)
    fecha = forms.DateField()
    hora_inicio = forms.TimeField()
    hora_fin = forms.TimeField()
