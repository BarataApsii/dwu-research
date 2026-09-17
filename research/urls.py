from django.urls import path

from . import views

app_name = 'research'

urlpatterns = [
    path('', views.research, name='home'),
    path('doctor-of-philosophy/', views.doctor_of_philosophy, name='doctor-of-philosophy'),
    path('master-of-philosophy/', views.master_of_philosophy, name='master-of-philosophy'),
    path('master-of-research-methodology/', views.master_of_research_methodology, name='master-of-research-methodology'),
    path('master-of-research-methodology/apply/', views.mrm_application_form, name='mrm-apply'),
    path('doctor-of-education/', views.doctor_of_education, name='doctor-of-education'),
]
