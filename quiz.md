# Django MVT 會員系統 — 隨堂測驗 (Quiz)

本測驗旨在檢驗學生對於本單元「Django 會員系統（Master-Details 架構、URL 變數傳遞、與母版樣板繼承）」的學習成效。題目緊扣本單元的分支程式碼與基本概念。

---

## 一、 選擇題 (Multiple Choice) — 共 5 題

### Q1. 關於 Django 中的 `{% extends "master.html" %}` 樣板標籤，下列敘述何者正確？
* (A) 它必須放在 HTML 檔案的最尾端。
* (B) 它可以用來導入多個不同的母版樣板，例如 `{% extends "a.html" "b.html" %}`。
* (C) 它必須作為子樣板（Child Template）檔案中的第一個樣板標籤。
* (D) 它是用來定義可以在母版中被覆寫的區塊名稱。

<details>
<summary>💡 點擊查看解答與解析</summary>

**正確答案**：**(C)**

**解析**：
* 在 Django 樣板系統中，`{% extends %}` 標籤是用來聲明樣板繼承關係。它**必須**是子樣板檔案中的第一個樣板標籤。如果它的前面有其他 HTML 內容或樣板標籤，樣板解析器在載入時會出錯或忽略繼承關係。
* (A) 必須放在檔案最上方；(B) 只能繼承一個母版；(D) 定義區塊名稱的是 `{% block %}` 標籤。
</details>

---

### Q2. 在本單元的子系統路由 `members/urls.py` 中，有以下設定：
```python
path('members/details/<int:id>', views.details, name='details')
```
請問其中的 `<int:id>` 主要作用是什麼？
* (A) 限制該網址只能由特定的使用者訪問。
* (B) 它是一個路徑變數（URL Parameter），會匹配網址中的一個整數，並將其作為名為 `id` 的參數傳遞給後端的 `views.details` 函數。
* (C) 它是 Django 內建用來自動遞增資料庫主鍵（Primary Key）的指令。
* (D) 它是一個內建的防毒檢驗碼，用來防止惡意的 SQL 注入。

<details>
<summary>💡 點擊查看解答與解析</summary>

**正確答案**：**(B)**

**解析**：
* `<int:id>` 是 Django 網址路由的路徑轉換器（Path Converter）。
* `<int: ...>` 表示匹配網址路徑中的一個整數（整數類型），而 `id` 是這個被捕獲變數的名稱。當網址匹配成功時（例如 `/members/details/3`），Django 會自動將該整數作為關鍵字參數 `id=3` 傳遞給 `views.details(request, id)` 函數。
</details>

---

### Q3. 觀察本單元的 `members/views.py` 程式碼，當點擊特定會員進入其詳細資料頁面時，View 函數使用了 `Member.objects.get(id=id)` 來查詢資料。請問 `.get()` 方法在找不到符合該 id 的資料時會發生什麼事？
* (A) 回傳一個空的清單 `[]`，網頁不會報錯。
* (B) 回傳 `None` 值，並自動跳轉到首頁。
* (C) 拋出 `Member.DoesNotExist` 的例外錯誤（Exception），若未妥善捕捉會導致網頁伺服器產生 500 錯誤。
* (D) 自動在資料庫中隨機新增一筆該 id 的測試資料。

<details>
<summary>💡 點擊查看解答與解析</summary>

**正確答案**：**(C)**

**解析**：
* Django ORM 的 `.get()` 方法預期資料庫中**必須且只能**回傳「剛好一筆」符合條件的資料。
* 如果在資料庫中找不到該條件的資料，它會拋出 `DoesNotExist` 異常；若查到多於一筆，則會拋出 `MultipleObjectsReturned` 異常。如果想要在查無資料時顯示 404 頁面，通常會搭配 `get_object_or_404()` 來使用。
</details>

---

### Q4. 在母版 `master.html` 中我們宣告了 `{% block content %}{% endblock %}`，而在子樣板 `all_members.html` 中我們寫了 `{% block content %} ... {% endblock %}`。這種設計架構的主要優點是什麼？
* (A) 它可以完全取代後端的 Python View 程式碼。
* (B) 它可以自動將資料庫的表格內容轉成網頁表格。
* (C) 它可以建立一個一致性的外觀骨架（如導覽列、頁尾），並讓各個子頁面只專注於自己專屬的網頁內容（提高程式重用性與維護性）。
* (D) 它能將網頁載入速度提升十倍以上。

<details>
<summary>💡 點擊查看解答與解析</summary>

**正確答案**：**(C)**

**解析**：
* 樣板繼承（Template Inheritance）的主要目的在於「不要重複自己 (DRY, Don't Repeat Yourself)」。
* 母版負責維護一致的排版骨架與導覽架構，而子樣板只需要透過複寫 `block` 來填入各自專屬的內容。當網站需要更動整體外觀（如修改導覽列文字）時，只需修改 `master.html` 一個檔案即可，極大地降低了網頁系統的維護成本。
</details>

---

### Q5. 若我們想要在網頁上建立一個連結，當使用者點擊它時，能自動回到本專案的首頁（Index/Main Page），依據 `members/urls.py` 中 `path('', views.main, name='main')` 的定義，下列哪一個 HTML 標記最為正確？
* (A) `<a href="{% url 'members' %}">首頁</a>`
* (B) `<a href="{% url 'main' %}">首頁</a>`
* (C) `<a href="main.html">首頁</a>`
* (D) `<a href="{% extends 'main' %}">首頁</a>`

<details>
<summary>💡 點擊查看解答與解析</summary>

**正確答案**：**(B)**

**解析**：
* 在 `members/urls.py` 的路徑設定中，我們透過 `name='main'` 將首頁的路由路徑命名為 `"main"`。
* 在 HTML 樣板中，使用 `{% url 'main' %}` 會被 Django 樣板引擎解析，自動生成該路由對應的真實網址（此處為根目錄 `/`）。這是避免寫死網址（Hardcoding）的最佳實踐。
</details>

---

## 二、 簡答題 (Short Answer) — 共 2 題

### Q6. 請解釋「Master-Details（概述與細節）」設計模式在網頁系統中的常見應用情境，並以本單元的 `all_members.html` 與 `details.html` 之間的互動流程為例進行說明。

<details>
<summary>💡 點擊查看解答與解析</summary>

**參考答案**：
* **常見應用情境**：
  在許多網頁應用程式中，為避免單一頁面過於擁擠、載入緩慢或不便閱讀，通常會先提供一個「概要列表」（Master），例如商品清單、會員清單等。當使用者對清單中的某個項目感興趣並點擊時，系統才會導向展示該項目所有詳細屬性的「細節頁面」（Details）。
* **本單元流程**：
  1. 概要頁面 `all_members.html` 巡覽並列出所有會員的姓名，每筆姓名都包裹在一個指向特定 ID 的超連結中，例如 `<a href="details/{{ x.id }}">`。
  2. 使用者點擊 Alice 的名字後，網址傳送 `/members/details/1` 到 Django 路由。
  3. 路由捕獲 `id=1` 並傳遞給 `views.details(request, id)` 函數。
  4. 函數向資料庫撈取單一物件，將其放入 `mymember` 變數並傳遞給 `details.html` 進行渲染，成功在專屬頁面展示 Alice 的電話與入會日期等完整資訊。
</details>

---

### Q7. 請指出「母版繼承（Template Inheritance）」中，母版（Master Template）與子樣板（Child Template）各自扮演的角色，以及在子樣板中如何使用關鍵字來複寫母版的內容？

<details>
<summary>💡 點擊查看解答與解析</summary>

**參考答案**：
* **母版 (Master Template)**：
  扮演「母片骨架」的角色。它宣告整個網站或專案共通的 HTML 骨架結構（例如引入 CSS/JS、導覽列、頁尾宣告），並在骨架中透過 `{% block 區塊名稱 %}{% endblock %}` 語法定義若干個「預留插槽」，等待子樣板來填充內容。
* **子樣板 (Child Template)**：
  扮演「特定頁面專屬內容」的角色。它本身沒有完整的 HTML 外殼，而是在檔案的最上方使用 `{% extends "母版名稱.html" %}` 宣告要繼承哪一個母版，接著再透過 `{% block 區塊名稱 %}專屬內容{% endblock %}` 將內容精準地填入母版對應的插槽位置，藉此完成頁面組裝。
</details>

---

## 三、 程式填空題 (Fill in the Blank) — 共 2 題

### Q8. 請完成以下 `members/views.py` 中 `details` 視圖（View）函數的填空，使其能依據傳入的 `id` 參數從資料庫撈取單一會員，並渲染 `details.html` 樣板。
```python
def details(request, id):
    # 1. 依據傳入的 id 參數查詢單一會員資料
    mymember = _______________________________________________
    
    # 2. 載入 details.html 樣板
    template = _______________________________________________
    
    # 3. 封裝傳給樣板的上下文資料
    context = {
        'mymember': mymember,
    }
    
    # 4. 渲染樣板並回傳
    return HttpResponse(template.render(context, request))
```

<details>
<summary>💡 點擊查看解答與解析</summary>

**正確答案**：

* 填空 1：**`Member.objects.get(id=id)`**
* 填空 2：**`loader.get_template('details.html')`**

**完整程式碼呈現**：
```python
def details(request, id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mymember': mymember,
    }
    return HttpResponse(template.render(context, request))
```
</details>

---

### Q9. 請完成以下子樣板 `details.html` 的填空，使其能繼承 `'master.html'` 母版，並覆寫母版中的 `title` 與 `content` 區塊，以印出該會員的名字（`mymember.firstname`）。
```html
<!-- 1. 繼承 master.html 母版 -->
(a)______ extends "master.html" (b)______

<!-- 2. 覆寫 title 區塊 -->
(c)______ block title (d)______
  詳細資料 - (e)______ mymember.firstname (f)______
(g)______ endblock (h)______

<!-- 3. 覆寫 content 區塊 -->
(i)______ block content (j)______
  <h1>會員姓名：(e)______ mymember.firstname (f)______</h1>
  <p>回到：<a href="/members">會員列表</a></p>
(k)______ endblock (l)______
```

<details>
<summary>💡 點擊查看解答與解析</summary>

**正確答案**：

* (a) **`{%`**
* (b) **`%}`**
* (c) **`{%`**
* (d) **`%}`**
* (e) **`{{`**
* (f) **`}}`**
* (g) **`{%`**
* (h) **`%}`**
* (i) **`{%`**
* (j) **`%}`**
* (k) **`{%`**
* (l) **`%}`**

**完整樣板內容**：
```html
{% extends "master.html" %}

{% block title %}
  詳細資料 - {{ mymember.firstname }}
{% endblock %}

{% block content %}
  <h1>會員姓名：{{ mymember.firstname }}</h1>
  <p>回到：<a href="/members">會員列表</a></p>
{% endblock %}
```
</details>
