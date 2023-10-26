from django import forms
from .models import Reg
class Regmodelform(forms.ModelForm):
    class Meta:
        model=Reg
        fields=['FirstName','LastName','UserName','Password','CPassword','EmailId','MobileNumber']
        widgets={'Password':forms.PasswordInput(),'CPassword':forms.PasswordInput()}
class Loginform(forms.Form):
    UserName=forms.CharField(max_length=10)
    Password=forms.CharField(max_length=10,widget=forms.PasswordInput())