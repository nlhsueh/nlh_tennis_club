# version bind_user

前一版本：img

[/members/models.py](/members/models.py)
* 加上 `user` 的外鍵
```python
user = models.OneToOneField(User, on_delete=models.CASCADE, default= None, blank=True, null=True)
```
* 因為一個 `user` 對應一個 `member`, 所以採用 `OneToOneField` 來建立 `user`。

[/members/views.py](/members/views.py)
* 把對應的 `member` 找出來傳過去，我們宣告了一個新的 function `getMember()`

[/members/templates/all_members.html](/members/templates/all_members.html)
* 把對應的 `user` 也印出來
* 這個版本也改用 bootstrap 來做 list 的呈現。 (`list-group`, `list-group-item`)

```html
      <ul class="list-group">
        {% for x in mymembers %}
          <li class="list-group-item  bg-transparent"><a href="details/{{ x.id }}">{{ x.lastname }}{{ x.firstname }}</a>, ({{ x.user }}) {{x.age}} 歲</li>
        {% endfor %}
      </ul>
```      

[/members/admin.py](/members/admin.py)
* 新增 `user` 的欄位

```python
  list_display = ("firstname", "lastname", "joined_date","age", "user")
```

[/courts/templates/my_bookings.html](/courts/templates/my_bookings.html)
* 前一版只印出 `user`, 這一版我們把 `member` 的姓名也印出來。所以在 [my_booking()](/courts/views.py) 中，`context` 加上 `member` 的資訊傳到 html。應用 `getMember()` 的函式來取得 member 物件。



