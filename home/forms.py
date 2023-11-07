from django import forms
from .models import filedata

class Fileform(forms.ModelForm):
    class Meta:
        model = filedata
        fields = ('File_type','Title','File_description','File')