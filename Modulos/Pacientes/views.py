from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Trastorno, Diagnostico, Estudiantes, HistoriaClinica, Cita, Intervencion, Observacion, PlanTratamiento, SeguimientoPlan   
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def pagina_principal(request):
    return render(request, 'pagina_principal.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('gestionEstudiantes')  
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    
    return render(request, 'login.html')  

@never_cache
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('login')

def busqueda_global(request):
    query = request.GET.get('q', '')

    estudiantes = Estudiante.objects.filter(nombre__icontains=query) if query else []
    citas = Cita.objects.filter(motivo__icontains=query) if query else []
    historias = HistoriaClinica.objects.filter(observaciones__icontains=query) if query else []
    intervenciones = Intervencion.objects.filter(descripcion__icontains=query) if query else []

    contexto = {
        'query': query,
        'estudiantes': estudiantes,
        'citas': citas,
        'historias': historias,
        'intervenciones': intervenciones,
    }
    return render(request, 'busqueda_resultados.html', contexto)
    
@never_cache
@login_required
def home(request):
    estudiantes = Estudiantes.objects.all()
    diagnosticos = Diagnostico.objects.all()  # Obtener todos los diagnósticos
    trastornos = Trastorno.objects.all()  # Obtener todos los trastornos
    grados = Estudiantes.grado.field.choices  # Extraer los choices directamente del modelo

    return render(request, 'gestionEstudiantes.html', {
        'estudiantes': estudiantes,
        'trastornos': trastornos,
        'diagnosticos': diagnosticos,
        'grados': grados  # Ahora la plantilla tiene acceso a esta variable
    })

@never_cache
@login_required
def registrarEstudiante(request):
    if request.method == "POST":
        id_estudiante = request.POST["txtIdEstudiante"]
        documento = request.POST["txtDocumento"]
        nombres = request.POST["txtNombres"]
        apellidos = request.POST["txtApellidos"]
        edad = request.POST["txtEdad"]
        direccion = request.POST["txtDireccion"]
        email = request.POST["txtEmail"]
        grado = request.POST["txtGrado"]
        nombreAcudiente = request.POST["txtnombreAcudiente"]
        apellidoAcudiente = request.POST["txtapellidoAcudiente"]
        documentoAcu = request.POST["txtdocumentoAcu"]
        telefonoAcu = request.POST["txtTelefonoAcu"]
        emailAcu = request.POST["txtEmailAcu"]

        id_diagnostico = request.POST.get("txtIdDiagnostico", None)

        diagnostico = None
        if id_diagnostico:
            try:
                diagnostico = Diagnostico.objects.get(id_diagnostico=id_diagnostico)
            except Diagnostico.DoesNotExist:
                diagnostico = None

        nuevo_estudiante = Estudiantes.objects.create(
            id_estudiante=id_estudiante,
            documento=documento,
            nombres=nombres,
            apellidos=apellidos,
            edad=edad,
            direccion=direccion,
            email=email,
            nombreAcudiente=nombreAcudiente,
            apellidoAcudiente=apellidoAcudiente,
            documentoAcu=documentoAcu,
            telefonoAcu=telefonoAcu,
            emailAcu=emailAcu,
            grado=grado,
            id_diagnostico=diagnostico
        )

        messages.success(request, '¡Estudiante registrado!')
        return redirect('gestionEstudiante')


@never_cache
@login_required
def edicionEstudiante(request, id_estudiante):
    estudiante = Estudiantes.objects.get(id_estudiante=id_estudiante)
    diagnosticos = Diagnostico.objects.all()
    trastornos = Trastorno.objects.all()
    
    # Verificamos si el modelo de Estudiante tiene un campo 'grado' con opciones
    lista_grados = Estudiantes._meta.get_field('grado').choices
    
    return render(request, "edicionEstudiantes.html", {
        "estudiante": estudiante,
        "diagnosticos": diagnosticos,
        "grados": lista_grados,
        "trastornos": trastornos
    })

@never_cache
@login_required
def editarEstudiante(request):
    if request.method == "POST":
        id_estudiante = request.POST["txtId"]
        documento = request.POST["txtDocumento"]
        nombres = request.POST["txtNombres"]
        apellidos = request.POST["txtApellidos"]
        edad = request.POST["txtEdad"]
        direccion = request.POST["txtDireccion"]
        email = request.POST["txtEmail"]
        grado = request.POST["txtGrado"]
        nombreAcudiente = request.POST["txtnombreAcudiente"]
        apellidoAcudiente = request.POST["txtnombreAcudiente"]
        documentoAcu = request.POST["txtdocumentoAcu"]
        telefonoAcu = request.POST["txtTelefonoAcu"]
        emailAcu = request.POST["txtEmailAcu"]
        id_trastorno = request.POST.get("txtTrastorno", None)
    

        estudiante = Estudiantes.objects.get(id_estudiante=id_estudiante)

        diagnostico = Diagnostico.objects.get(id_trastorno=id_trastorno) if id_trastorno else None

        estudiante.documento = documento
        estudiante.nombres = nombres
        estudiante.apellidos = apellidos
        estudiante.edad = edad
        estudiante.direccion = direccion
        estudiante.email = email
        estudiante.grado = grado
        estudiante.id_diagnostico = diagnostico
        estudiante.nombreAcudiente = nombreAcudiente
        estudiante.apellidoAcudiente = apellidoAcudiente
        estudiante.documentoAcu = documentoAcu
        estudiante.telefonoAcu = telefonoAcu
        estudiante.emailAcu = emailAcu
        estudiante.save()

        messages.success(request, '¡Estudiante actualizado!')
        return redirect('/')

@never_cache
@login_required
def eliminarEstudiante(request, id_estudiante):
    estudiante = Estudiantes.objects.get(id_estudiante=id_estudiante)
    estudiante.delete()    

    messages.success(request, '¡Estudiante eliminado!')
    return redirect('/')


# ----------------------------------------------
# CRUD para Diagnóstico
# ----------------------------------------------

@never_cache
@login_required
def gestionDiagnostico(request):
    diagnosticos = Diagnostico.objects.all()
    estudiantes = Estudiantes.objects.all()
    trastornos = Trastorno.objects.all()
    planes = PlanTratamiento.objects.all()
    planes_dict = {plan.id_historia.id_diagnostico.id_diagnostico: plan for plan in planes}

    for diagnostico in diagnosticos:
        diagnostico.plan = planes_dict.get(diagnostico.id_diagnostico)

    return render(request, "gestionDiagnostico.html", {
        "diagnosticos": diagnosticos,
        "Estudiantes": estudiantes,  # Ahora se envían los estudiantes
        "trastornos": trastornos
    })

@never_cache
@login_required
def registrarDiagnostico(request):
    if request.method == "POST":
        id_diagnostico = request.POST.get("txtId")
        id_estudiante = request.POST.get("id_estudiante")
        diagnostico = request.POST["txtDiagnostico"]
        nivel = request.POST["txtNivel"]
        requiereInter = request.POST["requiereInter"]
        fechaInter = request.POST["fechaInter"]
        detalleInter = request.POST["detalleInter"]
        id_trastorno = request.POST.get("txtTrastorno", None)
        observaciones = request.POST["txtObservaciones"]


        estudiante = get_object_or_404(Estudiantes, id_estudiante=id_estudiante)
        trastorno = Trastorno.objects.get(id_trastorno=id_trastorno) if id_trastorno else None

        nuevo_diagnostico = Diagnostico(
        id_diagnostico=id_diagnostico,
        id_estudiante=estudiante,  # Aquí usas el objeto, no el ID
        diagnostico=diagnostico,
        nivel=nivel,
        requiereInter=requiereInter,
        fechaInter=fechaInter,
        detalleInter=detalleInter,
        trastorno=trastorno,
        observaciones=observaciones,
    )

        nuevo_diagnostico.save()

        # Si requiere intervención, crea la intervención
        if requiereInter == "Sí" and fechaInter:
            # Busca la historia clínica del estudiante
            historia = HistoriaClinica.objects.filter(id_estudiante=id_estudiante).first()
            if historia:
                Intervencion.objects.create(
                    id_historia=historia,
                    tipo_intervencion="Intervención individual",  # O el tipo que desees
                    fecha=fechaInter,
                    motivoIn=f"Intervención generada por diagnóstico: {diagnostico.diagnostico}",
                    detalles=detalleInter,
                )

        return redirect("gestionDiagnostico")

@never_cache
@login_required
def edicionDiagnostico(request, id_diagnostico):
    diagnostico = get_object_or_404(Diagnostico, pk=id_diagnostico)
    estudiantes = Estudiantes.objects.all()
    trastornos = Trastorno.objects.all()
    
    return render(request, "edicionDiagnostico.html", {
        "diagnostico": diagnostico,
        "estudiantes": estudiantes,
        "trastornos": trastornos
    })

@never_cache
@login_required
def editarDiagnostico(request):
    if request.method == "POST":
        id_diagnostico = request.POST["txtId"]
        id_estudiante = request.POST["id_estudiante"]
        id_trastorno = request.POST.get("id_trastorno")  # Si agregaste trastornos
        fechaInter = request.POST.get("fechaInter")
        
        diagnostico = get_object_or_404(Diagnostico, pk=id_diagnostico)
        estudiante = get_object_or_404(Estudiantes, pk=id_estudiante)
        
        diagnostico.diagnostico = request.POST["txtDiagnostico"]
        diagnostico.nivel = request.POST["txtNivel"]
        diagnostico.requiereInter = request.POST["requiereInter"]
        diagnostico.fechaInter = fechaInter if fechaInter else None
        diagnostico.detalleInter = request.POST["detalleInter"]
        diagnostico.id_estudiante = estudiante  # Asignar el estudiante
        diagnostico.observaciones = request.POST["txtObservaciones"]

        
        if id_trastorno:  # Si tienes trastornos en Diagnóstico
            trastorno = get_object_or_404(Trastorno, pk=id_trastorno)
            diagnostico.trastorno = trastorno  # Asignar el trastorno

        diagnostico.save()

        messages.success(request, "¡Diagnóstico actualizado!")
        return redirect("gestionDiagnostico")

@never_cache
@login_required
def eliminarDiagnostico(request, id_diagnostico):
    diagnostico = get_object_or_404(Diagnostico, pk=id_diagnostico)
    diagnostico.delete()

    messages.success(request, '¡Diagnóstico eliminado!')
    return redirect("gestionDiagnostico")

#----------

@never_cache
@login_required
def historias_estudiante_api(request):
    estudiante_id = request.GET.get('estudiante_id')
    if not estudiante_id:
        return JsonResponse({'historias': []})

    historias = HistoriaClinica.objects.filter(id_estudiante__id=estudiante_id).values('id_historia', 'fecha_creacion')
    historias_list = list(historias)
    return JsonResponse({'historias': historias_list})


@never_cache
@login_required
def gestionHistoriaClinica(request):
    estudiantes = Estudiantes.objects.all()
    diagnosticos = Diagnostico.objects.all()
    historias_clinicas = HistoriaClinica.objects.all()
    trastornos = Trastorno.objects.all()
    

    return render(request, "gestionHistoriaClinica.html", {
        "estudiantes": estudiantes,
        "diagnosticos": diagnosticos,
        "historias_clinicas": historias_clinicas,
        'trastornos': trastornos
        
    })

@login_required
@never_cache
def registrarHistoriaClinica(request):
    if request.method == "POST":
        id_estudiante = request.POST["id_estudiante"]
        id_diagnostico = request.POST["id_diagnostico"]
        observaciones = request.POST["observaciones"]
        PIAR = request.POST.get("PIAR", "")
        detalles_PIAR = request.POST["detalles_PIAR"]
        fecha_str = request.POST["fecha_creacion"]

        # Convertir el string en datetime
        fecha_creacion = parse_datetime(fecha_str)

        estudiante = get_object_or_404(Estudiantes, id_estudiante=id_estudiante)
        diagnostico = get_object_or_404(Diagnostico, id_diagnostico=id_diagnostico)

        HistoriaClinica.objects.create(
            id_estudiante=estudiante,
            id_diagnostico=diagnostico,
            observaciones=observaciones,
            PIAR=PIAR,
            detalles_PIAR=detalles_PIAR,
            fecha_creacion=fecha_creacion 
        )

        messages.success(request, "Historia clínica registrada correctamente")
        return redirect("gestionHistoriaClinica")


@never_cache
@login_required
def edicionHistoriaClinica(request, id_historia):
    historia = get_object_or_404(HistoriaClinica, id_historia=id_historia)
    estudiantes = Estudiantes.objects.all()
    diagnosticos = Diagnostico.objects.all()
    return render(request, "edicionHistoriaClinica.html", {
        "historia": historia,
        "estudiantes": estudiantes,
        "diagnosticos": diagnosticos
    })

@never_cache
@login_required
def editarHistoriaClinica(request):
    if request.method == "POST":
        id_historia = request.POST.get("id_historia")
        historia = get_object_or_404(HistoriaClinica, id_historia=id_historia)

        id_estudiante = request.POST.get("id_estudiante")
        id_diagnostico = request.POST.get("id_diagnostico")
        observaciones = request.POST.get("observaciones", "")
        PIAR = request.POST.get("PIAR", "")
        detalles_PIAR = request.POST.get("detalles_PIAR")

        historia.id_estudiante = get_object_or_404(Estudiantes, id_estudiante=id_estudiante)
        historia.id_diagnostico = get_object_or_404(Diagnostico, id_diagnostico=id_diagnostico)
        historia.observaciones = observaciones
        historia.PIAR = PIAR
        historia.detalles_PIAR = detalles_PIAR
        historia.save()

        messages.success(request, "Historia clínica actualizada correctamente")
        return redirect("gestionHistoriaClinica")

@never_cache
@login_required
def eliminarHistoriaClinica(request, id_historia):
    historia = get_object_or_404(HistoriaClinica, id_historia=id_historia)
    historia.delete()
    messages.success(request, "Historia clínica eliminada correctamente")
    return redirect("gestionHistoriaClinica")

#--------------------

#--------------

@never_cache
@login_required
def gestionCitas(request):
    citas = Cita.objects.all()
    estudiantes = Estudiantes.objects.all()
    return render(request, "gestionCitas.html", {"citas": citas, "estudiantes": estudiantes})

@never_cache
@login_required
def registrarCita(request):
    if request.method == "POST":
        id_estudiante = request.POST["id_estudiante"]
        fecha = request.POST["fecha"]
        motivo = request.POST["motivo"]
         

        estudiante = get_object_or_404(Estudiantes, id_estudiante=id_estudiante)

        Cita.objects.create(
            id_estudiante=estudiante,
            fecha=fecha,
            motivo=motivo
        )

        messages.success(request, "Cita registrada correctamente")
        return redirect("gestionCitas")

@never_cache
@login_required
def edicionCita(request, id_cita):
    cita = get_object_or_404(Cita, id_cita=id_cita)
    estudiantes = Estudiantes.objects.all()
    return render(request, "edicionCita.html", {
        "cita": cita,
        "estudiantes": estudiantes
    })

@never_cache
@login_required
def editarCita(request):
    if request.method == "POST":
        id_cita = request.POST["id_cita"]
        cita = get_object_or_404(Cita, id_cita=id_cita)

        id_estudiante = request.POST["id_estudiante"]
        fecha = request.POST["fecha"]
        motivo = request.POST["motivo"] 

        cita.id_estudiante = get_object_or_404(Estudiantes, id_estudiante=id_estudiante)
        cita.fecha = fecha
        cita.motivo = motivo 
        cita.save()

        messages.success(request, "Cita actualizada correctamente")
        return redirect("gestionCitas")

@never_cache
@login_required
def eliminarCita(request, id_cita):
    cita = get_object_or_404(Cita, id_cita=id_cita)
    cita.delete()
    messages.success(request, "Cita eliminada correctamente")
    return redirect("gestionCitas")


@never_cache
@login_required

def observaciones_cita(request, id_cita):
    cita = get_object_or_404(Cita, id_cita=id_cita)

    if request.method == 'POST':
        contenido = request.POST.get('observacion')
        resumen = request.POST.get('resumen')
        obs_id = request.POST.get('obs_id')  # Para identificar si es edición

        if obs_id:
            observacion = get_object_or_404(Observacion, id=obs_id)
            observacion.contenido = contenido
            observacion.resumen = resumen
            observacion.save()
        elif contenido:
            Observacion.objects.create(cita=cita, contenido=contenido, resumen=resumen,)
        
         # Guardar el resumen si se ha enviado
        if resumen:
            cita.resumen = resumen
            cita.save()

        return redirect('observaciones_cita', id_cita=id_cita)

    observaciones = Observacion.objects.filter(cita=cita).order_by('-fecha_creacion')

    return render(request, 'observaciones_cita.html', {
        'cita': cita,
        'observaciones': observaciones
    })

@never_cache
@login_required

def eliminar_observacion(request, id_observacion):
    observacion = get_object_or_404(Observacion, id=id_observacion)
    id_cita = observacion.cita.id_cita
    observacion.delete()
    return redirect('observaciones_cita', id_cita=id_cita)
#generar pdf

def generar_pdf_observaciones(request, id_cita):
    cita = get_object_or_404(Cita, id_cita=id_cita)
    observaciones = Observacion.objects.filter(cita=cita).order_by('fecha_creacion')

    template_path = 'pdf_observaciones.html'
    context = {'cita': cita, 'observaciones': observaciones}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cita_{cita.id_cita}_observaciones.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

#--------------

@never_cache
@login_required
def gestionIntervenciones(request):
    estudiantes = Estudiantes.objects.all()
    tipo_intervencion = Intervencion.TIPOS  # <-- usa todos los tipos del modelo
    historias_estudiante = []
    estudiante_id = request.GET.get('estudiante_id')
    if estudiante_id:
        historias_estudiante = HistoriaClinica.objects.filter(id_estudiante=estudiante_id)
    intervenciones = Intervencion.objects.all()
    return render(request, 'gestionIntervenciones.html', {
        'estudiantes': estudiantes,
        'tipo_intervencion': tipo_intervencion,
        'historias_estudiante': historias_estudiante,
        'intervenciones': intervenciones,
    })

@never_cache
@login_required
def registrarIntervencion(request):
    if request.method == "POST":
        try:
            required_fields = ['id_historia', 'tipo_intervencion', 'fecha', 'motivoIn', 'detalles']
            if not all(field in request.POST and request.POST[field] for field in required_fields):
                messages.error(request, "Faltan campos requeridos")
                request.session["form_error"] = True
                return redirect("gestionIntervenciones")

            historia = get_object_or_404(HistoriaClinica, id_historia=request.POST["id_historia"])

            Intervencion.objects.create(
                id_historia=historia,
                tipo_intervencion=request.POST["tipo_intervencion"],
                fecha=request.POST["fecha"],
                motivoIn=request.POST["motivoIn"],
                detalles=request.POST["detalles"]
            )

            messages.success(request, "Intervención registrada correctamente")
            return redirect("gestionIntervenciones")

        except Exception as e:
            messages.error(request, f"Error al registrar intervención: {str(e)}")
            request.session["form_error"] = True
            return redirect('gestionIntervenciones')

@never_cache
@login_required
def edicionIntervencion(request, id_intervencion):
    intervencion = get_object_or_404(Intervencion, id_intervencion=id_intervencion)
    historias = HistoriaClinica.objects.all()
    tipo_intervencion = Intervencion.TIPOS  # <-- Esto es clave

    return render(request, 'edicionIntervencion.html', {
        'intervencion': intervencion,
        'historias': historias,
        'tipo_intervencion': tipo_intervencion,
    })

@never_cache
@login_required
def editarIntervencion(request, id_intervencion):
    intervencion = get_object_or_404(Intervencion, id_intervencion=id_intervencion)

    estudiantes = Estudiantes.objects.all()
    historias_estudiante = HistoriaClinica.objects.filter(id_estudiante=intervencion.id_historia.id_estudiante)

    if request.method == 'POST':
        print(request.POST)  # Ver qué datos lleganpara q

        historia_id = request.POST['id_historia']
        tipo_intervencion = request.POST['tipo_intervencion']
        fecha = request.POST['fecha']
        motivoIn = request.POST['motivoIn']
        detalles = request.POST['detalles']

        # Guardar cambios
        intervencion.id_historia_id = historia_id
        intervencion.tipo_intervencion = tipo_intervencion
        intervencion.fecha = fecha
        intervencion.motivoIn = motivoIn
        intervencion.detalles = detalles
        intervencion.save()

        return redirect('gestionIntervenciones')  # Redirigir tras guardar

    return render(request, 'editarIntervencion.html', {'intervencion': intervencion})

@never_cache
@login_required
def eliminarIntervencion(request, id_intervencion):
    intervencion = get_object_or_404(Intervencion, id_intervencion=id_intervencion)
    intervencion.delete()
    messages.success(request, "Intervención eliminada correctamente")
    return redirect("gestionIntervenciones")

#--------------
@never_cache
@login_required
def detalle_estudiante(request, id_estudiante):
    estudiante = get_object_or_404(Estudiantes, id_estudiante=id_estudiante)
    historia_clinica = HistoriaClinica.objects.filter(id_estudiante=estudiante).first()
    citas = Cita.objects.filter(id_estudiante=estudiante)
    intervenciones = Intervencion.objects.filter(id_historia=historia_clinica) if historia_clinica else []

    context = {
        'estudiante': estudiante,
        'historia_clinica': historia_clinica,
        'citas': citas,
        'intervenciones': intervenciones,
    }
    return render(request, 'detalleEstudiante.html', context)

#------
@never_cache
@login_required
def gestionTrastornos(request):
    trastornos = Trastorno.objects.all()  # Obtener todos los trastornos
    return render(request, 'gestionTrastornos.html', {'trastornos': trastornos})

@never_cache
@login_required 
def registrarTrastorno(request):
    if request.method == "POST":
        nombre = request.POST["txtNombre"]
        descripcion = request.POST.get("txtDescripcion", "")

        # Verificar si el trastorno ya existe
        if Trastorno.objects.filter(nombre=nombre).exists():
            messages.error(request, '¡El trastorno ya está registrado!')
            return redirect('/gestionTrastornos/')  # Asegúrate de redirigir a la vista correcta

        # Si no existe, lo creamos
        Trastorno.objects.create(nombre=nombre, descripcion=descripcion)
        messages.success(request, '¡Trastorno registrado!')
        return redirect('/gestionTrastornos/')

@never_cache
@login_required
def edicionTrastorno(request, id_trastorno):
    trastorno = get_object_or_404(Trastorno, id_trastorno=id_trastorno)
    return render(request, "edicionTrastorno.html", {"trastorno": trastorno})

@never_cache
@login_required
def editarTrastorno(request):
    if request.method == "POST":
        id_trastorno = request.POST.get["txtId"]
        nombre = request.POST["txtNombre"]
        descripcion = request.POST.get("txtDescripcion", "")
        
        trastorno = get_object_or_404(Trastorno, id_trastorno=id_trastorno)
        trastorno.nombre = nombre
        trastorno.descripcion = descripcion
        trastorno.save()
        
        messages.success(request, '¡Trastorno actualizado!')
        return redirect('/')

@never_cache
@login_required
def eliminarTrastorno(request, id_trastorno):
    trastorno = get_object_or_404(Trastorno, id_trastorno=id_trastorno)
    trastorno.delete()
    messages.success(request, '¡Trastorno eliminado!')
    return redirect('/')

@never_cache
@login_required
def generar_pdf_historia(request, id_historia):
    historia = get_object_or_404(HistoriaClinica, id_historia=id_historia)
    template = get_template('historia_clinica_pdf.html')
    html = template.render({'historia': historia})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historia_{historia.id_historia}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

@never_cache
@login_required
def historias_por_estudiante(request):
    estudiante_id = request.GET.get('estudiante_id')
    historias = []
    if estudiante_id:
        historias_qs = HistoriaClinica.objects.filter(id_estudiante__id=estudiante_id)
        historias = [
            {"id": h.id_historia, "texto": f"HC-{h.id_historia}"}
            for h in historias_qs
        ]
    return JsonResponse({"historias": historias})

@never_cache
@login_required
def api_historias_estudiante(request):
    estudiante_id = request.GET.get('estudiante_id')
    historias = []
    if estudiante_id:
        historias_qs = HistoriaClinica.objects.filter(id_estudiante=estudiante_id)
        historias = [
            {
                'id_historia': h.id_historia,
                'fecha_creacion': h.fecha_creacion.isoformat(),
            }
            for h in historias_qs
        ]
    return JsonResponse({'historias': historias})

@never_cache
@login_required
def crearPlanTratamiento(request, id_diagnostico):
    diagnostico = get_object_or_404(Diagnostico, pk=id_diagnostico)
    historia = HistoriaClinica.objects.filter(id_diagnostico=diagnostico).first()
    if request.method == "POST":
        objetivo = request.POST.get("objetivo")
        detalles = request.POST.get("detalles")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_revision = request.POST.get("fecha_revision")
        frecuencia = request.POST.get("frecuencia")
        PlanTratamiento.objects.create(
            id_historia=historia,
            objetivo=objetivo,
            detalles=detalles,
            fecha_inicio=fecha_inicio,
            fecha_revision=fecha_revision,
            frecuencia=frecuencia
        )
        messages.success(request, "Plan de tratamiento creado correctamente.")
        return redirect("gestionDiagnostico")
    return render(request, "crearPlanTratamiento.html", {
        "diagnostico": diagnostico,
        "historia": historia
    })

@never_cache
@login_required
def detallePlanTratamiento(request, id_plan):
    plan = get_object_or_404(PlanTratamiento, pk=id_plan)
    seguimientos = plan.seguimientos.order_by('-fecha') if hasattr(plan, 'seguimientos') else []
    if request.method == "POST":
        avance = request.POST.get("avance")
        observaciones = request.POST.get("observaciones")
        if avance:
            SeguimientoPlan.objects.create(plan=plan, avance=avance, observaciones=observaciones)
            messages.success(request, "Seguimiento agregado.")
            return redirect('detallePlanTratamiento', id_plan=id_plan)
    return render(request, "detallePlanTratamiento.html", {
        "plan": plan,
        "seguimientos": seguimientos
    })

from django.shortcuts import redirect
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os
import pickle

def agendar_cita_google(request):
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    creds = None

    # Intenta cargar credenciales almacenadas localmente
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Si no hay credenciales válidas, inicia el flujo de autenticación
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # Guarda las credenciales para la próxima vez
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Datos de la cita (puedes personalizarlos)
    evento = {
        'summary': 'Cita en Psicología COSFA',
        'description': 'Acompañamiento emocional',
        'start': {
            'dateTime': '2025-06-01T10:00:00-05:00',
            'timeZone': 'America/Bogota',
        },
        'end': {
            'dateTime': '2025-06-01T11:00:00-05:00',
            'timeZone': 'America/Bogota',
        },
    }

    evento = service.events().insert(calendarId='primary', body=evento).execute()
    return redirect(evento.get('htmlLink'))  # Te envía al enlace del evento creado

