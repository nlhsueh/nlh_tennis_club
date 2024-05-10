from django import forms 
from .models import Member
from datetime import date
  
# a form for searching member by last name  
class CheckMemberForm(forms.Form):   
    # first_name = forms.CharField(max_length = 200) 
    last_name = forms.CharField(max_length = 200) 
    # phone = forms.IntegerField(help_text = "Enter 6 digit roll number") 
    # joined_date = forms.DateField(label='加入日期',
    #                               widget= forms.SelectDateWidget)
