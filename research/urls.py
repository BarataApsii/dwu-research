from django.urls import path

from . import views

app_name = 'research'

urlpatterns = [
    path('', views.research, name='home'),
    path('doctor-of-philosophy/', views.doctor_of_philosophy, name='doctor-of-philosophy'),
    path('master-of-philosophy/', views.master_of_philosophy, name='master-of-philosophy'),
    path('master-of-research-methodology/', views.master_of_research_methodology, name='master-of-research-methodology'),
    path('master-of-research-methodology/apply/', views.mrm_application_form, name='mrm-apply'),
    path('master-of-philosophy/apply/', views.mphil_application_form, name='mphil-apply'),
    path('doctor-of-philosophy/apply/', views.phd_application_form, name='phd-apply'),
    path('doctor-of-education/', views.doctor_of_education, name='doctor-of-education'),
    path('dashboard/', views.coordinator_dashboard, name='coordinator-dashboard'),
    path('dashboard/export/', views.export_applications_csv, name='export-applications'),
    path('dashboard/applications/<int:pk>/', views.application_detail, name='application-detail'),
    path('dashboard/applications/<int:pk>/download/', views.download_application_documents, name='download-application-documents'),
    path('documents/<int:pk>/download/', views.document_download, name='download-document'),
]
