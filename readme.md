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

## 部署到 Render.com

此專案已準備好部署到 Render.com。請依照以下步驟進行：

1. 在專案根目錄建立或確認以下檔案：
   - `Procfile`
   - `requirements.txt`
   - `runtime.txt`
   - `my_tennis_club/settings.py` 已支援透過 `DATABASE_URL`、`DJANGO_SECRET_KEY` 與 `DJANGO_ALLOWED_HOSTS` 設定環境變數。
2. 前往 Render.com，建立新的 Web Service，並選擇連接此 GitHub 儲存庫或手動上傳專案。
3. 在 Render 的服務設定中設定環境變數：
   - `DJANGO_SECRET_KEY`：請設定安全的秘密金鑰。
   - `DEBUG`：設定為 `False`。
   - `DJANGO_ALLOWED_HOSTS`：設定專案對應的域名，例如 `*` 或 Render 提供的子域名。
   - `DATABASE_URL`：如果使用 Render Postgres，請設定 Render 提供的資料庫連線字串。
4. Render 會自動安裝 `requirements.txt` 中的相依套件，並執行 `Procfile` 中的 `gunicorn my_tennis_club.wsgi --bind 0.0.0.0:$PORT`。
5. 部署完成後，Render 會自動執行建置；必要時可在 Build Command 中加入 `python manage.py collectstatic --noinput`。

> 注意：專案本地端預設使用 SQLite；如果在 Render 上使用正式資料庫，請務必改成使用 `DATABASE_URL` 指定的 Postgres。
