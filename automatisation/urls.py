from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export-results/', views.export_results, name='export_results'),
    path('alert-configuration/', views.alert_configuration, name='alert_configuration'),
    path('home/', views.home_redirect, name='home'),
    path('admin/', admin.site.urls),  # URLs de l'admin
]
