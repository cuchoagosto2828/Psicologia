from django.contrib import admin
from Modulos.Pacientes.models import *

# Register your models here.

admin.site.register(Diagnostico)
admin.site.register(Estudiantes)
admin.site.register(HistoriaClinica)
admin.site.register(Cita)
admin.site.register(Intervencion)


