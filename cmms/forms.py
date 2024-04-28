from django import forms
from .models import Maquina, Personal

def get_tuple(array, atribute):
    arr = []
    if atribute == "maquina":
        for index, value in enumerate(array):
            arr.append((index, value.nombre))
        return arr
    else:
        for index, value in enumerate(array):
            arr.append((index, value.nombre))
        return arr
maquinas = Maquina.objects.all()
machine_names = []
for index, value in enumerate(maquinas):
    machine_names.append((index, value.nombre))


personal = Personal.objects.all()
personal_names = []
for index, value in enumerate(personal):
    personal_names.append((index, value.nombre))

tipo = [
    (0, "preventivo"),
    (1, "correctivo"),
    (2, "predictivo"),
]

hecho = [
    (0, "si"),
    (1, "no")
]


class OrdenForm(forms.Form):


    fecha = forms.DateField(required=True, widget=forms.DateInput(
        attrs={
            "class":"form-control",
            "placeholder":"Date",
            "id":"date",
            "type":"date"
        }
    ))

    hora = forms.TimeField(required=False, widget=forms.TimeInput(
        attrs={
            "class":"form-control",
            "placeholder":"Hour",
            "id":"time",
            "type":"time"
        }
    ))

    maquina = forms.CharField(required=False, widget=forms.Select(choices=machine_names, attrs={
         "class":"form-control",
        "placeholder":"maquina",
        "id":"maquina"
    }))

 

    responsable = forms.CharField(required=False, widget=forms.Select(choices=personal_names, attrs={
         "class":"form-control",
        "placeholder":"responsable",
        "id":"responsable"
    }))

    actividad = forms.CharField(required=False, max_length=255, widget=forms.TextInput(
        attrs={
            "class":"form-control",
            "placeholder":"Activity",
            "id":"actividad"
        }
    ))

    tipo = forms.CharField(required=False, widget=forms.Select(choices=tipo, attrs={
         "class":"form-control",
        "placeholder":"tipo",
        "id":"tipo"
    }))
    
    realizado = forms.CharField(required=False, widget=forms.Select(choices=hecho, attrs={
         "class":"form-control",
        "placeholder":"realizado",
        "id":"realizado"
    }))

    autorizado = forms.CharField(required=False, widget=forms.Select(choices=personal_names, attrs={
         "class":"form-control",
        "placeholder":"autorizado",
        "id":"autorizado"
    }))


    tiempo = forms.IntegerField(required=False, min_value=0 , widget=forms.NumberInput(
        attrs={
            "class":"form-control",
            "placeholder":"Total time",
            "id":"tiempo"
        }
    ))

    costo = forms.FloatField(required=False, min_value=0, widget=forms.NumberInput(
        attrs={
            "class":"form-control",
            "placeholder":"Total cost",
            "id":"costo"
        }
    ))


class TimelineForm(forms.Form):

    pass


class VjpForm(forms.Form):

    pass

class ReportForm(forms.Form):

    pass


class Actualizar(forms.Form):

    pass


class EjecutivoForm(forms.Form):

    pass

