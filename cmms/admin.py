from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo']
    ordering = ['codigo']


@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ["nombre", "codUser", "puesto"]

@admin.register(OrdenDeMantenimiento)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'maquina', 'responsable']