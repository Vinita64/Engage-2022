# Generated by Django 3.2.13 on 2022-05-21 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_tracker', '0005_auto_20220521_0745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='classes',
        ),
        migrations.AddField(
            model_name='student',
            name='departement',
            field=models.CharField(choices=[('ECE', 'Ece'), ('CSE', 'Cse')], default='CSE', max_length=20),
        ),
        migrations.AddField(
            model_name='timetable',
            name='departement',
            field=models.CharField(choices=[('ECE', 'Ece'), ('CSE', 'Cse')], default='CSE', max_length=20),
        ),
    ]
