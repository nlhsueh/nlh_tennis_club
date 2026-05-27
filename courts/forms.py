from django import forms
from courts.models import Booking
from django.forms import SelectDateWidget, ValidationError
from datetime import date, timedelta

class BookingForm(forms.ModelForm):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': '請輸入預約原因（至少 10 個字，此為必填欄位）',
            'rows': 3,
        }),
        required=True,
        label='用途'
    )

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
        }

        labels = {
            'user': '使用者',
            'court': '球場',
            'date': '預約日期',
        }

    def clean_reason(self):
        print ('clean_reason is called')
        reason = self.cleaned_data.get('reason')
        if not reason:
            raise ValidationError('預約原因不能為空。')
        if len(reason) <= 10:
            raise ValidationError(f'用途必須超過 10 個字元（至少 11 字）。目前只有 {len(reason)} 個字')
        
        # 練習題一：過濾敏感或測試字詞
        forbidden_words = ['test', 'demo', '測試', '範例']
        reason_lower = reason.lower()
        for word in forbidden_words:
            if word in reason_lower:
                raise ValidationError(f'預約原因不能包含測試或範例字詞（如 {word}）。')
        return reason        

    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        if booking_date:
            # 練習題二：限制只能預約 30 天以內的日期
            max_date = date.today() + timedelta(days=30)
            if booking_date > max_date:
                raise ValidationError(f'預約日期最多只能是自今天起算 30 天以內的日期（最晚為 {max_date}）。目前您選擇了 {booking_date}。')
        return booking_date