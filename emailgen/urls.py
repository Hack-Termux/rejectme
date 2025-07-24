from django.urls import path
from . import views

urlpatterns = [
    path('', views.email_form, name='email_form'),
    path('generate-email/', views.email_form, name='generate_email'),  # this can reuse the same view
    path('job-application/', views.job_application, name='job_application'),
]
