from django import forms
from django.contrib.auth.models import User

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

