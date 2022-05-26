from django import forms

class AttendanceDateTrackerForm(forms.Form):
    date_from_field = forms.DateField()
    date_to_field = forms.DateField()