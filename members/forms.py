from django import forms 
from .models import Member
  
# creating a form  
class InputForm(forms.Form): 
  
    first_name = forms.CharField(max_length = 200) 
    last_name = forms.CharField(max_length = 200) 
    phone = forms.IntegerField(help_text = "Enter 6 digit roll number") 
    joined_date = forms.DateField()

class InputForm02(forms.ModelForm): 
    class Meta:
            model = Member
            fields = "__all__"