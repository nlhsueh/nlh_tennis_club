## Django MVT 基礎課堂隨堂測驗 — Form 欄位自訂驗證 (Quiz)

本測驗旨在檢驗學生對於本單元（`validation` 分支：Django Form 欄位清理與驗證機制、自訂 `clean_<fieldname>` 方法、`ValidationError` 拋出、`is_valid()` 調用流程、以及前端錯誤訊息渲染）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 關於 Django 中自訂 Form 的欄位驗證方法（例如本單元的 `clean_reason(self)`），下列敘述何者正確？
* (A) 該驗證方法可以隨意命名，例如 `validate_reason(self)`，Django 在表單提交時會自動掃描並執行。
* (B) 驗證方法必須回傳一個布林值（`True` 或 `False`），以代表該欄位是否通過驗證。
* (C) 驗證成功後，驗證方法**必須**將經過清理或檢查後的該欄位值（如 `reason`）回傳，否則該欄位值在表單的 `cleaned_data` 中會遺失（變為 `None`）。
* (D) 如果驗證失敗，應直接在方法中使用 `print()` 印出錯誤訊息，Django 就會自動向瀏覽器發送 500 內部伺服器錯誤。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* Django 在執行表單驗證時，會依序調用 `clean_<fieldname>()` 方法。該方法在驗證通過後，**必須**將經過清洗或檢查後的欄位值回傳（`return`）。
* 如果忘記回傳（或回傳 `None`），Django 會將 `cleaned_data` 中該欄位的值覆蓋為 `None`，進而導致儲存時發生錯誤。
* (A) 錯，命名必須遵循嚴格的 `clean_<fieldname>` 格式。
* (B) 錯，應回傳欄位的值，而不是布林值。
* (D) 錯，驗證失敗時，必須拋出 `ValidationError` 例外。
</details>

---

### 2. 當我們在 `views.py` 中呼叫 `if booking_form.is_valid():` 時，Django 表單系統內部會自動執行哪些動作？
* (A) 它只會檢查前端 HTML 是否有設定 `required` 屬性，不會執行任何後端 Python 邏輯。
* (B) 它會先將使用者輸入的原始資料進行初步清洗，再依序調用表單中定義的所有 `clean_<fieldname>()` 與 `clean()` 方法，最後回傳一個布林值指出表單資料是否完全合格。
* (C) 它會直接執行 `booking_form.save()` 將資料寫入資料庫，如果資料庫拋出異常才回傳 `False`。
* (D) 它會清除所有先前的使用者輸入，使表單恢復成空白表單狀態。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* `is_valid()` 是 Django 表單驗證的總開關。呼叫它時，會觸發後端的驗證管道（Validation Pipeline）：
  1. 清理各個欄位的資料類型（轉換為對應的 Python 物件）。
  2. 依序執行各別欄位的自訂驗證方法 `clean_<fieldname>()`。
  3. 執行全表單跨欄位驗證方法 `clean()`。
  4. 若無任何錯誤，則回傳 `True`，並將乾淨的資料填入 `cleaned_data` 中；若有錯誤，則回傳 `False`，並將錯誤存入 `errors`。
</details>

---

### 3. 在 Django 視圖（View）函數的宣告上方，加上 `@login_required` 裝飾器（Decorator）的主要作用是什麼？
* (A) 限制只有特定系統管理員（Superuser）才能使用此網頁。
* (B) 強制要求該視圖必須以 HTTPS 加密協議來傳輸資料。
* (C) 限制只有已登入（Authenticated）的使用者才能訪問該頁面。匿名使用者訪問時，會自動被重導向至登入頁面（通常是 `/accounts/login/`）。
* (D) 在後台自動註冊該預約路由，避免其他人盜用。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* `@login_required` 是 Django 內建的安全裝飾器，用來阻擋未登入的訪客訪問敏感頁面。
* 當未登入的使用者試圖存取該頁面時，它會自動將頁面導向至 `settings.py` 中設定的 `LOGIN_URL`，並在 URL 中帶上 `?next=當前頁面路徑`，以便使用者登入後自動導回原頁面。
</details>

---

### 4. 當表單欄位驗證失敗，我們在自訂驗證方法中拋出了 `raise ValidationError(...)`。請問在 HTML 模板（如 `booking_result.html`）中，我們該如何取得並顯示這些欄位的錯誤訊息？
* (A) 透過 `{{ booking_form.errors }}` 或 `{{ booking_form.reason.errors }}` 取得。
* (B) 透過 `{{ request.GET.error_message }}` 取得。
* (C) 透過 `{{ booking_form.clean_reason }}` 直接渲染出錯誤。
* (D) 透過 `{{ result.errors }}` 取得。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(A)**

**解析**：
* 當表單驗證失敗時，所有的錯誤訊息都會被打包收集在 Form 物件的 `errors` 屬性中。
* 我們可以透過 `{{ form.errors }}` 列出全表單的所有錯誤；或者在前端輸入欄位旁邊，使用 `{{ form.<fieldname>.errors }}` 精準地渲染該欄位的專屬錯誤訊息，提供良好的使用者體驗。
</details>

---

### 5. 觀察 `courts/forms.py` 中取得使用者輸入並清理資料的程式碼：
```python
reason = self.cleaned_data.get('reason')
```
關於 **`self.cleaned_data`** 字典，下列敘述何者正確？
* (A) 它包含的是使用者提交的原始 HTTP POST 字串，完全沒有進行任何格式轉換。
* (B) 只有當表單欄位通過了 Django 預設與自訂的基礎清洗與驗證後，該欄位的值才會被放入 `cleaned_data` 中。
* (C) 它是唯讀的，我們不可以在任何驗證方法中修改其中的值。
* (D) 如果使用者在表單中完全沒有填寫該欄位（且欄位非必填），`cleaned_data` 會直接拋出 `KeyError` 異常。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* `cleaned_data` 是儲存「乾淨資料」的字典。只有當欄位通過類型檢查、長度限制以及 `clean_<fieldname>()` 的基本驗證後，該欄位的值才會以適當的 Python 類型放入此字典中。
* 若欄位驗證失敗，它將不會出現在 `cleaned_data` 中（或為 `None`）。因此在跨欄位驗證時，建議使用 `.get('fieldname')` 來安全地獲取值，避免拋出 `KeyError` 異常。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請詳細說明：在 `BookingForm` 中自訂的 `clean_reason(self)` 函數內，`ValidationError` 是如何產生的？當此例外被拋出後，Django 會如何處置這個錯誤訊息，並使它出現在前端網頁中？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **產生例外**：在 `clean_reason` 中，我們藉由 `len(reason) <= 10` 判斷使用者的輸入是否小於等於 10 個字。若是，則會執行 `raise ValidationError('用途必須超過 10 個字元...')`，主動拋出驗證錯誤例外。
2. **收集錯誤**：當 View 呼叫 `is_valid()` 時，Django 表單系統會自動捕獲這個 `ValidationError` 例外，將其錯誤訊息打包放入表單的 `errors` 字典中（以欄位名稱 `reason` 為 key），並將表單判定為不合格（`is_valid()` 回傳 `False`）。
3. **前端渲染**：因為驗證失敗，View 將含有錯誤狀態的 `booking_form` 傳遞回模板進行渲染。在 HTML 中，我們可以使用 `{{ booking_form.reason.errors }}` 動態輸出對應的錯誤紅字，提醒使用者修改。
</details>

---

### 7. 本單元介紹了「延伸練習題一：過濾敏感或測試字詞」的設計。請寫出您將如何修改 `clean_reason` 的實作，使得當 `reason` 中包含 `'test'`、`'demo'`、`'測試'` 或 `'範例'` 等測試用字時，會觸發驗證失敗並顯示錯誤訊息？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
我們可以在 `clean_reason(self)` 中獲取 `reason` 欄位值後，使用一個禁止關鍵字清單進行遍歷判定，若包含則拋出 `ValidationError`：
```python
def clean_reason(self):
    reason = self.cleaned_data.get('reason')
    if not reason:
        raise ValidationError('預約原因不能為空。')
    if len(reason) <= 10:
        raise ValidationError(f'用途必須超過 10 個字元（至少 11 字）。')
        
    # 練習題一：關鍵字檢查
    forbidden_words = ['test', 'demo', '測試', '範例']
    reason_lower = reason.lower() # 轉小寫以進行不分大小寫檢查
    for word in forbidden_words:
        if word in reason_lower:
            raise ValidationError(f'預約原因不能包含測試或範例字詞（如 {word}）。')
            
    return reason
```
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 請在 `forms.py` 的表單自訂驗證方法中，填入正確的 Django 方法、例外類別或變數，使其能夠成功檢驗「用途（reason）必須大於 10 個字元（至少 11 字）」：
```python
# courts/forms.py
from django import forms
from django.forms import ___(1)___ # 1. 引入驗證錯誤類別

class BookingForm(forms.ModelForm):
    # ... 欄位 Meta 設定省略 ...

    def clean_reason(self):
        # 2. 從已清理的資料字典中取得 'reason' 的值
        reason = self.cleaned_data.___(2)___('reason')
        
        if not reason:
            raise ___(1)___('預約原因不能為空。')
            
        # 3. 檢查長度是否小於等於 10 個字
        if ___(3)___(reason) <= 10:
            # 拋出驗證失敗訊息
            raise ___(1)___('用途必須超過 10 個字元（至少 11 字）。')
            
        # 4. 驗證成功，必須將該值回傳
        ___(4)___ reason
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `ValidationError`
* `(2)`: `get`
* `(3)`: `len`
* `(4)`: `return`
</details>

---

### 9. 以下是 `courts/views.py` 中處理預約表單提交的 `booking` 視圖函數。請在填充處填入正確的屬性、方法或裝飾器以完成這套表單驗證與儲存的控制流：
```python
# courts/views.py
from django.contrib.auth.decorators import ___(1)___ # 1. 引入要求登入裝飾器
from courts.forms import BookingForm

# 2. 套用裝飾器以確保使用者必須登入才能預約
___(2)___
def booking(request, court_id):
    if request.method == 'GET':
        # 第一次載入空白表單
        booking_form = BookingForm(initial={'court': court_id, 'user': request.user})
        return render(request, 'booking.html', {'booking_form': booking_form})
        
    elif request.method == 'POST':
        # 3. 綁定前端提交的 POST 資料
        booking_form = BookingForm(request.___(3)___)
        
        # 4. 觸發並檢驗表單資料是否完全合法
        if booking_form.___(4)___():
            booking_form.save()
            result = 'Booking ok'
        else:
            result = 'Booking fail'
            
        context = {
            'booking_form': booking_form,
            'result': result
        }
        return render(request, 'booking_result.html', context)
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `login_required`
* `(2)`: `@login_required`
* `(3)`: `POST`
* `(4)`: `is_valid`

**解析**：
1. `login_required` 裝飾器可以限制視圖只能被登入使用者存取。
2. 裝飾器語法在 Python 中使用 `@` 開頭。
3. `request.POST` 用於綁定前端 POST 提交的資料。
4. `is_valid()` 方法會自動觸發並執行所有內建與自訂的清理與驗證管道，如 `clean_reason()`，當且僅當所有驗證都通過時回傳 `True`。
</details>
