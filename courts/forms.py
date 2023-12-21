from django import forms
from courts.models import Booking
from django.forms import SelectDateWidget, ValidationError
from datetime import date

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking     # 對應的資料

        # fields = '__all__'  # 呈現所有欄位
        # 也可以用 list 來表達要呈現的欄位
        fields = ['user', 'court', 'date', 'reason']

        widgets = {
            'user': forms.Select(attrs={'readonly': 'readonly'}),
            # 'user': forms.TextInput(                
            #     attrs={'readonly': 'readonly'}),    # 文字框
            'court': forms.Select(),                # 下拉式選單
            'date': SelectDateWidget(               
                attrs={'initial': date.today()}),   # 日期選單
            'reason': forms.Textarea(),                
        }

        labels = {
            'user': '使用者',
            'court': '球場',
            'date': '預約日期',
            'reason': '用途',
        }

    def clean_reason(self):
        print ('clean_reason is called')
        reason = self.cleaned_data.get('reason')
        if len(reason) <= 10:
            raise ValidationError(f'用途必須至少包含 10 個字元。目前只有 {len(reason)} 個字')
        return reason        