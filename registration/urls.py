from django.urls import path
from .views import register  # import the view you made
from .views import register, checkin
from .views import register, checkin, export_csv
from django.urls import path
from . import views

urlpatterns = [
    path('', register, name='register'),
    path('checkin/<str:code>/', checkin, name='checkin'),
    path('export/', export_csv, name='export'),
]


urlpatterns = [
    path('', register, name='register'),
    path('checkin/<str:code>/', checkin, name='checkin'),
]


urlpatterns = [
    path('', register, name='register'),
]




urlpatterns = [
    path('', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('scanner/', views.qr_scanner, name='scanner'),
    path('check-in/<str:code>/', views.qr_checkin, name='qr_checkin'),
]