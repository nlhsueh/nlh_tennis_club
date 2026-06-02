# version img.ex

前一版本：`img`

---

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

**💡 `img-ex` 參考解答說明**：
1. **資料欄位與遷移**：我們在 [/members/models.py](/members/models.py) 中為 `Member` 加上了 `avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)`，並已自動產生並套用了資料庫遷移。
2. **Admin 後台註冊**：我們已在 [/members/admin.py](/members/admin.py) 的 `list_display` 中加入 `"avatar"`，如此在後台管理系統即可以直接查看與上傳會員頭像。
3. **前端視覺美化呈現**：
   - **詳情頁**：在 [/members/templates/details.html](/members/templates/details.html) 中，我們以極具現代感的圓形相框顯示頭像 (Avatar)，當沒有上傳頭像時則顯示預設的 `👤` 符號。
   - **列表頁**：更進一步，我們在 [/members/templates/all_members.html](/members/templates/all_members.html) 的列表項目中，在名字左側加入了精緻的迷你圓形頭像縮圖，大幅提升會員列表的視覺層次！

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

**💡 `img-ex` 參考解答說明**：
1. **提供預設圖片**：我們已將一張經典網球場照片 [default_court.jpeg](file:///Users/nlh/mini24-tools/nlh_tennis_club/static/img/default_court.jpeg) 放入靜態目錄 [/static/img/](/static/img/) 底下。
2. **詳情頁面渲染**：在 [/courts/templates/court_details.html](/courts/templates/court_details.html) 中載入了 `{% load static %}`，並於 `{% else %}` 區塊中使用該預設圖案，取代原本的純文字提示，讓卡片元件在無自訂圖片時依然保持一致的版面與高質感。
3. **列表頁面同步美化**：我們也一併更新了 [/courts/templates/all_courts.html](/courts/templates/all_courts.html) 的球場表格，當某個球場無自訂照片時，表格中亦會顯示這張預設的迷你球場縮圖，使整個球場資料列表的視覺風格一致。

