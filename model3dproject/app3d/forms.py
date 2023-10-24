from django import forms
from .models import Model3d

class Model3dForm(forms.ModelForm):
    class Meta:
        model = Model3d
        fields = ['title', 'description', 'image']