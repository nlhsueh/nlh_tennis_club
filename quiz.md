## Django MVT 基礎課堂隨堂測驗 — 多 App 架構與 Choices 列舉 (Quiz)

本測驗旨在檢驗學生對於本單元（`court` 分支：Django 多 App 系統架構、列舉型態（Choices）處理、以及樣板中 Choices 中文對應的顯示方法 `get_<fieldname>_display`）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 在 Django 專案中，當我們要建立一個全新且獨立的子系統/應用程式（例如本單元用來管理球場的 `courts` App），應該在終端機執行哪一個指令？
* (A) `python manage.py startapp courts`
* (B) `python manage.py newapp courts`
* (C) `python manage.py startproject courts`
* (D) `python manage.py createapp courts`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(A)**

**解析**：
* `startapp` 是 Django 專屬的命令，用於在現有的 Django 專案中初始化一個全新 App 的目錄結構與基本預設檔案（如 `models.py`、`views.py` 等）。
* (C) `startproject` 是用來建立整個 Django 專案外殼骨架的指令，而非子系統 App。
</details>

---

### 2. 建立好新的 App（如 `courts`）後，我們必須將它註冊到專案設定檔 `settings.py` 中的哪一個變數清單裡，Django 才能在後續運作中，自動掃描並載入它的 Models、Migrations 以及 Templates？
* (A) `ALLOWED_APPS`
* (B) `INSTALLED_APPS`
* (C) `REGISTERED_APPS`
* (D) `MIDDLEWARE`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 所有的自訂 App、第三方套件（如 Django REST Framework）或 Django 內建系統（如 admin, auth），都必須在 `settings.py` 的 **`INSTALLED_APPS`** 列表中完成註冊。
* 否則，在執行 `makemigrations` 或是載入樣板時，Django 會完全忽略該 App 的存在。
</details>

---

### 3. 觀察 `courts/models.py` 中以下這段列舉型態（Choices）的宣告：
```python
    COURT_TYPE = [
        ("G", "草地"),
        ("H", "硬地"),
        ("N", "泥地"),
        ("D", "地毯"),
    ]
    courttype = models.CharField(max_length=1, choices=COURT_TYPE)
```
請問元組中的第一個元素（如 `"G"`）與第二個元素（如 `"草地"`）在 Django 系統中分別代表什麼含義？
* (A) 第一個元素是前端網頁呈現的中文；第二個元素是資料庫中實際儲存的英文代碼。
* (B) 第一個元素是資料庫中實際儲存的精簡值（Value）；第二個元素是便於人類閱讀的顯示名稱（Label），常在 Admin 後台或前端表單中顯示。
* (C) 兩者沒有區別，資料庫會同時儲存這兩個值。
* (D) 第一個元素是欄位名稱；第二個元素是欄位的預設值。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* Django 的 Choices 設定中，每個選項均為一個長度為 2 的二元組（Tuple）：
  - **第一個值**（如 `"G"`）：是實際寫入並儲存在資料庫中的值。通常使用簡短的代碼，可大幅節省資料庫儲存空間並提升索引效率。
  - **第二個值**（如 `"草地"`）：是便於人類閱讀的中文標籤。用於在 Django Admin 後台、表單下拉選單或前端網頁中展示給使用者看。
</details>

---

### 4. 當我們在模型中設定了 choices 欄位（例如 `courttype`），如果我們在 HTML 模板中直接寫 `{{ x.courttype }}`，網頁會印出儲存在資料庫的精簡代碼（如 `'G'`）。若我們希望在網頁上動態渲染出便於人類閱讀的中文顯示名稱（如 `'草地'`），應該在模板中使用哪一個 Django 自動生成的特殊方法？
* (A) `{{ x.courttype.label }}`
* (B) `{{ x.courttype.display }}`
* (C) `{{ x.get_courttype_display }}`
* (D) `{{ x.get_display_name }}`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* 對於任何在 `models.py` 中設定了 `choices` 參數的欄位，Django 會在模型實例化時，自動為其動態生成一個名為 **`get_<fieldname>_display()`** 的方法。
* 在樣板中直接調用該方法：`{{ x.get_courttype_display }}`，即可將資料庫中的單碼字元（如 `'G'`）無縫轉換為可讀的中文標籤（如 `'草地'`）並輸出。
</details>

---

### 5. 關於在 Django 專案中採用「多 App（Multi-App）架構」（例如同時存在 `members` 與 `courts` 兩個 App），下列敘述何者正確？
* (A) Django 專案規定只能有一個 App，多 App 架構會導致資料庫讀取混亂。
* (B) 每個 App 都應該各自專注於一項核心業務邏輯（例如 members 負責會員，courts 負責球場），這符合高內聚、低耦合的設計原則，有利於程式碼的模組化與重用。
* (C) 多 App 架構下，所有的 App 必須強行共享同一個 `views.py` 與 `urls.py`，不能分開寫。
* (D) 採用多 App 架構會導致 `python manage.py migrate` 無法執行。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* Django 的核心哲學之一就是「模組化 App」。將不同的業務功能切分為獨立的 App，有助於保持程式碼結構清晰。
* 每個 App 有各自的 `models.py`、`views.py`、`urls.py` 與 templates 資料夾，這讓 App 具有高度的獨立性，甚至能直接拷貝到其他專案中重用，是大型專案開發的最佳實踐。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請詳細說明：在多 App（Multi-App）架構下，為了讓專案的根路由配置保持簡潔與模組化，我們是如何將 `nlh_tennis_club/urls.py`（專案層級）與各個子系統（如 `members/urls.py`、`courts/urls.py`）進行串接與分流的？請寫出串接時使用的關鍵方法。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **子系統路由配置（Sub-routing）**：
   - 每個子系統 App 都會建立並維護自己專屬的 `urls.py`，用來管理該 App 內部的各個路徑（如 `path('', views.courts)`, `path('details/<int:id>', views.details)`）。
2. **根路由整合與分流**：
   - 在專案最外層的 `nlh_tennis_club/urls.py` 中，使用 `django.urls.include` 方法將子系統的路由包含進來。
   - 範例配置：
     ```python
     from django.urls import path, include

     urlpatterns = [
         path('members/', include('members.urls')),
         path('courts/', include('courts.urls')),
     ]
     ```
3. **分流機制好處**：
   - 當使用者存取以 `/courts/` 開頭的網址時，根路由會自動忽略前綴，並將剩餘的路徑比對工作「分流」交給 `courts/urls.py` 處理。這樣做可大幅減少專案主路由檔案的複雜度，實現路由的模組化分工。
</details>

---

### 7. 在開發 `courts` 子系統時，我們建立了一個與 `Member` 類似的 MVT 展示流程。請簡述球場列表頁面（`all_courts.html`）與球場細節頁面（`court_details.html`）在 View 層級是如何撈取資料庫資料，並渲染出來的？（請說明分別使用了哪些 Django ORM 方法）

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **球場列表頁面（List View）**：
   - 在 `courts/views.py` 的列表視圖中，調用 **`Court.objects.all().values()`**（或 `Court.objects.all()`）方法，從資料庫中一次性撈取所有的球場資料。
   - 將撈出的資料包裝在 `context` 字典中，載入 `all_courts.html` 樣板進行渲染輸出。
2. **球場細節頁面（Detail View）**：
   - 在網址路由中設計變數接收球場 ID（例如 `details/<int:id>`）。
   - 在 `views.py` 的細節視圖中接收該 `id` 參數，並使用 **`Court.objects.get(id=id)`** 方法，精準地從資料庫中取得符合該 ID 的單一球場物件。
   - 將此球場物件傳入 `court_details.html` 樣板，在前端印出其專屬屬性（球場名、型態與城市）。
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 請完成以下 `courts/models.py` 中 `Court` 模型（Model）的填空，使其包含正確的 `courtname`、列舉欄位 `courttype` 與 `city`，並能正常與資料庫對接：
```python
# courts/models.py
from django.db import ___(1)___

class Court(models.Model):  
    # 1. 定義球場型態列舉清單
    COURT_TYPE = [
        ("G", "草地"),
        ("H", "硬地"),
        ("N", "泥地"),
        ("D", "地毯"),
    ]
    # 2. 定義球場名稱字串欄位
    courtname = models.CharField(max_length=100)
    
    # 3. 定義使用 choices 的列舉欄位，限制資料庫長度為 1 碼
    courttype = models.CharField(max_length=1, ___(2)___=COURT_TYPE)
    
    # 4. 定義城市字串欄位
    city = models.CharField(max_length=100)

    # 5. 設定物件字串表達方式
    def __str__(self):
        return f"{self.city} {self.courtname}"
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `models`
* `(2)`: `choices`
</details>

---

### 9. 以下是 `all_courts.html` 中用來遍歷並顯示所有球場列表的部分 HTML 樣板，請填入正確的 Django 樣板語法、路徑或特殊方法以完成列表的渲染：

```html
<!-- courts/templates/all_courts.html -->
{% extends "master.html" %}

{% block content %}
  <h2>網球場清單</h2>
  <ul>
    <!-- 1. 遍歷所有的球場資料 -->
    ___(1)___ x in courts %}
      <li>
        <!-- 2. 動態生成通往該球場細節頁面的超連結 -->
        <a href="___(2)___">{{ x.courtname }}</a>
        
        <!-- 3. 印出球場的城市 -->
        ( 城市：{{ x.___(3)___ }} | 
        
        <!-- 4. 印出便於人類閱讀的「球場中文型態」(如草地、硬地) -->
        型態：{{ x.___(4)___ }} )
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `{% for`
* `(2)`: `details/{{ x.id }}`
* `(3)`: `city`
* `(4)`: `get_courttype_display`

**解析**：
* 在樣板中開啟循環遍歷的標籤是 `{% for 變數 in 集合 %}`。
* 超連結路徑可使用相對路徑 `details/{{ x.id }}` 拼接到當前 URL 後面，指向單一球場細節。
* 輸出欄位屬性使用 `x.city`。
* 對於 `choices` 列舉欄位，必須調用 `get_<fieldname>_display` 以便在網頁印出對應的中文標籤。
</details>
