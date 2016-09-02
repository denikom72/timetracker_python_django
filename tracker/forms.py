from django import forms
from .models import CheckInCheckOut

class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = CheckInCheckOut
        fields = ['check_in_time', 'check_out_time']
        widgets = {
            'check_in_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'check_out_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class NewTimeEntryForm(forms.ModelForm):
    class Meta:
        model = CheckInCheckOut
        fields = ['user', 'check_in_time', 'check_out_time']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'check_in_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'check_out_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
