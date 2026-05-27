# Django MVT 基礎課堂隨堂測驗 — 首頁與除錯模式設定 (Quiz)

本測驗旨在檢驗學生對於本單元（`index` 分支：系統首頁建立、除錯模式關閉與自訂 `404` 錯誤說明頁面、模板導航連結）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 在 Django 專案的設定檔 `settings.py` 中，哪一個變數是用來控制「除錯模式」的開關？當我們要將專案部署上線（Production）時，該變數應如何設定？
* (A) `DEBUG_MODE = False`
* (B) `DEBUG = False`
* (C) `ERROR_LOG = True`
* (D) `TEST_ENVIRONMENT = False`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 在 Django 中，**`DEBUG`** 是布林型態變數，用來控制是否開啟除錯模式。
* 當 `DEBUG = True` 時，若網頁出錯，會顯示非常詳細的報錯資訊（StackTrace、變數狀態等）；當 `DEBUG = False` 時，則會隱藏細節，改用簡潔的狀態頁面（如 404、500）回覆用戶。
* 因此，部署上線時為了安全性與隱私，**必須**將其設定為 `False`。
</details>

---

### 2. 當我們在 `settings.py` 中將 `DEBUG` 設定為 `False` 後，若沒有正確設定哪一個變數，Django 在啟動或接收請求時會直接拋出 `CommandError` 或 `Bad Request (400)` 錯誤？
* (A) `SECURE_HOSTS`
* (B) `TRUSTED_DOMAINS`
* (C) `ALLOWED_HOSTS`
* (D) `SERVER_NAMES`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* 當除錯模式關閉（`DEBUG = False`）時，Django 為了防範 HTTP Host Header 攻擊，會嚴格檢查 Request 的域名是否合法。
* **`ALLOWED_HOSTS`** 是一個清單，用來指定該 Django 專案允許運行的主機名稱或 IP 地址。若在測試階段想允許所有 Host，可以設定為 `ALLOWED_HOSTS = ['*']`。
</details>

---

### 3. 當 `DEBUG = False` 且使用者造訪了不存在的路由時，Django 會自動尋找並渲染自訂的 `404` 錯誤網頁。請問該自訂模板檔案的檔名與預設存放位置應為下列何者？
* (A) 檔名為 `error.html`，放在專案根目錄下
* (B) 檔名為 `404.html`，放在 Template 目錄下（例如 `templates/404.html`）
* (C) 檔名為 `page_not_found.html`，放在靜態資料夾 `static/` 內
* (D) 檔名為 `missing.html`，放在 `settings.py` 同級目錄下

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* Django 內建的 404 處理器在找不到資源時，會自動在註冊的模板路徑中尋找名為 **`404.html`** 的檔案。
* 我們只需在模板資料夾（例如 `members/templates/404.html`，或是全域 templates 資料夾）中建立一個名為 `404.html` 的檔案，Django 就會自動載入它。
</details>

---

### 4. 我們想要為網球俱樂部建立一個「系統主畫面（首頁）」，並希望當使用者存取 `http://127.0.0.1:8000/` 時能直接進入該首頁。在 `my_tennis_club/urls.py` 中，正確的根路由 path 宣告方式為何？
* (A) `path('/', include('members.urls'))`
* (B) `path('index/', include('members.urls'))`
* (C) `path('', include('members.urls'))`
* (D) `path('*', include('members.urls'))`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* 在 Django 的 `path()` 路由比對中，**空字串 `''`** 代表專案的根路徑（Root URL）。
* ⚠️ 注意：Django 的路由匹配會自動忽略最前面的斜線，因此不需要在 `path()` 的開頭加上 `/`，所以 (A) `path('/')` 是不正確的。
</details>

---

### 5. 如果我們在路由中為首頁設定了別名：`path('', views.main, name='main')`。為了讓繼承母模板 `master.html` 的所有分頁都能快速「回到首頁」，我們應該在 HTML 的 `<a>` 標籤中，使用哪一個最符合 Django 最佳實踐的動態解析語法？
* (A) `<a href="/members/main/">回到首頁</a>`
* (B) `<a href="{% url 'main' %}">回到首頁</a>`
* (C) `<a href="{{ url_main }}">回到首頁</a>`
* (D) `<a href="{% redirect 'main' %}">回到首頁</a>`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 使用 **`{% url '路由別名' %}`** 是 Django 模板中最推薦的寫法。
* 它可以根據 `urls.py` 中定義的 `name='main'` 動態反向解析出對應的真實網址。
* 這樣做的好處是：未來如果修改了 `urls.py` 中的 URL 路徑，HTML 模板中的超連結完全不需要手動修改，避免了硬編碼（Hardcoding）路徑所帶來的維護難題。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請簡述為什麼在「正式生產部署環境（Production Environment）」中，絕對不可開啟除錯模式（必須將 `DEBUG` 設為 `False`）？這會帶來哪些嚴重的資安隱患？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **敏感資訊外洩**：當網頁程式出錯時，`DEBUG = True` 會在瀏覽器上顯示非常詳細的 traceback（堆疊追蹤資訊），其中包含伺服器的內部實體檔案路徑、Python 程式碼片段、第三方套件版本等。
2. **機密參數暴露**：報錯頁面中甚至會顯示 Django 所有的環境變數與設定資訊，包括 `SECRET_KEY`、資料庫連線密碼、API 密鑰等，一旦暴露將導致伺服器或資料庫被完全掌控。
3. **增加被攻擊機率**：惡意攻擊者能藉由這些詳細的錯誤訊息，精準得知系統所使用的框架漏洞、資料庫結構，進而輕鬆發起 SQL Injection 或代碼執行等精準攻擊。
</details>

---

### 7. 請說明在 `DEBUG = False` 模式下，當 Django 遇到 `Http404` 異常時，它是如何搜尋並渲染 `404.html` 模板的？如果我們同時在多個 App 的 `templates/` 資料夾下都建立 `404.html`，會發生什麼事？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
* **搜尋機制**：
  - Django 觸發 404 錯誤時，會調用內建的 `django.views.defaults.page_not_found` 視圖。
  - 該視圖會透過配置的模板引擎（Templates Engines）載入器，依序在 `settings.py` 中設定的 `TEMPLATES` -> `DIRS` 列表路徑中尋找是否存在 `404.html`。
  - 如果沒有，則會按照 `INSTALLED_APPS` 裡註冊的 App 順序，在每個 App 的 `templates/` 目錄下尋找 `404.html`。
* **多個 `404.html` 衝突結果**：
  - Django 模板載入器採用「**先找到先贏（First-match-wins）**」原則。
  - 當多個 App 內都存在 `404.html` 時，Django 會渲染在 `INSTALLED_APPS` 中**註冊順序最靠前**的那個 App 下的 `404.html`，其餘的將會被忽略。因此，最佳做法是將全域錯誤頁面放在專案層級的 `templates/` 資料夾下。
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 為了將本網球系統切換到生產環境的安全狀態，我們需要修改 `settings.py` 的設定。請在下列程式碼的空缺處（標示為 `___(1)___`、`___(2)___`）填入正確的設定值，使其能夠關閉除錯功能並允許所有 Host 進行測試：

```python
# my_tennis_club/settings.py

# 1. 關閉除錯模式
DEBUG = ___(1)___

# 2. 允許任何主機網域存取該 Django 系統
ALLOWED_HOSTS = [___(2)___]
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `False`
* `(2)`: `'*'` （或 `"*"`）

**完整設定呈現**：
```python
# my_tennis_club/settings.py

DEBUG = False

ALLOWED_HOSTS = ['*']
```
</details>

---

### 9. 我們在 `members/views.py` 中撰寫了 `main` 視圖來處理首頁請求，並希望該視圖能載入 `main.html` 模板。同時，我們在 `master.html` 中加入了導覽列首頁連結。請填入空缺處（標示為 `___(1)___`、`___(2)___`、`___(3)___`）的程式碼：

```python
# members/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def main(request):
  template = loader.get_template('___(1)___')
  return HttpResponse(template.render({}, request))
```

```html
<!-- members/templates/master.html -->
<!DOCTYPE html>
<html>
<head>
  <title>{% block title %}{% endblock %}</title>
</head>
<body>

<div class="topnav">
  <!-- 動態連結到名為 'main' 的路由 -->
  <a href="___(2)___">Home</a> | 
  <a href="___(3)___">Members</a>
</div>

{% block content %}
{% endblock %}

</body>
</html>
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `main.html`
* `(2)`: `{% url 'main' %}`
* `(3)`: `{% url 'members' %}`

**解析**：
* 在視圖中，我們需要指定載入首頁模板 `main.html`。
* 在母模板中，使用 `{% url 'main' %}` 導向首頁路由，`{% url 'members' %}` 導向會員列表路由，可實現高度靈活的動態導覽。
</details>
