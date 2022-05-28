from django.db import models
#Structure or details of what info classes, Timetables, Students and Attendance have
# Entered only two departments for demo purpose 
class Dept(models.TextChoices):
        ECE = 'ECE'
        CSE = 'CSE'
        
class Classes(models.Model):
    teacher_name = models.CharField(max_length=200)
    subject_title = models.CharField(max_length=200)
    departement = models.CharField(max_length=20, choices=Dept.choices, default=Dept.CSE)

    def __str__(self):
        return self.subject_title
    class Meta:
        verbose_name_plural = 'Classes'

class TimeTable(models.Model):
    class Day(models.TextChoices):
        MON = 'Monday'
        TUE = 'Tuesday'
        WED = 'Wednesday'
        THU = 'Thursday'
        FRI = 'Friday'
        SAT = 'Saturday'
        SUN = 'Sunday'

    start_time = models.TimeField()
    end_time = models.TimeField()
    departement = models.CharField(max_length=20, choices=Dept.choices, default=Dept.CSE)
    subject = models.ForeignKey(
        Classes, blank=True, null=True, on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices=Day.choices, default=Day.MON)

    def __str__(self):
        return self.day

class Student(models.Model):
    student_name = models.CharField(max_length=200)
    student_roll_no = models.CharField(max_length=10)
    student_image = models.ImageField()
    pub_date = models.DateTimeField('date published')
    departement = models.CharField(max_length=20, choices=Dept.choices, default=Dept.CSE)

    def __str__(self):
        return self.student_name


class Attendance(models.Model):
    subject = models.ForeignKey(
        Classes, blank=True, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateField()



