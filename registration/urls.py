from django.urls import path
from . import views  # ✅ single, consistent import

urlpatterns = [
    path('', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('scanner/', views.qr_scanner, name='scanner'),
    path('check-in/<str:code>/', views.qr_checkin, name='qr_checkin'),
    path('checkin/<str:code>/', views.checkin, name='checkin'),
    path('export/', views.export_csv, name='export'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

