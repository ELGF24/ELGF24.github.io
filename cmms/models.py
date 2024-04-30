from django.db import models
import datetime

from django.urls import reverse
# Create your models here.

class Maquina(models.Model):

    machineId = models.IntegerField(primary_key=True, default=0, unique=True)
    nombre = models.CharField(unique=True, verbose_name="maquina", db_index=True)
    codigo = models.CharField(max_length=25, verbose_name="codigoMaquina")

    class Meta:
        ordering = ("codigo",)
        verbose_name = "maquina"
        verbose_name_plural = "maquinas"
        db_table = "maquinas"

class Personal(models.Model):
    CHOICES = (
        ("practicante", "Practicante"),
        ("ingeniero", "Ingeniero"),
        ("gerente", "Gerente")
    )
    userId = models.IntegerField(primary_key=True, default=0, unique=True)
    nombre = models.CharField(verbose_name="nombre")
    codUser = models.IntegerField(verbose_name="userCode", unique=True)
    puesto = models.CharField(choices=CHOICES, default="ingeniero", verbose_name="puesto")

class DoneManager(models.Manager):
    def get_queryset(self):
        return super(DoneManager, self).get_queryset().filter(realizado="si")

class OrdenDeMantenimiento(models.Model):

    CHOICES = (
        ('si', 'Si'),
        ('no', 'No')
    )
    now = datetime.datetime.now()
    time = now.time()
    reporteId = models.IntegerField(primary_key=True)
    fecha = models.DateField(verbose_name="fecha")
    hora = models.TimeField(verbose_name="hora", default=time)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='ordenes_mantenimiento')
    responsable = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='ordenes_mantenimiento')
    actividad = models.CharField(verbose_name="actividad")
    tipo = models.CharField(max_length=20, choices=[('preventivo', 'Preventivo'), ('correctivo', 'Correctivo')], verbose_name="tipo")
    realizado = models.CharField(max_length=3, choices=CHOICES, verbose_name="realizado")
    autorizado = models.CharField(max_length=255, verbose_name="autorizado")
    tiempo = models.IntegerField(verbose_name="tiempo")
    costo = models.FloatField(verbose_name="costo")

    objects = models.Manager()
    done_objects = DoneManager()

    def __str__(self):
        return f"Orden de Mantenimiento - {self.maquina.nombre} - {self.fecha}"
    
    def get_absolute_url(self):
        return reverse("cmms:reporte_detail", args=[self.reporteId])

