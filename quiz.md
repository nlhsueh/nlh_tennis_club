# 🎾 Django MVT 基礎課堂隨堂測驗 (Quiz)

本測驗旨在檢驗學生對於本單元（`member` 分支：Django Model、Migration、Django Shell 資料操作與 MVT 基本資料渲染）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 關於 Django Model 的宣告與設計，下列哪一個敘述是正確的？
* (A) 所有 Model 類別必須繼承自 `models.BaseModel`。
* (B) `CharField`（字串欄位）型態在宣告時，`max_length` 為必填的參數。
* (C) 在 Django 設計 Model 時，不一定要繼承任何父類別。
* (D) `__str__` 方法主要是用來設定資料欄位的最大限制長度。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* (A) 錯誤：必須繼承自 `models.Model`。
* (B) 正確：`CharField` 在 Django 中要求必須明確定義最大字元長度限制 `max_length`。
* (C) 錯誤：必須繼承 `models.Model` 才能擁有資料庫對應與 ORM 功能。
* (D) 錯誤：`__str__` 是 Python 的內建特殊方法，用來定義當該物件被轉為字串或在後台顯示時的呈現格式（例如直接印出人名）。
</details>

---

### 2. 當變更了 `models.py` 的資料庫欄位設計後，要將這個變更套用到本地資料庫，需要依序執行哪兩個 Django 命令？
* (A) `python manage.py runserver` ➡️ `python manage.py migrate`
* (B) `python manage.py makemigrations` ➡️ `python manage.py runserver`
* (C) `python manage.py makemigrations` ➡️ `python manage.py migrate`
* (D) `python manage.py shell` ➡️ `python manage.py migrate`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* 步驟一：執行 `makemigrations` 分析 Model 的異動，並在該 App 的 `migrations/` 資料夾下生成遷移說明檔（.py 藍圖檔）。
* 步驟二：執行 `migrate` 將這些生成的遷移檔案實際執行並套用到資料庫，正式變更資料庫 Table 的結構。
</details>

---

### 3. 在 Django Shell 環境中，要查詢 `Member` 資料表中所有資料的詳細屬性與對應的值（會傳回一個包含欄位字典的 QuerySet 集合），應使用下列哪一個指令？
* (A) `Member.objects.all()`
* (B) `Member.objects.all().values()`
* (C) `Member.all_values()`
* (D) `Member.objects.get_values()`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* `Member.objects.all()` 會傳回一個包含 Member 物件實例的 QuerySet，顯示格式由 `__str__` 定義。
* 串接 `.values()` 後，會將資料庫中每一筆紀錄的各欄位名稱與實際儲存值轉換為 Dict (字典) 格式傳回（例如 `{'id': 1, 'firstname': 'Alice', 'lastname': 'Wang'}`），這也是本單元 View 傳遞給前端最常使用的資料格式。
</details>

---

### 4. 關於 View 將資料傳遞給 Template 的機制，下列敘述何者錯誤？
* (A) 我們通常使用 Python `dict` (字典) 的結構來包裝要傳給模板的參數，這個變數通常稱為 `context`。
* (B) 透過 `loader.get_template('all_members.html')` 可以載入指定的 HTML 模板檔案。
* (C) `template.render(context, request)` 的作用是將 context 內的變數渲染到 HTML 模板中，產出網頁字串。
* (D) 由於傳入模版的字典鍵值（Key）會直接成為模板變數的名稱，因此 `context` 字典的鍵值（Key）可以使用任何資料型態（包含數字與物件）。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**Correct Answer**: **(D)**

**解析**：
* `context` 的鍵值（Key）必須是 **字串 (String)** 型態，因為它會直接轉換為 HTML 模版中的樣板變數名稱（如 `mymembers`）。如果使用非字串作為 Key，模版引擎在解析時將會無法對應而導致找不到變數。其他 (A), (B), (C) 選項的敘述均為完全正確的 MVT 資料串接流程。
</details>

---

### 5. 關於 Django 模板（Template）的語法，下列哪一組符號被稱為「樣板標籤 (Template Tag)」，常用於控制流（如迴圈、條件分支判斷等）？
* (A) `{{ ... }}`
* (B) `{% ... %}`
* (C) `{# ... #}`
* (D) `[* ... *]`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* `{% ... %}` 被稱為樣板標籤 (Template Tag)，常用於控制邏輯，如迴圈 `{% for x in mymembers %}` 或判斷 `{% if x.age > 20 %}` 等。
* `{{ ... }}` 用於輸出具體的樣板變數值 (Template Variable)。
* `{# ... #}` 用於撰寫模版內的註解 (Comments)。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請簡述 `python manage.py makemigrations` 與 `python manage.py migrate` 兩者在功能上的根本不同點。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
* **`makemigrations`**：分析 `models.py` 的變動，在記憶體中比對先前的資料庫狀態，並在該 App 下的 `migrations/` 目錄中建立一個**遷移描述檔案（遷移藍圖 .py 檔案）**。此指令**並不會**對本地的實際資料庫（如 `db.sqlite3`）進行任何結構修改。
* **`migrate`**：實際讀取 `migrations/` 底下所有尚未套用的遷移檔案，並在本地資料庫（如 SQLite、PostgreSQL）上**執行 SQL 指令**，正式建立、刪除或修改資料表（Table）與欄位，使資料庫結構與模型的宣告達成完全一致。
</details>

---

### 7. 如果想要在 Django Shell 環境中，直接執行一個現成的自訂外部 Python 指令碼（例如批次新增會員資料的腳本 `add_members.py`），應在 shell 中輸入什麼 Python 代碼？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
```python
exec(open('add_members.py').read())
```
**解析**：
此指令會開啟指定路徑下的實體檔案，讀取其程式碼字串，並利用 Python 內建的 `exec()` 函式直接在當前已載入 Django 環境的 Shell 內運行，是批次快速匯入或清洗資料時非常實用的指令。
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 在 `members/views.py` 中，我們需要將所有的會員物件詳細資料傳遞給前端網頁模板。請在下列程式碼的空缺處（標示為 `___(1)___`、`___(2)___`、`___(3)___`）填入正確的 Django ORM 或視圖元件代碼：

```python
from django.http import HttpResponse
from members.models import Member
from django.template import loader

def members(request):
    mymembers = Member.objects.all().___(1)___()
    template = loader.___(2)___('all_members.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.___(3)___(context, request))
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `values`
* `(2)`: `get_template`
* `(3)`: `render`

**完整程式碼呈現**：
```python
def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('all_members.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))
```
</details>

---

### 9. 在 `all_members.html` 網頁模板中，我們希望用一個 HTML 無序清單 `<ul>` 迴圈列出所有會員的名（firstname）與姓（lastname）。請在下列 HTML 模板的空缺處（標示為 `___(1)___`、`___(2)___`、`___(3)___`、`___(4)___`）填入正確的 Django 模板引擎專屬標籤或變數符號：

```html
<ul>
  ___(1)___ for x in mymembers ___(2)___
    <li>___(3)___ x.firstname ___(4)___ {{ x.lastname }}</li>
  {% endfor %}
</ul>
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `{%`
* `(2)`: `%}`
* `(3)`: `{{`
* `(4)`: `}}`

**完整 HTML 呈現**：
```html
<ul>
  {% for x in mymembers %}
    <li>{{ x.firstname }} {{ x.lastname }}</li>
  {% endfor %}
</ul>
```
</details>
