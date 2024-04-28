from django import urls
from django.urls import path
from . import views

app_name = "cmms"

urlpatterns = [
    path("", views.index, name="index"),
    path("orden/", views.orden_trabajo, name="orden"),
    path("actualizar/", views.actualizar, name="actualizar"),
    path("ejecutivo/", views.ejecutivo, name="ejecutivo"),
    path("vjp/", views.reporte, name="reporte"),
    path("timeline/", views.timeline, name="timeline"),
    path('<int:reporteId>/', views.reporte_detail, name="reporte_detail")
]