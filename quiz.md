# Django MVT 基礎課堂隨堂測驗 — Master-Details & Extending (Quiz)

本測驗旨在檢驗學生對於本單元（`details` 分支：Master-Details 架構、Template Extending 模板繼承、URL 參數傳遞與單一資料獲取）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 在 Django 的 URL 路由設定（`urls.py`）中，如果我們要擷取 URL 中的整數 ID 作為參數傳遞給視圖函數（例如從 `members/details/5` 擷取出整數 `5` 並傳給 `id` 參數），應該使用下列哪一個路徑宣告格式？
* (A) `path('members/details/<id>', views.details)`
* (B) `path('members/details/<int:id>', views.details)`
* (C) `path('members/details/{id}', views.details)`
* (D) `path('members/details/<str:id>', views.details)`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* Django 提供了路徑轉換器（Path Converters）來捕獲網址參數。
* `<int:id>` 代表捕獲一個**整數**型態的參數，並將其命名為 `id` 傳遞給視圖函數。
* (A) `<id>` 預設為字串型態。
* (C) 與 (D) 分別為錯誤的語法和錯誤的型態轉換器。
</details>

---

### 2. 關於 Django 的模板繼承（Template Inheritance）機制，子模板（Child Template）必須在檔案最頂端使用哪一個標籤（Tag）來宣告其要承襲哪一個母模板（Parent Template）的網頁結構？
* (A) `{% include "master.html" %}`
* (B) `{% import "master.html" %}`
* (C) `{% extends "master.html" %}`
* (D) `{% block content %}`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* **`{% extends "母模板名稱" %}`** 是 Django 模板系統中宣告繼承關係的唯一專屬標籤，且必須放在子模板檔案的最上方第一行。
* (A) `include` 是用來嵌入另一個獨立的網頁片段。
* (B) `import` 不是 Django 模板的內建繼承語法。
* (C) 是正確的。
</details>

---

### 3. 在 `details` 視圖函數中，為了從資料庫取得符合特定 ID 的單一會員物件，下列哪一個 Django ORM 指令最為正確且常用？
* (A) `mymember = Member.objects.all().get(id=id)`
* (B) `mymember = Member.objects.get(id=id)`
* (C) `mymember = Member.objects.filter(id=id)`
* (D) `mymember = Member.objects.find(id=id)`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* **`Member.objects.get(id=id)`** 是用來檢索並直接回傳**單一條**符合條件的物件實例的最標準做法。
* (C) `filter()` 雖然能用來篩選資料，但它回傳的是一個 `QuerySet`（物件集合列表），而非單一的物件實例。
* (A) 寫法多餘。
* (D) `find()` 不是 Django ORM 的有效查詢指令。
</details>

---

### 4. 關於在母模板（如 `master.html`）中所定義的 `{% block content %}{% endblock %}` 區塊，下列敘述何者正確？
* (A) 它是用來引入網站全域 CSS 樣式或 JS 動態檔案的專用載入標記。
* (B) 它是母模板保留給子模板用來填入「該頁面特定網頁內容」的佔位標記（Placeholder）。
* (C) 如果子模板繼承後沒有覆寫（Override）這個 Block，系統在渲染時會直接拋出錯誤並崩潰。
* (D) 子模板要覆寫這個區塊時，必須使用 `{% block content = "value" %}` 語法。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* `{% block <名稱> %}` 語法用來在母模板中保留佔位，允許子模板在繼承後覆寫其中的內容。
* 如果子模板沒有覆寫該區塊，系統會預設渲染母模板中該 block 內寫好的預設內容（如果有的話），並不會拋出錯誤或崩潰。
</details>

---

### 5. 如果我們希望在會員列表 `all_members.html` 中為每個會員名字加上超連結，點擊後導向該會員的詳情頁（例如當前的相對網址路徑），在 Django 模板語法中應如何撰寫超連結？
* (A) `<a href="details/{{ x.id }}">{{ x.firstname }}</a>`
* (B) `<a href="details/{ x.id }">{{ x.firstname }}</a>`
* (C) `<a href="members/details/[x.id]">{{ x.firstname }}</a>`
* (D) `<a href="/details/x.id">{{ x.firstname }}</a>`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(A)**

**解析**：
* 在 HTML 超連結中，使用相對路徑 `details/{{ x.id }}` 可以讓使用者從當前網址 `/members/` 順利導向至子目錄 `/members/details/<id>`。
* 變數必須包裹在 `{{ }}` 雙大括號內，才能被 Django 模板引擎正確解析並將 `x.id` 替換為實際的數字 ID。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請簡述什麼是「Master-Extending (模板繼承)」，以及使用此網頁組織架構的核心優點為何？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
* **定義**：
  模板繼承是一種進階的網頁組織方式，我們會先建立一個共用的母模板（如 `master.html`），在其中定義全站共用的 HTML 骨架（例如 `<head>`、側邊欄、全域導航列與頁尾），並保留一些命名區塊（`{% block %}`）。子模板只需繼承母模板並覆寫這些特定 block 即可。
* **核心優點**：
  1. **維護一致風格**：能確保全站所有網頁的版面、配色與導覽控制維持高度一致。
  2. **避免重複程式碼 (DRY - Don't Repeat Yourself)**：不需在每個 HTML 檔案中重複撰寫重複的 `<html>`, `<head>`, `<body>` 結構。
  3. **便於快速維護**：當需要修改全站共用的版面配置（如修改頁尾的版權聲明）時，只需修改母模板一處，所有子網頁便會自動同步更新。
</details>

---

### 7. 請說明 `Member.objects.get(id=id)` 與 `Member.objects.filter(id=id)` 兩者在回傳結果與出錯機制上的本質差異。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
* **`Member.objects.get(id=id)`**：
  - **回傳結果**：直接回傳**單一條符合條件的 Member 物件實例**。
  - **出錯機制**：條件要求非常嚴格。如果找不到任何符合的資料，會拋出 `DoesNotExist` 異常；如果找到多於一筆的資料，則會拋出 `MultipleObjectsReturned` 異常。
* **`Member.objects.filter(id=id)`**：
  - **回傳結果**：無論篩選出的結果有幾筆（0 筆、1 筆或多筆），都會回傳一個 **`QuerySet`（物件集合列表）**。
  - **出錯機制**：極其寬鬆，不論結果如何都不會拋出任何異常。若找不到符合的資料，它會回傳一個空的 `QuerySet`。
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 在 `members/views.py` 中，我們需要編寫 `details` 視圖，透過 URL 傳入的 `id` 參數從資料庫取得對應會員的單一物件，並渲染 `details.html` 頁面。請在下列程式碼的空缺處（標示為 `___(1)___`、`___(2)___`、`___(3)___`）填入正確的 Django ORM 或視圖函式代碼：

```python
from django.http import HttpResponse
from members.models import Member
from django.template import loader

def details(request, id):
    mymember = Member.objects.___(1)___(id = id)
    template = loader.___(2)___('details.html')
    context = {
        'mymember': mymember,
    }
    return HttpResponse(template.___(3)___(context, request))
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `get`
* `(2)`: `get_template`
* `(3)`: `render`

**完整程式碼呈現**：
```python
def details(request, id):
    mymember = Member.objects.get(id = id)
    template = loader.get_template('details.html')
    context = {
        'mymember': mymember,
    }
    return HttpResponse(template.render(context, request))
```
</details>

---

### 9. 我們希望建立一個子網頁模板，繼承自母模板 `master.html`，並覆寫母模板中的 `title` 區塊與 `content` 區塊。請在下列模板程式碼的空缺處（標示為 `___(1)___`、`___(2)___`、`___(3)___`、`___(4)___`）填入正確的 Django 模板標籤：

```html
___(1)___ extends "master.html" ___(2)___

___(3)___ block title ___(4)___
  球場詳情頁面
{% endblock %}

{% block content %}
  <h1>球場細節資訊</h1>
{% endblock %}
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `{%`
* `(2)`: `%}`
* `(3)`: `{%`
* `(4)`: `%}`

**完整 HTML 呈現**：
```html
{% extends "master.html" %}

{% block title %}
  球場詳情頁面
{% endblock %}

{% block content %}
  <h1>球場細節資訊</h1>
{% endblock %}
```
</details>
