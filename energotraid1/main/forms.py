from django import forms
from .models import *


# creating a form
class addCpForm(forms.ModelForm):
    class Meta:
        model = Сounterparty
        fields = '__all__'


class addContForm(forms.ModelForm):
    class Meta:
        model = Contract
        #fields = '__all__'
        fields = '__all__'

class addTuForm(forms.ModelForm):
    class Meta:
        model = Tu
        fields = '__all__'
        #fields=['uploaded_at','file']


class DocumentForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields=['file']
