# version bs

using bootstrap

[/members/templates/master.html](/members/templates/master.html)
* 加上匯入 bs 的指令
* 透過 `class="p-5 bg-primary text-white rounded"` 建立一個首頁的標示牆
* 透過 `class="container-fluid"` 做一個大頁面，裡面放一個列表，透過 `class=nav, nav-item, nav-link`
* 列表：HOME, ADMIN, login/logout, My-booking
* 透過 <footer> 製作一個頁尾。

[/members/templates/main.html](/members/templates/main.html)
* 透過 container 製作一個非滿版的容器; 透過 col-sm-3 放置四個圖片 (12/3=4)
* 再放一個 container 容器，裡面放一些文字。假設我們一列要有兩行，所以用 `col-md-6` (12/6=2)。

[/web/templates/login.html](/web/templates/login.html)
* 登入頁面 label 標記為 form-label

[/web/forms.py](/web/forms.py)
* username 和 password 也需要改成 form-control, 所以設定 widget 的 attrs
```
    username = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
```

