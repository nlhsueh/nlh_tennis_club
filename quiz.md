## Django MVT 基礎課堂隨堂測驗 — Form GET 查詢會員 (Quiz)

本測驗旨在檢驗學生對於本單元（`form_get` 分支：Django Form 基礎、GET 表單提交機制、QueryDict 處理與 Django ORM 條件篩選）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 關於 Django 中自訂 Form 類別（例如本單元的 `class CheckMemberForm(forms.Form)`），下列敘述何者正確？
* (A) 它必須繼承自 `models.Model` 才能運作。
* (B) 它在模板中被渲染時，會自動產生 `<form>` 開頭標籤以及 `<input type="submit">` 送出按鈕。
* (C) 它是用來定義表單欄位與驗證規則的類別，在 HTML 模板中可以透過 `{{ form.as_p }}` 等方式渲染出輸入欄位。
* (D) 每次修改 Form 類別的欄位後，都必須在終端機執行 `makemigrations` 與 `migrate` 來更新資料庫。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* Django 的 `forms.Form` 主要用於定義表單結構、欄位 HTML 渲染方式以及驗證資料，它並不會自動生成 `<form>` 標籤或提交按鈕，這些需要在 HTML 中手動編寫。
* 普通的 `forms.Form` 不需要與資料庫進行遷移（Migration），因此不需要執行 `migrate`，這與 `models.Model` 不同。
</details>

---

### 2. 在 HTML 模板中，如果我們在 `{{ form }}` 後面呼叫不同的方法，如 `{{ form.as_p }}`、`{{ form.as_table }}` 或 `{{ form.as_ul }}`，它們的主要區別是什麼？
* (A) `as_p` 會將表單轉換為 PDF 格式，`as_table` 會將其轉換為 Excel 表格。
* (B) 它們代表不同的表單發送方式（例如 POST 或 GET）。
* (C) 它們會影響表單欄位在網頁上的 HTML 排版結構（分別包裹在 `<p>`、`<tr>`、`<li>` 標籤中）。
* (D) 它們分別用於不同權限等級的使用者登入表單呈現。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* `as_p` 會將每個欄位和其 Label 包裹在 `<p>` 標籤中；
* `as_table` 會將每個欄位包裹在 HTML 的表格列 `<tr>` 標籤中（因此開發者必須在外面手動加上 `<table>...</table>`）；
* `as_ul` 則會將其包裹在無序列表項目 `<li>` 中（外面需手動加上 `<ul>...</ul>`）。
* 這幾種方法僅影響渲染出來的 HTML 標籤排版。
</details>

---

### 3. 在本單元中，我們使用 GET 方法來設計查詢表單 `<form action="" method="GET">`。關於 GET 方法在表單提交時的特性，下列敘述何者錯誤？
* (A) 表單資料會被附加在 URL 的後半部（如 `?last_name=Smith`），成為 Query String。
* (B) 因為資料會顯眼地顯示在瀏覽器網址列中，所以非常適合用於密碼變更或信用卡結帳等安全性要求高的情境。
* (C) 使用 GET 查詢的結果網址可以被使用者加入書籤（Bookmark），方便下次直接造訪相同的查詢結果頁面。
* (D) 瀏覽器通常會對 GET 的 URL 長度有一定限制，因此不適合用來傳送大量的檔案或超長文字。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* GET 方法的資料會直接暴露在網址列中，且會留在瀏覽器的歷史紀錄、代理伺服器日誌或伺服器日誌中。
* 因此，**絕對不可**將 GET 用於密碼、信用卡、敏感個人資料等安全性要求高的傳輸情境（這類情境應使用 **POST** 請求，並配合 CSRF 保護）。
</details>

---

### 4. 觀察 `views.check_member` 中以下這段程式碼：
```python
def check_member(request):
    if request.method == 'GET':
        if request.GET:
            who_you_input = request.GET['last_name']
            ...
```
當使用者**「第一次透過連結進入查詢頁面」**與**「輸入姓氏並點選 Submit 提交查詢後」**，`request.GET` 的狀態分別為何？
* (A) 第一次載入時為 `None`；提交後為 `'GET'` 字串。
* (B) 第一次載入時為空字典 `{}` 狀態；提交後會包含如 `{'last_name': 'Smith'}` 的 QueryDict 內容。
* (C) 兩者都會因為網址中未帶有路徑參數而拋出 `Http404` 異常。
* (D) 第一次載入時就包含預設的所有會員資料；提交後則變為空。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 當使用者第一次訪問 `/members/check_member` 時，屬於 GET 請求，但網址後方沒有任何 `?key=value` 的查詢參數，此時 `request.GET` 是一個空的 QueryDict（行為類似空字典 `{}`，在布林評估中 `if request.GET` 為 `False`），所以會執行 `else` 的邏輯去渲染空白的表單。
* 當使用者在表單填寫並提交後，網址會變成 `/members/check_member?last_name=Smith`，此時 `request.GET` 含有參數資料，評估為 `True`，進而執行查詢與結果渲染。
</details>

---

### 5. 如果我們想要在 `views.py` 中，找出資料庫中所有姓氏（`lastname` 欄位）剛好等於使用者所輸入變數 `who_you_input` 的會員，應該使用哪一個 Django ORM 查詢語法？
* (A) `Member.objects.get(lastname=who_you_input)`
* (B) `Member.objects.all().filter(lastname=who_you_input)`
* (C) `Member.objects.filter(lastname=who_you_input)`
* (D) `Member.objects.find(lastname=who_you_input)`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* `Member.objects.filter(...)` 是最標準且正確的寫法，會回傳符合條件的 QuerySet（可能包含零個、一個或多個物件）。
* (A) `get(...)` 如果查到多筆或零筆資料時，會直接拋出 `DoesNotExist` 或 `MultipleObjectsReturned` 異常，不適合用在可能有多個同姓會員的查詢。
* (B) 不需要先調用 `all()` 再接 `filter()`，因為 `filter()` 本身就可以直接套用在 manager 上。
* (D) Django ORM 並沒有 `find()` 這個方法。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請詳細說明：為什麼 Django 在處理「查詢（如搜尋會員）」時通常建議使用 `GET` 請求，而在「建立、更新或刪除資料（如新增會員）」時強烈建議使用 `POST` 請求？請從「安全性（Security）」與「冪等性（Idempotency）」的角度分析。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **安全性（Security）**：
   - **GET**：資料直接放在 URL 中，容易被瀏覽器紀錄、留下痕跡，不適合傳輸敏感變更資訊。
   - **POST**：將資料放在 HTTP Request Body 中，不會暴露在網址上，更為安全；且配合 Django 的 `{% csrf_token %}` 機制，可以防範跨站請求偽造（CSRF）攻擊，這是 GET 表單無法原生做到的安全防護。
2. **冪等性（Idempotency）**：
   - **GET 請求是冪等的（Idempotent）**：多次執行同一個 GET 查詢（例如多次搜尋 "Smith"），只會讀取資料，不會對伺服器的狀態或資料庫造成任何副作用。這也讓查詢結果可以被瀏覽器快取、加入書籤與分享。
   - **POST 請求是非冪等的**：每次提交 POST 請求都代表要在伺服器上執行狀態變更（例如新增會員、刷卡付費）。如果重覆執行，會導致重複新增或扣款等嚴重副作用。因此，瀏覽器在使用者嘗試重整 POST 頁面時，通常會跳出「確認重新傳送表單」的警告。
</details>

---

### 7. 請解釋為什麼在 HTML 模板中寫 `<form action="" method="GET">` 時，如果 `action` 屬性留空（`action=""`），表單被提交時會將資料送到哪一個 URL？這樣設計對於我們的 `views.check_member` 處理流程有什麼好處？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **送達的 URL**：當 `action` 屬性為空字串或留空時，瀏覽器會預設將表單提交到**目前當前的頁面 URL**（即 `/members/check_member`）。
2. **設計上的好處**：這樣能將「顯示表單」與「處理表單提交結果」兩個不同的邏輯，完美整合在同一個 URL 與同一個 View 函數中處理：
   - **第一次載入**：偵測到 `request.GET` 為空，View 會直接提供並渲染空白的搜尋表單。
   - **提交搜尋時**：表單送回同一個 View，此時 `request.GET` 帶有資料，View 就能直接讀取變數進行資料庫篩選，並渲染搜尋結果。
   - 這樣做可以大幅簡化 URL 路由（`urls.py`）的配置，並將相關聯的互動邏輯集中在同一個視圖函數中，程式結構更為簡潔。
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 為了設計可以查詢會員的 Form，請在 `forms.py` 中填入正確的類別與欄位宣告，使其能正常運行：
```python
# members/forms.py
from django import ___(1)___

# 建立一個繼承自 Django Form 的搜尋表單類別
class CheckMemberForm(forms.___(2)___):
    # 宣告一個最大長度為 200 的文字輸入欄位來代表姓氏
    last_name = forms.___(3)___(max_length=200)
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `forms`
* `(2)`: `Form`
* `(3)`: `CharField`

**完整設定呈現**：
```python
# members/forms.py
from django import forms

class CheckMemberForm(forms.Form):
    last_name = forms.CharField(max_length=200)
```
</details>

---

### 9. 以下是 `views.check_member` 的邏輯程式碼，請依據填空處（標示為 `___(1)___`、`___(2)___`、`___(3)___`）填入正確的屬性、方法或類別：
```python
# members/views.py
from django.template import loader
from django.http import HttpResponse
from .forms import CheckMemberForm
from members.models import Member

def check_member(request):
    # 1. 檢查 HTTP 請求方法是否為 GET
    if request.___(1)___ == 'GET':
        
        # 2. 判斷 GET 請求中是否包含查詢參數（非第一次空白載入）
        if request.GET:
            # 取得輸入的 last_name 欄位值
            who_you_input = request.GET['last_name']
            
            # 3. 使用 Django ORM 篩選出符合 lastname 欄位的所有會員物件
            members = Member.objects.___(2)___(lastname=who_you_input)
            
            checked_members_page = loader.get_template('checked_members.html')
            context = {
                "lastname": who_you_input,
                "checked_members": members
            }
            return HttpResponse(checked_members_page.render(context, request))
        else:
            # 第一次載入空白查詢頁面
            checking_member_page = loader.get_template('check_member.html')
            context = {
                # 4. 實例化搜尋表單並傳遞給模板
                'form': ___(3)___()
            }
            return HttpResponse(checking_member_page.render(context, request))
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `method`
* `(2)`: `filter`
* `(3)`: `CheckMemberForm`

**解析**：
* `request.method` 用於獲取當前 HTTP 請求方法（皆為大寫字串，如 `'GET'` 或 `'POST'`）。
* `filter()` 是 Django ORM 用於過濾多筆資料的 API，會回傳 QuerySet。
* 為了在模板中使用 Django Form 來動態產生欄位結構，我們必須在後端實例化表單物件：`CheckMemberForm()`。
</details>
