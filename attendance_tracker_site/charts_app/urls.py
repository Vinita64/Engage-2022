#from django.contrib import admin


from django.urls import path
from . import views

#from charts_app import views

app_name = 'charts_app'
#urlpatterns = [
#	path('admin/', admin.site.urls),
#	path('', views.HomeView.as_view()),
#	# path('test-api', views.get_data),
#	path('api', views.ChartData.as_view()),
#]


urlpatterns = [
    path('', views.pie_chart, name='pie-chart'),
]