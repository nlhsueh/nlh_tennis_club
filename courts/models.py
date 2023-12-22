from django.db import models
# User
from django.contrib.auth.models import User
# timezone
from datetime import date

class Court(models.Model):  
    COURT_TYPE = [     # 使用 list 來做列舉
        ("G", "草地"),  # 第一個 "G" 表示真實儲存的資料，第二個表示呈現的字
        ("H", "硬地"),
        ("N", "泥地"),
        ("D", "地毯"),
    ]   
    courtname = models.CharField(max_length=100)
    courttype = models.CharField(max_length=1, choices=COURT_TYPE)
    ''' 列舉型態用 choices = 來設定 '''
    city = models.CharField(max_length=100)

    photo = models.ImageField(upload_to='court_photos/', null=True, blank=True)


    def __str__(self):
        return f"{self.city} {self.courtname}"  

'''
    預借場館的紀錄，包含誰借的，借哪一個場館及日期
'''

class Booking(models.Model):
    court = models.ForeignKey(Court, models.CASCADE)
    ''' models.CASCADE (層級刪除) 表示當某個 Court 被刪除時，
        與之相關的 Booking 也會跟著刪除
    '''
    user = models.ForeignKey(User, models.CASCADE)
    date = models.DateField(default = date.today())

    reason = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user}, {self.court}, {self.date}"

    class Meta:
        unique_together = ('court', 'date')    
        ''' 場館及日期的聯合必須是唯一的 '''