# version bind_user

前一版本：img

[/members/models.py](/members/models.py)
* 加上 user 的外鍵
```python
user = models.OneToOneField(User, on_delete=models.CASCADE, default= None, blank=True, null=True)
```

[/members/views.py](/members/views.py)
* 把對應的 

[/members/templates/all_members.html](/members/templates/all_members.html)
* 把對應的 user 也印出來


[/members/admin.py]()
* 新增 user 的欄位

[/courts/mybookings.html](/courts/mybookings.html)
* 要把 user 也印出來
* 



