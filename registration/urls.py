from django.urls import path
from .views import register  # import the view you made
from .views import register, checkin
from .views import register, checkin, export_csv

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
