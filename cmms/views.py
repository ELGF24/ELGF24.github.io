from django.shortcuts import get_object_or_404, redirect, render

from . import forms
from .models import Maquina, Personal, OrdenDeMantenimiento

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Create your views here.
def index(request):
    maquinas = Maquina.objects.all()
    personal = Personal.objects.all()
    mantenimiento_realizado = OrdenDeMantenimiento.objects.filter(realizado="si").count()
    mantenimiento_no_realizado = OrdenDeMantenimiento.objects.filter(realizado="no").count()
    mantenimiento_preventivo = OrdenDeMantenimiento.objects.filter(tipo="preventivo").count()
    mantenimiento_correctivo = OrdenDeMantenimiento.objects.filter(tipo="correctivo").count()
    mantenimiento_predictivo = OrdenDeMantenimiento.objects.filter(tipo="predictivo").count()
    mantenimientos = [OrdenDeMantenimiento.objects.filter(tipo="preventivo").count(), OrdenDeMantenimiento.objects.filter(tipo="correctivo").count(), OrdenDeMantenimiento.objects.filter(tipo="predictivo").count()]
    labels = ["preventivo", "correctivo", "predictivo"]

    fig2 = go.Figure(data=[go.Pie(labels=labels, values=mantenimientos)])
    chart2 = fig2.to_html()


    dates = []
    costos = []
    tipo = []
    # Recorremos todas las órdenes de mantenimiento y almacenamos las fechas y costos
    for orden in OrdenDeMantenimiento.objects.all():
        dates.append(orden.fecha)
        costos.append(orden.costo)
        tipo.append(orden.tipo)


    # Creamos el DataFrame utilizando pandas
    df = pd.DataFrame({
        'Fecha': dates,
        'Costo': costos,
        "tipo":tipo
    })

    fig = px.scatter(
        df,
        x='Fecha', 
        y='Costo', 
        title="Costos de Mantenimiento en Función de la Fecha",
        color="tipo"
        )
    fig.update_traces(marker_size=15)
    
    chart = fig.to_html()

    preventivo = OrdenDeMantenimiento.objects.filter(tipo="preventivo")
    correctivo = OrdenDeMantenimiento.objects.filter(tipo="correctivo")
    predictivo = OrdenDeMantenimiento.objects.filter(tipo="predictivo")

    realizado = OrdenDeMantenimiento.objects.filter(realizado="si")
    no_realizado = OrdenDeMantenimiento.objects.filter(realizado="no")


    return render(request, "index.html", {
        "maquinas":maquinas,
        "personal":personal,
        'mantenimiento_realizado': mantenimiento_realizado,
        'mantenimiento_no_realizado': mantenimiento_no_realizado,
        "preventivo":mantenimiento_preventivo,
        "correctivo":mantenimiento_correctivo,
        "predictivo":mantenimiento_correctivo,
        "context":chart,
        "context2":chart2,
        "preventivo_orden":preventivo,
        "predictivo_orden":predictivo,
        "correctivo_orden":correctivo,
        "realizado":realizado,
        "no_realizado":no_realizado
    })


def orden_trabajo(request):
    form = forms.OrdenForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        fecha = form.cleaned_data.get("fecha")
        hora = form.cleaned_data.get("time")
        maquina = form.cleaned_data.get("maquina")
        responsable = form.cleaned_data.get("responsable")
        actividad = form.cleaned_data.get("actividad")
        tipo = form.cleaned_data.get("tipo")
        realizado = form.cleaned_data.get("realizado")
        autorizado = form.cleaned_data.get("autorizado")
        tiempo = form.cleaned_data.get("tiempo")
        costo = form.cleaned_data.get("costo")

        # encontrar valores de formulario
        maquina_seleccionada = Maquina.objects.get(machineId=maquina)
        personal_responsable = Personal.objects.get(userId=responsable)
        personal_autorizo = Personal.objects.get(userId=autorizado)

        if tipo == '0':
            tipo = "preventivo"
        elif tipo == '1':
            tipo = "correctivo"
        else:
            tipo = "predictivo"

        if realizado == '0':
            realizado = "si"
        else:
            realizado = 'no'
        total_reportes = OrdenDeMantenimiento.objects.all().count()
        orden = OrdenDeMantenimiento(reporteId=total_reportes+1 ,fecha=fecha, maquina=maquina_seleccionada, responsable=personal_responsable, actividad=actividad, tipo=tipo, realizado=realizado, autorizado=personal_autorizo.nombre, tiempo=tiempo, costo=costo)
        orden.save()

        return render(request, "reporte.html", {"orden":orden})


    return render(request, "orden_de_trabajo.html", {"form":form})
    
def timeline(request):
    maquinas = Maquina.objects.all()
    personal = Personal.objects.all()
    mantenimiento_realizado = OrdenDeMantenimiento.objects.filter(realizado="si").count()
    mantenimiento_no_realizado = OrdenDeMantenimiento.objects.filter(realizado="no").count()
    mantenimiento_preventivo = OrdenDeMantenimiento.objects.filter(tipo="preventivo").count()
    mantenimiento_correctivo = OrdenDeMantenimiento.objects.filter(tipo="correctivo").count()
    mantenimientos = [OrdenDeMantenimiento.objects.filter(tipo="preventivo").count(), OrdenDeMantenimiento.objects.filter(tipo="correctivo").count(), OrdenDeMantenimiento.objects.filter(tipo="predictivo").count()]
    labels = ["preventivo", "correctivo", "predictivo"]


    dates = []
    costos = []
    tipo = []
    # Recorremos todas las órdenes de mantenimiento y almacenamos las fechas y costos
    for orden in OrdenDeMantenimiento.objects.all():
        dates.append(orden.fecha)
        costos.append(orden.costo)
        tipo.append(orden.tipo)


    # Creamos el DataFrame utilizando pandas
    df = pd.DataFrame({
        'Fecha': dates,
        'Costo': costos,
        "tipo":tipo
    })

    fig = px.scatter(
        df,
        x='Fecha', 
        y='Costo', 
        title="Costos de Mantenimiento en Función de la Fecha",
        color="tipo"
        )
    fig.update_traces(marker_size=15)
    
    chart = fig.to_html()

    fechas = [mant.fecha for mant in OrdenDeMantenimiento.objects.all()]  # Extraer todas las fechas en una lista

    fecha_mas_temprana = min(fechas)
    fecha_mas_reciente = max(fechas)
    return render(request, "timeline.html", {"context":chart, "min_date":fecha_mas_temprana, "max_date":fecha_mas_reciente})


def reporte(request):
    reportes = OrdenDeMantenimiento.objects.all()
    return render(request, "vjp.html", {"reportes":reportes})

def reporte_detail(request, reporteId):
    reporte = get_object_or_404(OrdenDeMantenimiento, reporteId=reporteId)
    return render(request, 'detail.html', {"orden":reporte})

def actualizar(request):
    return render(request, "actualizar.html")

def ejecutivo(request):
    mantenimiento_realizado = OrdenDeMantenimiento.objects.filter(realizado="si").count()
    mantenimiento_no_realizado = OrdenDeMantenimiento.objects.filter(realizado="no").count()
    mantenimiento_preventivo = OrdenDeMantenimiento.objects.filter(tipo="preventivo").count()
    mantenimiento_correctivo = OrdenDeMantenimiento.objects.filter(tipo="correctivo").count()
    mantenimiento_predictivo = OrdenDeMantenimiento.objects.filter(tipo="predictivo").count()

    tipos_mantenimiento = ['Preventivo', 'Correctivo', 'Predictivo']

    # costos
    preventivo = OrdenDeMantenimiento.objects.filter(tipo="preventivo")
    correctivo = OrdenDeMantenimiento.objects.filter(tipo="correctivo")
    predictivo = OrdenDeMantenimiento.objects.filter(tipo="predictivo")

    costo_preventivo = sum([orden.costo for orden in preventivo])
    costo_correctivo = sum([orden.costo for orden in correctivo])
    costo_predictivo = sum([orden.costo for orden in predictivo])

    costos = [costo_preventivo, costo_correctivo, costo_predictivo]
    colores = ['#1f77b4', '#ff7f0e', '#2ca02c']

    fig = go.Figure(data=[go.Bar(x=tipos_mantenimiento, y=costos, marker=dict(color=colores))])
    fig.update_layout(title='Costos de Mantenimiento por Tipo',
                   xaxis_title='Tipo de Mantenimiento',
                   yaxis_title='Costo',
                   )
    chart = fig.to_html()
    
    mantenimientos = [OrdenDeMantenimiento.objects.filter(tipo="preventivo").count(), OrdenDeMantenimiento.objects.filter(tipo="correctivo").count(), OrdenDeMantenimiento.objects.filter(tipo="predictivo").count()]

    labels = ["preventivo", "correctivo", "predictivo"]

    fig2 = go.Figure(data=[go.Pie(labels=labels, values=mantenimientos)])
    chart2 = fig2.to_html()
    fechas = [mant.fecha for mant in OrdenDeMantenimiento.objects.all()]
    
    dates = []
    costos = []
    tipo = []
    # Recorremos todas las órdenes de mantenimiento y almacenamos las fechas y costos
    for orden in OrdenDeMantenimiento.objects.all():
        if orden.tipo == "predictivo" or orden.tipo == "correctivo":
            dates.append(orden.fecha)
            costos.append(orden.costo)
            tipo.append(orden.tipo)


    # Creamos el DataFrame utilizando pandas
    df = pd.DataFrame({
        'Fecha': dates,
        'Costo': costos,
        "tipo":tipo
    })

    fig3 = px.scatter(
        df,
        x='Fecha', 
        y='Costo', 
        title="Comparación de Costos de Mantenimiento Predictivo y Correctivo",
        color="tipo"
        )
    fig3.update_traces(marker_size=15)
    chart3 = fig3.to_html()
    
    return render(request, "ejecutivo.html", {"context":chart, "context2":chart2, "context3":chart3 , "fechas":fechas, "mantenimientos":OrdenDeMantenimiento.objects.all()})
