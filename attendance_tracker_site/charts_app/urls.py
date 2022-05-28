#from django.contrib import admin


from django.urls import path
from . import views

#from charts_app import views

app_name = 'charts_app'

urlpatterns = [
    path('', views.pie_chart, name='pie-chart'),
]