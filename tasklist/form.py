"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from django import forms
from .models import Tasks

class TaskForm(forms.Form):
    task_title = forms.CharField(label='Title', max_length=30)
    task_description = forms.CharField(label='Description', max_length=255)

class TaskModelForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=20)
    description = forms.CharField(label='Description', max_length=255, widget = forms.Textarea)
    class Meta:
        model = Tasks
        fields = ['title', 'description']
    #def __init__(self, *args, **kwargs):
    #    super(TaskModelForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
    #    self.fields['description'].widget.attrs['maxlength'] = 255;
    #    self.fields['description'].widget=forms.Textarea()
