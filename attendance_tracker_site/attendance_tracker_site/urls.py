"""attendance_tracker_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Admin Login"
admin.site.site_title = "Attendance Tracking"
admin.site.index_title = "Login to access student data"

urlpatterns = [
    path('', include('student_management.urls')),
    path('charts_app/', include('charts_app.urls')),
    #path('charts_app/', views.pie_chart,name='pie-chart'),
    path('attendance_tracker/', include('attendance_tracker.urls')),
    path('admin/', admin.site.urls),
    
]
