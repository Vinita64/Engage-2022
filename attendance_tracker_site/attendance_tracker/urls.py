from django.urls import path

from . import views

app_name = 'attendance_tracker'


urlpatterns = [
    path('', views.index, name='index'),
    path('attendance_report', views.initial_attendance_report, name='show_attendance_report'),
    path('attendance_report/get_report', views.show_attendance_report, name='get_attendance_report'),
    path('attendance_report_mail',views.send_attendance_mail,name='send_attendance_mail'),
    path('attendance_report/by_dept', views.show_dept_attendance_report, name='show_dept_attendance_report'),
    path('update_attendance', views.update_attendance, name='update_attendance'),
   
]
