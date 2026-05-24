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

此專案已準備好部署到 Render.com。請依照以下設定進行：

### 1. 專案檔案

專案根目錄必須包含：

- `Procfile`：啟動指令 `gunicorn my_tennis_club.wsgi:application --bind 0.0.0.0:$PORT`
- `requirements.txt`：Django、gunicorn、whitenoise、dj-database-url、psycopg2-binary
- `runtime.txt`：指定 Python 版本 `python-3.11.15`
- `.python-version`：指定 Python 版本 `3.11.15`
- `render.yaml`：讓 Render 使用正確的 build command 和 Python 版本

### 2. Django 設定

`my_tennis_club/settings.py` 已支援：

- `DJANGO_SECRET_KEY`
- `DEBUG`（建議 production 設為 `False`）
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_URL`
- 靜態檔案設定：
  - `STATIC_URL = '/static/'`
  - `STATIC_ROOT = BASE_DIR / 'staticfiles'`
  - `STATICFILES_DIRS = [BASE_DIR / 'static']`
  - `WHITENOISE_USE_FINDERS = True`
  - `STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'`

### 3. Render 服務設定

在 Render Dashboard 的服務設定中：

- 選擇 branch：`bs`
- 指定 Python 版本：`3.11.15`
- Build Command：
  - `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Start Command：
  - `gunicorn my_tennis_club.wsgi:application --bind 0.0.0.0:$PORT`

### 4. 建議環境變數

- `DJANGO_SECRET_KEY`：安全金鑰
- `DEBUG`：`False`
- `DJANGO_ALLOWED_HOSTS`：例如 `*` 或 Render 提供的域名
- `DATABASE_URL`：如果使用 Render Postgres，請設定資料庫連線字串

### 5. 常見問題

- 如果出現 `404` 的靜態檔案錯誤，通常是因為 `collectstatic` 沒有成功執行。
- 如果樣式表回傳 `text/html`，表示 CSS 請求被 404 頁面取代。
- `render.yaml` 已經協助 Render 正確執行 build 並收集靜態檔案。

> 注意：本專案本地端預設使用 SQLite，若要在 Render 使用正式資料庫，請改用 `DATABASE_URL` 指定的 Postgres。