from django.db import models
import datetime

# Create your models here.
class Member(models.Model):
    firstname = models.CharField(max_length=255,
                                 verbose_name='名字')
    lastname = models.CharField(max_length=255,
                                verbose_name='姓')
    phone = models.IntegerField(null=True, 
                                blank=True,
                                verbose_name='電話')
    joined_date = models.DateField(null=True,
                                   blank=True,
                                   verbose_name='入會日期',
                                   default=datetime.date.today(),
                                   help_text='the day he pay fee',
                                   editable=True,
                                   )

    def __str__(self):
      return f"{self.firstname} {self.lastname}"  