from django.db import models

# Create your models here.
class Member(models.Model):
  GENDER_TYPE = [     
      ("M", "男性"),  
      ("F", "女性"),
  ]   

  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.IntegerField(null=True)
  joined_date = models.DateField(null=True)
  age = models.IntegerField(default=20)
  gender = models.CharField(null=True, max_length=10,
                            choices=GENDER_TYPE)

  def __str__(self):
    return f"{self.firstname} {self.lastname}"  