from django.contrib import admin

# Register your models here.
from .models import Student, Classes, TimeTable, Attendance


admin.site.register(Student)
admin.site.register(Classes)
admin.site.register(TimeTable)
admin.site.register(Attendance)
