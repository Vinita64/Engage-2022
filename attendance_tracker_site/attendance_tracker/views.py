
from email.errors import StartBoundaryNotFoundDefect
import io
import base64
import traceback
import face_recognition
import datetime

from django.utils import timezone
from django.core.files.base import ContentFile
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from attendance_tracker.models import Student, TimeTable, Attendance,Classes
from django.db.models import Count

from django.core.mail import send_mail

THRESHOLD_ATTENDANCE_VALUE = 70

daysWeek = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']


def students_info(student_data):
    student_encoded = []
    student_names = []
    for student in student_data:
        loaded_image = face_recognition.load_image_file(
            student.student_image)
        encoded_image = face_recognition.face_encodings(loaded_image)[0]
        student_encoded.append(encoded_image)
        student_names.append(student.student_name)
    return [student_names, student_encoded]


def get_face_encoding_from_base64(data):
    format, imgstr = data.split(';base64,')
    image = face_recognition.load_image_file(
        io.BytesIO(base64.b64decode(imgstr)))
    image_encoding = face_recognition.face_encodings(image)[0]
    return image_encoding


def index(request):
    return render(request, "attendance_tracker/index.html")


def update_attendance(request):
    try:
        unknown_student_pic_encoding = get_face_encoding_from_base64(
            request.POST.get('student_pic'))
        students_data = Student.objects.all()
        student_names, known_students_image_encoded = students_info(
            student_data=students_data)
        results = face_recognition.compare_faces(
            known_students_image_encoded, unknown_student_pic_encoding)
        matched_results_index = [idx for idx,
                                 value in enumerate(results) if value]

        if len(matched_results_index) > 0:
            student = Student.objects.get(
                student_name=student_names[matched_results_index[0]])
            current_class = TimeTable.objects.filter(
                departement=student.departement).filter(day=daysWeek[timezone.now().weekday()]).filter(
                start_time__lte=timezone.now().time()).filter(end_time__gte=timezone.now().time())
            if(current_class.count() == 0):
                return render(request, "attendance_tracker/updated_attendance.html", {'student': student, 'class_not_found': 'Currently no classes'})
            else:
                current_class_obj = current_class.first()
                Attendance.objects.create(
                    student=student,
                    subject=current_class_obj.subject,
                    date=timezone.now().date()
                )
                return render(request, "attendance_tracker/updated_attendance.html", {'student': student, 'current_class': current_class_obj.subject.subject_title})
        else:
            return render(request, "attendance_tracker/updated_attendance.html", {'error': 'Not a student!'})

    except Exception as e:
        print(traceback.format_exc())
        return render(request, "attendance_tracker/updated_attendance.html", {'error': "Couldn't render anything!"})

def subject_count(date_from, date_to, number_of_classes_per_day):

    total_days = (date_to-date_from).days
    print("Total_days:",total_days)
    weeks = total_days//7
    print("Weeks:",weeks)
    days_of_week = {i: weeks for i in range(7)}
    if date_to.weekday() > date_from.weekday():
        end_date = date_to.weekday()
    else:
        end_date = date_to.weekday() + 7

    for i in range(date_from.weekday(), end_date + 1):
        print(i,days_of_week[i%7])
        days_of_week[i % 7] += 1
        print(i,days_of_week[i%7])
    total_count = 0
    for i in range(7):
        total_count = total_count + number_of_classes_per_day[i]*days_of_week[i]
    print("Total count:",total_count)
    return total_count

def initial_attendance_report(request):
    return render(request, "attendance_tracker/attendance_report.html", {'students_list': []})

def show_attendance_report(request):
    depts = ['CSE','ECE']
    student_list = []
    startDateStr = request.GET.get('startDate')
    if (startDateStr != None) and (startDateStr != ''):
        startDate = datetime.datetime.strptime(request.GET.get('startDate'),"%Y-%m-%d").date()
    else:
        startDate=datetime.date.today()
    endDateStr = request.GET.get('endDate')
    if (endDateStr != None) and (endDateStr != ''):
        endDate = datetime.datetime.strptime(request.GET.get('endDate'),"%Y-%m-%d").date()
    else:
        endDate = datetime.date.today()
    date_from = startDate
    date_to = endDate
    for dept in depts:
        print(dept)
        numC = [0,0,0,0,0,0,0]

        numC[0] = TimeTable.objects.filter(day='Monday').filter(departement=dept).count()
        numC[1] = TimeTable.objects.filter(day='Tuesday').filter(departement=dept).count()
        numC[2] = TimeTable.objects.filter(day='Wednesday').filter(departement=dept).count()
        numC[3] = TimeTable.objects.filter(day='Thursday').filter(departement=dept).count()
        numC[4] = TimeTable.objects.filter(day='Friday').filter(departement=dept).count()
        numC[5] = TimeTable.objects.filter(day='Saturday').filter(departement=dept).count()
        numC[6] = TimeTable.objects.filter(day='Sunday').filter(departement=dept).count()

        total_count = subject_count(date_from = date_from, date_to=date_to, number_of_classes_per_day=numC) 

        if (total_count == 0):
            return render(request, "attendance_tracker/attendance_report.html", {'no_relevant_classes': 'No classes for  dept'})
    
    
        for student in Student.objects.all():
        #attendance_count = Attendance.objects.filter(
        #    student=student).filter(date__month=timezone.now().month).count()
            if student.departement==dept:
                attendance_count = Attendance.objects.filter(
                    student=student).filter(date__month=timezone.now().month).count()
                attendance_percent =(attendance_count/total_count) * 100 
                if(attendance_percent < THRESHOLD_ATTENDANCE_VALUE):
                     student_list.append({ 'student_name' : student.student_name, 'attendance_percentage':attendance_percent  })
    return render(request, "attendance_tracker/attendance_report.html", {'students_list': student_list, 'startDate' : startDate, 'endDate' : endDate}) 



def show_dept_attendance_report(request):
    selected_dept = request.GET.get('selected_dept')
    startDateStr = request.GET.get('startDate')
    if (startDateStr != None) and (startDateStr != ''):
        startDate = datetime.datetime.strptime(request.GET.get('startDate'),"%Y-%m-%d").date()
    else:
        startDate=datetime.date.today()
    endDateStr = request.GET.get('endDate')
    if (endDateStr != None) and (endDateStr != ''):
        endDate = datetime.datetime.strptime(request.GET.get('endDate'),"%Y-%m-%d").date()
    else:
        endDate = datetime.date.today()
    print("startDate:",startDate," endDate:",endDate)
    
    students_list = Student.objects.filter(departement=selected_dept)
    subject_list = Classes.objects.filter(departement=selected_dept)
    
    #date_from = datetime.date(timezone.now().year, timezone.now().month, 1)
    #date_to = datetime.date(timezone.now().year,
    #                        timezone.now().month, timezone.now().day)
    date_from =startDate 
    date_to = endDate
    total_subject_classes = {}
    for subject in subject_list:
        total_count_subject_wise = [0,0,0,0,0,0,0]
        total_count_subject_wise[0] = TimeTable.objects.filter(day='Monday').filter(departement=selected_dept).filter(subject=subject).count()
        total_count_subject_wise[1] = TimeTable.objects.filter(day='Tuesday').filter(departement=selected_dept).filter(subject=subject).count()
        total_count_subject_wise[2] = TimeTable.objects.filter(day='Wednesday').filter(departement=selected_dept).filter(subject=subject).count()
        total_count_subject_wise[3] = TimeTable.objects.filter(day='Thursday').filter(departement=selected_dept).filter(subject=subject).count()
        total_count_subject_wise[4] = TimeTable.objects.filter(day='Friday').filter(departement=selected_dept).filter(subject=subject).count()
        total_count_subject_wise[5] = TimeTable.objects.filter(day='Saturday').filter(departement=selected_dept).filter(subject=subject).count()
        total_count_subject_wise[6] = TimeTable.objects.filter(day='Sunday').filter(departement=selected_dept).filter(subject=subject).count()
        print("Subject:",total_count_subject_wise)
        current_count = subject_count(date_from=date_from, date_to=date_to, number_of_classes_per_day=total_count_subject_wise)
        total_subject_classes[subject.subject_title] = current_count

    student_attendance = []
    for student in students_list:
        student_obj = {}
        student_obj['student_name'] = student.student_name
        student_obj['subject_list'] = []
        for subject in subject_list:
            if total_subject_classes[subject.subject_title] != 0:
                attendance = Attendance.objects.filter(student=student).filter(subject=subject).count()/total_subject_classes[subject.subject_title] * 100
                student_obj['subject_list'].append({'subject' : subject.subject_title , 'attendance': attendance})
        student_attendance.append(student_obj)
    return render(request, "attendance_tracker/dept_report.html", {'time_table_list': subject_list, 'student_list': student_attendance, 'selected_dept': selected_dept, 'startDate' : startDate , 'endDate' : endDate})

def send_attendance_mail(request):
    print("Came to send mail")
    subject = "Warning Low Attendance"  
    msg     = "Your attendance is less than 70 percent."  
    to      = 'vinita.wissenaire@gmail.com'  
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  
    if(res == 1):  
        msg = "Mail Sent Successfuly"  
    else:  
        msg = "Mail could not sent"  
    return HttpResponse(msg)  
   