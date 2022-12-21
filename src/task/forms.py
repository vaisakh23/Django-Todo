from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control custom-input', 'placeholder': 'New task...'}))
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['user']
