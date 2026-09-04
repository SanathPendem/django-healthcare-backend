"""
URL Configuration for Healthcare Backend.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls', namespace='users')),
    path('api/patients/', include('patients.urls', namespace='patients')),
    path('api/doctors/', include('doctors.urls', namespace='doctors')),
    path('api/mappings/', include('mappings.urls', namespace='mappings')),
]
