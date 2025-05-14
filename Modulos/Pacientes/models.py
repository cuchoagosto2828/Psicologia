from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Trastorno(models.Model):
    id_trastorno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Diagnostico(models.Model):
    id_diagnostico=models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey('Estudiantes', on_delete=models.CASCADE)
    diagnostico=models.CharField(max_length=50)
    nivel= models.CharField(
        max_length=15,
        choices=[
        ('Leve', 'Leve'), 
        ('Moderado', 'Moderado'),
        ('Grave', 'Grave'),
        ('Muy grave', 'Muy grave')
        ]
    )
    requiereInter=models.CharField(
        max_length=2,
        choices=[('Sí', 'Sí'), ('No', 'No')],
        default='No'
    )
    fechaInter = models.DateTimeField(null=True, blank=True)
    detalleInter= models.CharField(max_length=10000,null=True, blank=True)
    trastorno = models.ForeignKey('Trastorno', on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.CharField(max_length=10000, null=True, blank=True)
    

    def __str__(self):
        return f"{self.id_diagnostico} - {self.diagnostico} (Nivel {self.nivel})"


class Estudiantes(models.Model):
    id_estudiante = models.CharField(max_length=5, primary_key=True)
    documento = models.CharField(max_length=10)
    nombres = models.CharField(max_length=35)
    apellidos = models.CharField(max_length=35)
    edad = models.PositiveSmallIntegerField() 
    direccion = models.CharField(max_length=30, default=' ')
    email = models.CharField(max_length=100, default=' ', unique=True, null=True, blank=True) 
    nombreAcudiente = models.CharField(max_length=35)
    apellidoAcudiente = models.CharField(max_length=35)
    documentoAcu = models.CharField(max_length=10) 
    telefonoAcu = models.CharField(max_length=15, blank=True, null=True)
    emailAcu = models.CharField(max_length=50)
    

    # Choices de grado
    GRADOS = [
        ('1A', '1A'),
        ('1B', '1B'),
        ('2A', '2A'),
        ('2B', '2B'),
        ('3A', '3A'),
        ('3B', '3B'),
        ('4A', '4A'),
        ('4B', '4B'),
        ('5A', '5A'),
        ('5B', '5B')
    ]
    grado = models.CharField(max_length=3, choices=GRADOS)

    id_diagnostico = models.ForeignKey(Diagnostico, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - Grado {self.grado}" 




class HistoriaClinica(models.Model):
    id_historia = models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey('Estudiantes', on_delete=models.CASCADE, related_name='historias_clinicas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Profesional que crea la historia
    profesional = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Información clínica
    motivo_consulta = models.TextField(null=True, blank=True)
    antecedentes_personales = models.TextField(null=True, blank=True)
    antecedentes_familiares = models.TextField(null=True, blank=True)
    evaluacion_psicologica = models.TextField(null=True, blank=True)
    estado_actual = models.CharField(max_length=255, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField()

    # Diagnóstico y tratamiento
    id_diagnostico = models.ForeignKey('Diagnostico', on_delete=models.CASCADE)
    plan_tratamiento = models.ForeignKey('PlanTratamiento', on_delete=models.CASCADE, null=True, blank=True)
    intervenciones = models.ManyToManyField('Intervencion', blank=True)

    # PIAR
    PIAR = models.TextField(null=True, blank=True)
    detalles_PIAR = models.TextField(null=True, blank=True)

    recomendaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Historia {self.id_historia} - {self.id_estudiante}"


class PlanTratamiento(models.Model):
    id_plan = models.AutoField(primary_key=True)
    id_historia = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE)
    objetivo = models.CharField(max_length=255)
    detalles = models.TextField(null=True, blank=True)  # Descripción del objetivo o plan
    fecha_inicio = models.DateTimeField()
    fecha_revision = models.DateTimeField(null=True, blank=True)  # Fecha de revisión o evaluación
    frecuencia = models.CharField(max_length=100, null=True, blank=True)  # Ejemplo: "semanal", "mensual", etc.

    def __str__(self):
        return f"Plan {self.id_plan} - {self.objetivo}"



class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE)
    id_diagnostico = models.ForeignKey(Diagnostico, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField()
    motivo = models.TextField()
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cita {self.id_cita} - {self.id_estudiante} el {self.fecha.strftime('%Y-%m-%d %H:%M')}"


class Observacion(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Observación para Cita {self.cita.id_cita}"


class Intervencion(models.Model):
    TIPOS = [
        ('Intervención individual', 'Intervención individual'),
        ('Intervención grupal', 'Intervención grupal'),
        ('Intervención familiar', 'Intervención familiar'),
        ('Intervención psicoeducativa', 'Intervención psicoeducativa'),
        ('Intervención en crisis', 'Intervención en crisis'),
        ('Intervención comunitaria o social', 'Intervención comunitaria o social'),
        ('Intervención preventiva', 'Intervención preventiva')
    ]

    id_intervencion = models.AutoField(primary_key=True)
    id_historia = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE)
    tipo_intervencion = models.CharField(max_length=100, choices=TIPOS) 
    fecha = models.DateTimeField()
    detalles = models.TextField()
    motivoIn = models.TextField()

    def __str__(self):
        return f"Intervención {self.id_intervencion} - {self.tipo_intervencion} ({self.fecha.strftime('%Y-%m-%d')})"

