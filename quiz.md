## Django MVT 基礎課堂隨堂測驗 — 多媒體欄位與上傳處理 (Quiz)

本測驗旨在檢驗學生對於本單元（`img` 分支：Django ImageField 模型欄位、MEDIA 檔案系統設定、URL 路由配置以託管上傳檔案、以及 QuerySet `all()` 與 `values()` 傳值差異）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 為了讓 Django 的 Model 能夠支援使用者上傳影像檔案（例如本單元的 `photo` 欄位），我們應選用哪一種模型欄位型態？此外，執行該欄位時 Python 環境中必須安裝哪一個第三方影像處理庫？
* (A) `models.FilePathField`，需要安裝 `Pillow`
* (B) `models.ImageField`，需要安裝 `Pillow`
* (C) `models.FileField`，需要安裝 `OpenCV`
* (D) `models.PictureField`，不需要安裝任何額外套件

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 在 Django 中，**`models.ImageField`** 是專用來儲存與驗證圖片檔案的欄位。
* 由於 Django 在後端需要對上傳圖片的格式、尺寸（寬與高）進行完整性檢查，因此在底層會調用 Python 影像處理函式庫 **`Pillow`**。如果您的環境中沒有安裝 `Pillow`，在執行資料庫遷移或啟動專案時，Django 會直接拋出編譯錯誤。
</details>

---

### 2. 當我們在 `models.py` 中寫下 `photo = models.ImageField(upload_to='court_photos/')` 時，參數 `upload_to` 的核心作用是什麼？
* (A) 指定使用者在網頁上傳圖片時，所能挑選的本地端資料夾。
* (B) 指定該圖片在資料庫中儲存的二進位二級檔案代碼。
* (C) 指定該上傳圖片檔案在伺服器端實體磁碟中的「儲存子目錄名稱」，此目錄會自動建立於 `MEDIA_ROOT` 之下。
* (D) 限制只有路徑包含 `'court_photos'` 的圖片網址才能被網頁下載。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* **`upload_to`** 參數用來設定上傳檔案的儲存路徑。
* 這裡傳入 `'court_photos/'`，代表上傳的圖片會被儲存到 `<MEDIA_ROOT>/court_photos/` 目錄下。這樣做可以有效對不同功能模組上傳的圖片進行分類管理，避免所有檔案混雜在同一個根目錄。
</details>

---

### 3. 本單元中，我們將 `courts/views.py` 的第一行代碼從 `Court.objects.all().values()` 修改為 `Court.objects.all()`。請問做出這個修改的最核心原因是什麼？
* (A) `.values()` 回傳的資料不支援分頁顯示。
* (B) `.values()` 會直接回傳由原始資料庫值組成的字典（Dict）集合，而不再是模型物件（Model Instances）。這會導致我們無法在樣板中讀取 `photo.url` 屬性，或使用 `get_courttype_display` 等物件專屬方法。
* (C) `.values()` 無法查詢外鍵關係，會造成程式出錯。
* (D) 改成 `all()` 能讓查詢資料庫的速度提升十倍以上。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* Django 的 `.values()` 會將 QuerySet 中的每個物件直接轉換為一般的 Python 字典（例如 `{'courtname': '球場A', 'photo': 'img.jpg'}`）。字典是一個純資料結構，不具備 Django Model 的特殊屬性。
* 如果需要存取 `x.photo.url`（動態解析出該圖片的瀏覽器網址）或是 choices 列舉對應的 `x.get_courttype_display`，我們**必須**傳遞完整的 Model 物件，此時應使用不加 `.values()` 的 **`all()`** 來取得物件集合。
</details>

---

### 4. 關於 Django 設定檔中的 `MEDIA_ROOT` 與 `MEDIA_URL` 設定，下列哪一個敘述是正確的？
* (A) `MEDIA_ROOT` 是瀏覽器造訪上傳檔案時網址列的開頭；`MEDIA_URL` 是檔案在伺服器上的實體儲存目錄路徑。
* (B) `MEDIA_ROOT` 是伺服器儲存上傳多媒體檔案的「實體硬碟絕對路徑」；`MEDIA_URL` 是瀏覽器存取這些上傳檔案的「公開 URL 網址前綴」。
* (C) 兩者設定的內容必須完全相同，都必須是本地硬碟路徑。
* (D) `MEDIA_ROOT` 用於管理 CSS 與 JS 檔案；`MEDIA_URL` 用於管理使用者上傳的圖片。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 這是 Django 管理「多媒體上傳檔 (Media)」的兩個核心變數：
  - **`MEDIA_ROOT`**：實體磁碟目錄（如 `BASE_DIR / 'media'`），代表檔案要寫入電腦硬碟的哪裡。
  - **`MEDIA_URL`**：網路 URL 前綴（如 `'/media/'`），代表瀏覽器要以什麼網址去讀取它（如 `http://127.0.0.1:8000/media/court_photos/pic.jpg`）。
</details>

---

### 5. 在本地開發測試階段，為了讓 Django 開發伺服器（`runserver`）能夠支援並正確回應多媒體路徑的圖片存取，我們必須在專案的 `urls.py` 中進行以下哪一項路由配置？
* (A) `urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)`
* (B) `urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`
* (C) `urlpatterns += include('media.urls')`
* (D) `urlpatterns.append(path('media/', views.serve_media))`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* Django 預設不會在開發階段為您提供上傳多媒體檔案的路由託管。
* 為了讓開發伺服器能根據 `MEDIA_URL` 的網路請求，正確到 `MEDIA_ROOT` 的實體目錄中讀取圖片並回傳，我們必須匯入 `django.conf.urls.static.static` 與 `settings`，並在 `urlpatterns` 後方串接：
  `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請詳細說明：在 Django 中，什麼是「靜態檔案 (Static Files)」？什麼是「多媒體上傳檔 (Media Files)」？兩者在「檔案來源」與「Git 版本控制管理」上有何不同？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **靜態檔案 (Static Files)**：
   - **來源**：由軟體開發者（Develpers）自己撰寫或準備的網站素材，包括 CSS 樣式表、JavaScript 控制碼、網站 Logo 或背景圖。
   - **Git 管理**：它是專案原始碼的一部分。因此，這些檔案**必須**納入 Git 版本控制，一同推送到 GitHub，並跟著程式碼一起部署。
2. **多媒體上傳檔 (Media Files)**：
   - **來源**：在網站上線運行期間，由一般使用者或後台系統管理員（Administrators）動態上傳的檔案，如使用者頭像、球場照片、PDF 附件。
   - **Git 管理**：屬於動態產生的使用者數據，絕非專案原始碼。因此，**絕對不能**將上傳檔案（例如 `media/` 資料夾）納入 Git 版本控制。我們應在 `.gitignore` 中將其忽略，以免造成專案冗餘與資安外洩。
</details>

---

### 7. 在 `court_details.html` 中，我們希望印出球場照片。請寫出如何利用樣板標籤 `{% if %}` 判斷球場是否有上傳照片，如果有則印出該照片，若無則顯示一張預設的 Placeholder 佔位圖片？（請寫出關鍵的 HTML 程式碼片段）

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
我們可以使用模型實例的屬性進行布林判定，若有圖片，使用 `.photo.url` 獲取圖片的完整 URL：
```html
{% if court.photo %}
  <!-- 如果球場有相片，顯示上傳的相片 -->
  <img src="{{ court.photo.url }}" class="card-img-top" alt="{{ court.courtname }}">
{% else %}
  <!-- 如果球場沒有相片，顯示預設的佔位圖片 -->
  <img src="/static/images/default_court.jpg" class="card-img-top" alt="預設球場圖片">
{% endif %}
```
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 為了在專案根目錄的 `my_tennis_club/urls.py` 中，啟用本地開發環境下的多媒體檔案託管，請在以下代碼空缺處（標示為 `___(1)___`、`___(2)___`、`___(3)___`）填入正確的模組、類別或變數：
```python
# my_tennis_club/urls.py
from django.contrib import admin
from django.urls import path, include
# 1. 引入專案的 settings 設定檔
from django.conf import ___(1)___
# 2. 引入 static 路由輔助方法
from django.conf.urls.static import ___(2)___

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members.urls')),
    path('', include('courts.urls')),
]

# 3. 如果在開發環境 (settings.DEBUG 為 True)
if settings.DEBUG:
    # 串接多媒體上傳檔案的託管路由
    urlpatterns += ___(2)___(settings.MEDIA_URL, ___(3)___=settings.MEDIA_ROOT)
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `settings`
* `(2)`: `static`
* `(3)`: `document_root`
</details>

---

### 9. 我們想在 `courts/models.py` 的 `Court` 模型中，新增一個名為 `photo` 的多媒體上傳欄位，要求圖片上傳至 `court_photos/` 子目錄，並且在表單填寫或資料庫中，該欄位允許是留空或無資料的（非必填）。請在填充處填入正確的欄位類別與參數設定：
```python
# courts/models.py
from django.db import models

class Court(models.Model):  
    courtname = models.CharField(max_length=100)
    courttype = models.CharField(max_length=1)
    city = models.CharField(max_length=100)
    
    # 宣告圖片上傳欄位，設定上傳路徑並允許空白
    photo = models.___(1)___(
        upload_to='court_photos/', 
        ___(2)___=True, 
        ___(3)___=True
    )
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `ImageField`
* `(2)`: `blank`
* `(3)`: `null`

**解析**：
* 儲存上傳影像的欄位類別是 `ImageField`。
* `blank=True` 允許 Django 前端表單在驗證時接受此欄位留空。
* `null=True` 允許資料庫底層在此欄位寫入 `NULL` 空值，避免引發資料庫寫入衝突。
</details>
