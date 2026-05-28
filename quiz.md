## Django MVT 基礎課堂隨堂測驗 — Form POST 新增會員 (Quiz)

本測驗旨在檢驗學生對於本單元（`form_post` 分支：Django ModelForm 應用、POST 表單提交機制、資料驗證與儲存、以及 CSRF 安全防護機制）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 關於 Django 中的 `ModelForm`，下列敘述何者正確？
* (A) `ModelForm` 與普通 `Form` 相同，無法直接將使用者填寫的表單資料儲存進資料庫，仍需手動撰寫 SQL 或將資料填入 Model 物件中。
* (B) `ModelForm` 需要定義一個內嵌類別 `class Meta`，其中必須包含 `model` 屬性來指定關聯的 Model，以及 `fields` 屬性指定要在表單中呈現的欄位。
* (C) 在 `class Meta` 中，`fields = "__all__"` 的作用是「排除」所有的 Model 欄位，不讓它們呈現在網頁表單中。
* (D) 如果在 `ModelForm` 中修改了 `widgets` 或 `labels`，我們必須在終端機中執行 `makemigrations` 來進行資料庫結構遷移。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* `ModelForm` 需要透過巢狀的 `Meta` 類別來設定綁定的 `model` 與要包含的欄位 `fields`，這是它的標準設計結構。
* (A) 錯，`ModelForm` 提供非常便捷的 `.save()` 方法，可直接將經過驗證的表單資料寫入資料庫。
* (C) 錯，`__all__` 代表「包含」所有該 Model 的欄位。
* (D) 錯，修改 widgets、labels 等僅影響 HTML 前端的渲染樣式與說明標籤，不涉及資料庫結構變動，因此不需要進行 migration。
</details>

---

### 2. 在使用 `ModelForm` 來新增資料的 View 函數中，我們通常會這樣寫：
```python
new_member_form = NewMemberForm(request.POST)
```
請問傳入的 **`request.POST`** 主要用途是什麼？
* (A) 它是用來告訴瀏覽器，下一個頁面要跳轉至 POST 的目的地。
* (B) 它是 Django 自動從資料庫中拉取的最新資料，用來填補表單中的空白。
* (C) 它是一個包含使用者在前端表單中透過 POST 方法提交之所有資料的 QueryDict 物件，我們將其傳遞給 `NewMemberForm` 用於資料綁定與後續的驗證。
* (D) 它是用來啟用 CSRF 安全驗證機制的加密金鑰。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* `request.POST` 包含用戶提交的所有 POST 欄位資料。
* 將其傳入 `NewMemberForm(request.POST)` 會將這些前端傳回的資料與表單欄位進行「綁定（Binding）」，如此一來表單才能執行資料格式的檢查（驗證）並調用 `save()` 方法儲存。
</details>

---

### 3. 在 Django 專案中，當表單改用 `POST` 方法傳送資料時，我們必須在 HTML `<form>` 標籤內加上 `{% csrf_token %}` 標籤。請問其最核心的作用是什麼？
* (A) 加速表單的網頁傳輸與渲染效率。
* (B) 防範跨站請求偽造（Cross-Site Request Forgery, CSRF）安全攻擊，確保該 POST 請求是來自我們網站本身的表單。
* (C) 用來自動檢查表單的必填欄位是否為空白。
* (D) 將表單中的資料自動加密，使得資料庫中的敏感資料也呈現加密狀態。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* `{% csrf_token %}` 會在渲染的表單中自動插入一個隱藏的 `<input type="hidden" name="csrfmiddlewaretoken" ...>` 欄位，內含一個隨機生成的 token 字串。
* 當表單提交時，Django 伺服器會比對請求中的 token 與使用者瀏覽器 Cookie 中的 token 是否一致，若不符則會拒絕該 POST 請求（回傳 403 Forbidden 錯誤），藉此防範跨站請求偽造攻擊。
</details>

---

### 4. 當使用者填寫好欄位並按下 Submit 按鈕，POST 請求送至 View，下列哪一個 `ModelForm` 的方法被呼叫後，會負責「執行資料驗證（如檢查長度、型態、必填等）」？
* (A) `new_member_form.is_valid()`
* (B) `new_member_form.save()`
* (C) `new_member_form.errors.as_data()`
* (D) `new_member_form.clean_all()`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(A)**

**解析**：
* **`is_valid()`** 負責觸發並執行所有欄位的資料驗證。
* 如果所有的欄位都符合設定的規則（例如沒有留空必填欄位、字數長度正確等），`is_valid()` 會回傳 `True`，同時會將經過整理的乾淨資料放入 `cleaned_data` 屬性中；否則會回傳 `False`，並將錯誤訊息記錄在 `errors` 中。
</details>

---

### 5. 關於 CSRF 攻擊（Cross-Site Request Forgery，跨站請求偽造），下列哪一個描述「不是」此種安全攻擊成功發生的必要條件或關鍵？
* (A) 使用者必須曾經登入過目標信任網站（如銀行 `A.com`），且在瀏覽器中存有該網站有效的認證 Cookie（憑證）。
* (B) 使用者在尚未登出 A 網站的情況下，在同一個瀏覽器中點擊了駭客設計的惡意連結或造訪了惡意網站 `B.com`。
* (C) 惡意網站 `B.com` 在背景發送了指向 `A.com` 的請求，而使用者的瀏覽器在發送請求時，自發性地附帶了使用者在 `A.com` 的有效 Cookie。
* (D) 駭客必須事先駭入使用者的電腦，或者在背景監聽並竊取到使用者 Cookie 中儲存的明文帳號與密碼。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(D)**

**解析**：
* 在 CSRF 攻擊中，駭客**並不需要**知道或竊取 Cookie 的內容，也不需要知道密碼。
* 攻擊能成功的核心原因在於「瀏覽器的安全機制會自動在發送請求給某個網域（如 `A.com`）時，夾帶該網域在瀏覽器中已存有的 Cookie」。
* 因此，駭客只需誘騙使用者造訪其控制的 `B.com`，並在背景以使用者的名義對 `A.com` 發送惡意請求（例如轉帳、新增管理員），A 網站接收後由於偵測到正確的認證 Cookie，便會誤以為這是使用者的正常操作而執行。這也是為什麼 Django 必須設計 CSRF token 驗證來防範此問題。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請詳細說明在 `new_member` View 函數中，我們是如何將「GET 請求（顯示表單）」與「POST 請求（處理提交與儲存）」整合在同一個 View 裡的？請簡述其資料流向。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **GET 請求流程（顯示表單）**：
   - 當使用者點選連結或存取 `/members/new_member` 時，發送的是 `GET` 請求，程式進入 `if request.method == 'GET':` 分支。
   - View 函數會實例化一個**空白**的 `NewMemberForm()` 物件，將其傳遞給 `new_member.html` 模板，最後渲染出包含輸入框的空白頁面呈現給使用者。
2. **POST 請求流程（處理提交與儲存）**：
   - 使用者填寫資料並按下提交後，瀏覽器以 `POST` 方法將資料發送至同一個網址，程式進入 `elif request.method == 'POST':` 分支。
   - View 透過 `NewMemberForm(request.POST)` 將使用者提交的表單資料與 Form 類別進行「資料綁定（Binding）」。
   - 調用 `is_valid()` 方法對綁定的資料進行格式驗證。
   - **驗證成功**：調用 `save()` 將新會員資料直接存入資料庫，並設定成功訊息。
   - **驗證失敗**：將錯誤細節擷取下來，最後將結果渲染至 `new_member_result.html` 頁面顯示給使用者。
</details>

---

### 7. 請解釋 `ModelForm` 中的 `Meta` 內嵌類別內，`model`、`fields`、`widgets` 和 `labels` 屬性各自的用途是什麼？並以本單元的 `NewMemberForm` 為例說明。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
* **`model`**：用來指定此 `ModelForm` 是與哪一個資料庫模型（Model）相綁定。在本例中指定綁定 `Member`。
* **`fields`**：用來指定哪些 Model 欄位需要呈現在前端網頁表單中。本例中使用 `"__all__"`，代表將 `Member` 的所有欄位（如 `firstname`, `lastname`, `phone`, `joined_date`）都列入表單。
* **`widgets`**：用來客製化表單欄位在前端渲染出來的 HTML 表單元件（如 Input、Select 等）。本例中將 `joined_date` 欄位預設的單一文字框，改為使用 `forms.SelectDateWidget`（三個下拉選單分別選擇年、月、日），並設定預設值屬性為今天。
* **`labels`**：用來客製化特定欄位對應的中文標籤說明文字。本例中將 `joined_date` 欄位的前端標籤文字改為更容易閱讀的 `'加入日期'`。
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 請在 `forms.py` 的 `NewMemberForm` 宣告中填入適當的屬性，使其能正確建立一個與 `Member` 模型綁定的 `ModelForm`，且包含所有欄位，並將 `joined_date` 欄位的 Label 設定為 `'加入日期'`：
```python
# members/forms.py
from django import forms
from .models import Member

class NewMemberForm(forms.___(1)___):
    class ___(2)___:
        # 指定綁定的 model
        model = ___(3)___
        
        # 包含所有 Model 欄位
        fields = ___(4)___
        
        # 客製化 label
        labels = {
            'joined_date': '加入日期'
        }
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `ModelForm`
* `(2)`: `Meta`
* `(3)`: `Member`
* `(4)`: `"__all__"` (或 `'__all__'`)
</details>

---

### 9. 以下是 `new_member` View 函數與 `new_member.html` 模板的部分程式碼。請填入正確的 Django 屬性、方法或安全標籤以完成這套新增會員的流程：

```python
# members/views.py
def new_member(request):
  if request.method == 'GET':
    new_member_template = loader.get_template('new_member.html')
    # 第一次載入空白表單
    context = {'form': NewMemberForm()}
    return HttpResponse(new_member_template.render(context, request))
  elif request.method == 'POST':
    # 1. 綁定用戶 POST 提交的資料
    new_member_form = NewMemberForm(request.___(1)___)
    
    # 2. 驗證資料是否合法
    if new_member_form.___(2)___():
        # 3. 將資料儲存至資料庫
        new_member_form.___(3)___()
        result = 'Add a new member successfully'
    else:
        result = new_member_form.errors.as_data()
```

```html
<!-- members/templates/new_member.html -->
<h1>新增網球俱樂部會員</h1>
<form action="" method="POST">
  <!-- 4. 加入防範 CSRF 攻擊的安全 Token -->
  ___(4)___
  
  {{ form.as_p }}
  <input type="submit" value="Submit">
</form>
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `POST`
* `(2)`: `is_valid`
* `(3)`: `save`
* `(4)`: `{% csrf_token %}`

**解析**：
1. `request.POST` 用於取得前端以 POST 表單提交的資料字典（QueryDict）。
2. `is_valid()` 是表單執行驗證的核心方法，回傳布林值。
3. `save()` 是 `ModelForm` 特有的便捷方法，可以直接將表單輸入寫入對應的模型並儲存至資料庫，不需手動一個個欄位賦值。
4. 為了防止跨站請求偽造（CSRF），任何 Django 中的 POST 表單內都**必須**寫上 `{% csrf_token %}`。
</details>
