"""
URL configuration for psicologia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views



urlpatterns = [

    path('', views.pagina_principal, name='inicio'),
# Ruta login
    

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),



# Rutas de Estudiantes
    path('gestionEstudiantes/', views.home, name='gestionEstudiantes'),
    path('registrarEstudiante/', views.registrarEstudiante),
    path('edicionEstudiante/<id_estudiante>', views.edicionEstudiante),
    path('editarEstudiante/', views.editarEstudiante),
    path('eliminarEstudiante/<id_estudiante>', views.eliminarEstudiante),

 # Rutas de Diagnóstico
    
    path("gestionDiagnostico/", views.gestionDiagnostico, name="gestionDiagnostico"),
    path("registrarDiagnostico/", views.registrarDiagnostico),
    path("edicionDiagnostico/<str:id_diagnostico>/", views.edicionDiagnostico),
    path("editarDiagnostico/", views.editarDiagnostico),
    path("eliminarDiagnostico/<str:id_diagnostico>/", views.eliminarDiagnostico),

# Historia clínica

    path("gestionHistoriaClinica/", views.gestionHistoriaClinica, name="gestionHistoriaClinica"),
    path("registrarHistoriaClinica/", views.registrarHistoriaClinica),
    path("edicionHistoriaClinica/<int:id_historia>/", views.edicionHistoriaClinica),
    path("editarHistoriaClinica/", views.editarHistoriaClinica),
    path("eliminarHistoriaClinica/<int:id_historia>/", views.eliminarHistoriaClinica),
    path('historia/pdf/<int:id_historia>/', views.generar_pdf_historia, name='generar_pdf_historia'),

# Citas
    path("gestionCitas/", views.gestionCitas, name="gestionCitas"),
    path("registrarCita/", views.registrarCita),
    path("edicionCita/<int:id_cita>/", views.edicionCita),
    path("editarCita/", views.editarCita),
    path("eliminarCita/<int:id_cita>/", views.eliminarCita),
    path('observaciones/<int:id_cita>/', views.observaciones_cita, name='observaciones_cita'),
    path('observaciones/eliminar/<int:id_observacion>/', views.eliminar_observacion, name='eliminar_observacion'),
    path('cita/<int:id_cita>/pdf/', views.generar_pdf_observaciones, name='generar_pdf_observaciones'),


#Intervencion
    path("gestionIntervenciones/", views.gestionIntervenciones, name="gestionIntervenciones"),
    path("registrarIntervencion/", views.registrarIntervencion),
    path("edicionIntervencion/<int:id_intervencion>/", views.edicionIntervencion, name="edicionIntervencion"),
    path('editarIntervencion/<int:id_intervencion>/', views.editarIntervencion, name='editarIntervencion'),
    path("eliminarIntervencion/<int:id_intervencion>/", views.eliminarIntervencion),


#--------------------
    path('detalleEstudiante/<str:id_estudiante>/', views.detalle_estudiante, name='detalle_estudiante'),

#---------
# Trastornos
    path("gestionTrastornos/", views.gestionTrastornos, name="gestionTrastornos"),
    path("registrarTrastorno/", views.registrarTrastorno),
    path("edicionTrastorno/<int:id_trastorno>/", views.edicionTrastorno),
    path("editarTrastorno/<int:id_trastorno>/", views.editarTrastorno, name="editarTrastorno"),
    path("eliminarTrastorno/<int:id_trastorno>/", views.eliminarTrastorno),

#--------------------
    path('buscar/', views.busqueda_global, name='busquedaGlobal'),
    path('api/historias_estudiante/', views.api_historias_estudiante, name='api_historias_estudiante'),
    path('plantratamiento/nuevo/<int:id_diagnostico>/', views.crearPlanTratamiento, name='crearPlanTratamiento'),
    path('plantratamiento/<int:id_plan>/', views.detallePlanTratamiento, name='detallePlanTratamiento'),

]