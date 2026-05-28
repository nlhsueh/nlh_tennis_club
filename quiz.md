## Django MVT 基礎課堂隨堂測驗 — Template if 標籤與資料遷移 (Quiz)

本測驗旨在檢驗學生對於本單元（`age` 分支：Django Model 新增欄位、資料庫遷移機制 `makemigrations`/`migrate`、以及 Django Template 中的 `{% if %}` 條件判斷標籤）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 當我們在 Django 的 Model 中新增一個欄位時（例如在 `Member` 中加入 `age = models.IntegerField(default=20)`），為了將此結構變更同步套用到實際的資料庫中，我們必須在終端機依序執行哪一組指令？
* (A) `python manage.py runserver` ➔ `python manage.py check`
* (B) `python manage.py startapp` ➔ `python manage.py createsuperuser`
* (C) `python manage.py makemigrations` ➔ `python manage.py migrate`
* (D) `python manage.py sqlmigrate` ➔ `python manage.py flush`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* 在 Django 中，修改 Model 結構後，必須先執行 **`makemigrations`** 來讓 Django 偵測模型異動，並在該 App 的 `migrations/` 資料夾下自動生成遷移腳本檔案。
* 接著執行 **`migrate`** 指令，Django 才會真正將這些遷移腳本轉換為 SQL 命令並執行，從而更新實際資料庫的資料表結構。
</details>

---

### 2. 在新增 `age` 欄位時，我們設定了 `default=20`。請問設定「預設值 (default)」在模型遷移（Migration）時的最核心作用是什麼？
* (A) 為了限制使用者在前端表單中輸入的年齡必須剛好是 20 歲。
* (B) 當資料庫中已存在舊的會員資料時，Django 能夠自動為舊資料的 `age` 欄位填入預設值 `20`，避免因為欄位不允許為空（NOT NULL）而導致遷移失敗。
* (C) 為了讓網頁的讀取速度自動提升，並節約伺服器的記憶體空間。
* (D) 這是用來宣告 `age` 是一個外鍵（ForeignKey）的專用關鍵字。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 如果資料庫中本來就存有會員資料，當我們新增一個不可為空的新欄位時，如果沒有設定預設值 `default`，資料庫在更新欄位結構時，會因為「舊有的紀錄不知道該填寫什麼年齡」而導致 `NOT NULL` 限制衝突，進而導致遷移失敗。
* 設定 `default` 能確保資料庫中已存有的舊會員資料自動取得一個合理的年齡初始值（此例為 20 歲）。
</details>

---

### 3. 在 Django 樣板（Template）中，使用 `{% if %}` 標籤進行條件判斷，下列哪一個語法結構或結束標籤是完全正確的？
* (A) `{% if x.age < 20 %} ... {% end %}`
* (B) `{% if x.age < 20 %} ... {% endif %}`
* (C) `{% if x.age < 20 %} ... { endif }`
* (D) `{% if x.age < 20 %} ... <!-- endif -->`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* Django 樣板的條件判斷標籤必須使用 `{% if 條件式 %}` 開始。
* 並且必須配合成對的結束標籤 **`{% endif %}`**（注意有 `%` 符號包裹且中間無空格），以明確告知樣板引擎條件判斷區塊的邊界。
</details>

---

### 4. 在本單元的 `all_members.html` 中，我們在樣板內透過迴圈並搭配 `{% if x.age < 20 %}` 篩選出青少年會員。關於「在 Template 中使用 if 進行篩選」與「在 View 中使用 ORM 篩選（例如 `Member.objects.filter(age__lt=20)`）」，下列敘述何者正確？
* (A) 在 Template 中進行篩選效能更好，因為不需要經過後端資料庫查詢。
* (B) 兩者在效能上完全沒有任何區別，僅是程式碼撰寫位置不同而已。
* (C) 在 View 中篩選能有效減少資料庫與伺服器之間傳輸的資料量。如果資料量極大，應在 View 中篩選，只抓取需要的資料送往 Template。
* (D) Django 官方規定禁止在 View 函數中進行任何資料篩選。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* 雖然兩者都能達到顯示正確資料的效果，但運作機制有著巨大的效能差異：
  - **Template 篩選**：必須先把「所有」會員從資料庫撈出並傳送至記憶體，再由樣板引擎跑遍歷與過濾，極度消耗資源。
  - **View 篩選（ORM）**：直接在資料庫端執行篩選，僅傳送符合條件的會員至前端，傳輸與運算效率極高。
* 效能最佳實踐是「在 View 中過濾資料，在 Template 中僅負責展示」。
</details>

---

### 5. 如果我們想在樣板中判定一個會員是否年滿 20 歲且不超過 30 歲（即包含 20 與 30 歲），下列哪一個 Django 樣板條件判斷寫法正確？
* (A) `{% if x.age >= 20 and x.age <= 30 %}`
* (B) `{% if x.age >= 20 && x.age <= 30 %}`
* (C) `{% if 20 <= x.age <= 30 %}`
* (D) `{% if x.age >= 20 AND x.age <= 30 %}`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(A)**

**解析**：
* Django 樣板系統支援標準的比較運算子（如 `>=`, `<=`）。
* 在做邏輯與（AND）的複合判斷時，必須使用 Python 的全小寫關鍵字 **`and`**，而不可以使用 JavaScript 的 `&&` 或全大寫的 `AND`。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請簡述在 Django 中什麼是「資料庫遷移（Database Migrations）」？並解釋 `makemigrations` 與 `migrate` 這兩個核心指令在處理模型異動時扮演的具體角色與互動流程。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **資料庫遷移（Migrations）**：它是 Django 用來在模型（models.py）發生變更時，將變更記錄下來並安全地同步更新至實際資料庫結構（SQLite / MySQL 等）中的版本控制系統。
2. **`makemigrations`（生成設計圖）**：負責偵測模型變更。它會對比 `models.py` 的現有代碼與之前的狀態，在 `migrations/` 目錄下自動寫入一個 Python 檔案（如 `0002_member_age.py`）。此時實體資料庫尚未發生任何改變。
3. **`migrate`（按圖施工）**：負責套用變更。它會讀取那些新生成的遷移檔案，將其翻譯成對應資料庫的 SQL 語法並在資料庫中執行，從而正式修改實體資料庫的欄位與資料表結構。
</details>

---

### 7. 在 `all_members.html` 中，我們需要將會員分成「青少年組（小於 20 歲）」與「成人組（大於等於 20 歲）」。若不使用兩個獨立的 `{% for %}` 迴圈，而是希望在「單一迴圈」中完成，請寫出如何利用 `{% else %}` 來改寫樣板程式碼？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
我們可以利用 `{% if %}` 搭配 `{% else %}` 來在同一個 `{% for %}` 迴圈中進行二分支判斷，這樣只需要掃描一遍資料：
```html
<ul>
  {% for x in mymembers %}
    {% if x.age < 20 %}
      <li>[青少年] <a href="details/{{ x.id }}">{{ x.firstname }} {{ x.lastname }}</a>, {{ x.age }}</li>
    {% else %}
      <li>[成年人] <a href="details/{{ x.id }}">{{ x.firstname }} {{ x.lastname }}</a>, {{ x.age }}</li>
    {% endif %}
  {% endfor %}
</ul>
```
這樣可以有效減少樣板中 `{% for %}` 迴圈遍歷的次數，使渲染更為高效。
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 請在 `models.py` 的模型欄位宣告中，填入正確的類別或屬性參數名稱，使其能正確建立一個預設值為 `20` 的整數年齡欄位：
```python
# members/models.py
from django.db import models

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)
    
    # 宣告一個整數欄位，並設定預設值為 20
    age = models.___(1)___(____(2)____=20)
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `IntegerField`
* `(2)`: `default`
</details>

---

### 9. 以下是 `all_members.html` 中用來顯示青少年與成人會員的部分程式碼，請填入正確的 Django 樣板標籤或關鍵字以完成這個條件過濾與迴圈流程：

```html
<!-- members/templates/all_members.html -->
{% extends "master.html" %}

{% block content %}
  <h3>Young Members (age < 20)</h3>
  <ul>
    <!-- 1. 開始巡覽所有會員 -->
    ___(1)___ x in mymembers %}
      <!-- 2. 判斷年齡是否小於 20 -->
      {% ___(2)___ x.age < 20 %}
        <li><a href="details/{{ x.id }}">{{ x.firstname }}</a>, {{ x.age }}</li>
      <!-- 3. 結束條件判斷 -->
      ___(3)___
    {% endfor %}
  </ul>

  <h3>Adult Members (age >= 20)</h3>
  <ul>
    {% for x in mymembers %}
      {% if x.age >= 20 %}
        <li><a href="details/{{ x.id }}">{{ x.firstname }}</a>, {{ x.age }}</li>
      <!-- 4. 結束條件判斷 -->
      ___(4)___
    {% endfor %}
  </ul>
{% endblock %}
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `{% for`
* `(2)`: `if`
* `(3)`: `{% endif %}`
* `(4)`: `{% endif %}`

**解析**：
* 樣板中進行集合迴圈的開頭為 `{% for 變數 in 集合 %}`。
* 條件判斷的語法為 `{% if 條件式 %}`，並且必須有對應的結束標籤 `{% endif %}` 關閉區塊。
</details>
