from django import forms
from courts.models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        widget = {
            'user': forms.Select(attrs={'readonly': 'readonly'}),
        }
