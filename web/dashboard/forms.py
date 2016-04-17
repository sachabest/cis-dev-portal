from django import forms

class UploaderForm(forms.Form):
    student_list = forms.FileField(label="Student List")
    project_list = forms.FileField(label="Project List")