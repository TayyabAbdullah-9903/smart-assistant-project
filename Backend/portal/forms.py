from django import forms
from manuals.models import Manual

class ManualUploadForm(forms.ModelForm):
    class Meta:
        model = Manual
        fields = ["file"]
