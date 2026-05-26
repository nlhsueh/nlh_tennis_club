# version img

前一版本：validation

資料庫的欄位可以存放影像檔。透過 admin 的介面，我們為每一個球場 (court) 加上照片。在觀看球場細部的時候，將之呈現。

[/courts/models.py](/courts/models.py)
* `Court` 的類別，加上 `photo` 的欄位，用來儲存照片。欄位的型態是 ImageField
* 透過 `upload_to` 來指定要上傳的目的地路徑。這裡路徑我們寫 `court_photos/`，是相對路徑，相對於 `setting` 中所設定的 `MEDIA_URL` 路徑。

Fix bug: [/courts/views.py](/courts/views.py)
* courts() 的第一行，要取得所有的球場，將 `courts = Court.objects.all.values()` 改為 `courts = Court.objects.all()`。修改後傳過去的 courts 才是一個完整物件的集合。

[/my_tennis_club/settings.py](/my_tennis_club/settings.py)
* 新增 `MEDIA_URL` 及 `MEDIA_ROOT` 的路徑-- 這是所有上傳的檔案的根目錄。
    * [/my_tennis_club/urls.py](/my_tennis_club/urls.py) 需要新增 `urlpatterns: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`。因為會用到 `static` 和 `setting`, 所以也要記得做 `import`。

[/courts/admin.py](/courts/admin.py) 
* `list_display` 加上 `photo`, 以便在 admin 中呈現

[/courts/templates/all_courts.html](/courts/templates/all_courts.html) 
* 改用 bootstrap table 的方式呈現球場列表
* `courttype` 如果直接印出，會印出他的 key ("G"), 我們想印出的是有意義的 value ("草地")，因此用 `{{ c.get_courttype_display }}`。 `get_xxx_display` 會印出 `xxx` 的 value。

[/courts/templates/court_details.html](/courts/templates/court_details.html) 印出球場的細節，這裡我們印出他的照片。用 bootstrap 的 `card` 元件來做輸出美化。

---

## 🏋️ 課堂練習

### 練習一：為會員（Member）新增「個人大頭貼 (avatar)」欄位

**目標**：模仿球場照片的作法，為俱樂部的會員加上個人頭像，並在會員列表或細節頁面中顯示。

**提示**：
1. **修改 Model**：在 [/members/models.py](/members/models.py) 的 `Member` 類別中新增一個 `avatar` 欄位：
   ```python
   avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
   ```
2. **資料庫遷移**：在終端機中執行：
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **註冊 Admin**：在 [/members/admin.py](/members/admin.py) 中，將 `avatar` 欄位加入 `list_display`，使管理員能在後台直接上傳與檢視頭像。
4. **前端渲染**：在 [/members/templates/details.html](/members/templates/details.html) 中加入頭像顯示：
   ```html
   {% if mymember.avatar %}
     <img src="{{ mymember.avatar.url }}" width="150px" style="border-radius: 50%;">
   {% else %}
     <span>（暫無頭像）</span>
   {% endif %}
   ```

---

### 練習二：為沒有上傳照片的球場設定「預設圖片 (Default Placeholder)」

**目標**：目前如果球場沒有上傳照片，頁面會顯示 `📷 暫無球場照片` 文字。請練習改為使用一張預設的網球場圖片作為 placeholder，使版面在沒有照片時依然美觀。

**提示**：
1. 在 [/static/img/](/static/img/) 目錄下放一張預設的球場圖片（例如命名為 `default_court.jpeg`）。
2. 在 [/courts/templates/court_details.html](/courts/templates/court_details.html) 中，利用 `{% static 'img/default_court.jpeg' %}` 來替換掉 `{% else %}` 中的純文字區塊：
   ```html
   {% load static %}
   ...
   {% if court.photo %}
     <img src="{{ court.photo.url }}" class="card-img-top court-detail-img" alt="{{ court.courtname }}">
   {% else %}
     <img src="{% static 'img/default_court.jpeg' %}" class="card-img-top court-detail-img" alt="Default Court">
   {% endif %}
   ```
3. 測試在後台新增一個沒有上傳圖片的球場，確認在詳情頁中能正確顯示這張預設圖片！

