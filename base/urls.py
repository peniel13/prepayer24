from django.urls import path
from .import views

urlpatterns= [
    path('',views.index, name= 'index'),
    path('apropos/',views.apropos, name= 'apropos'),
    path('contact/', views.contact, name='contact'),
    path('station_list/', views.station_list, name='station_list'),
]