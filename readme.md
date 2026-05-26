# version validation

在 form 物件中，加上驗證的邏輯程式碼

[/courts/models.py](/courts/models.py)
* `Booking` 的類別，加上 `reason` 的欄位，用來描述預約的目的

[/courts/forms.py](/courts/forms.py)
* `BookingForm` 也同步加上 `reason` 的設定，特別是加上 `clean_reason(self)` 的方法用來檢查 reason 輸入是否超過 10 個字。
* `clean_xxx()` 表示要對 `xxx` 欄位進行檢查
    * `reason = self.cleaned_data.get('reason')` 會對使用者輸入的資料進行清理，例如前置空白或是不安全的程式碼。大家可以輸入 `    this is a test, many space before the text   ` 來進行測試-- 輸入後前置空白會被清掉。
    * 我們要求使用者輸入的理由不可以少於 10 個字，所以做 `len(reason) <= 10` 的檢查。如果使用者違反，會產出 `ValidationError` 的錯誤。

[/courts/views.py](/courts/views.py)
* `booking_form.is_valid()` 會呼叫所有 `clean_xxx()` 方法。
    * 如果驗證通過（第 46 行）：儲存預約，並設定 `result = '預約成功！'`、`success = True`。
    * 如果驗證失敗（第 51 行）：使用 `booking_form.errors.as_text()` 取得錯誤訊息，設定 `result = '預約失敗：...'`、`success = False`。
* 不論成功或失敗，都將 `result`、`success`、`booking_form` 包進 `context`，傳給 `booking_result.html`。

[/courts/templates/booking_result.html](/courts/templates/booking_result.html)
* 透過 `{% if success %}` 來判斷預約是否成功，成功顯示 🎉，失敗顯示 😞。
* 透過 `{% if success %}` 來判斷預約是否成功，成功顯示 🎉，失敗顯示 😞。
* 透過 `{{ result }}` 顯示結果訊息（成功文字或包含錯誤詳情的失敗訊息）。

---

## 🏋️ 課堂練習

### 練習一：限制預約日期不得為過去的日期

**目標**：在 `BookingForm` 中加入對 `date` 欄位的驗證，確保使用者不能預約過去的日期。

**提示**：
* 在 [/courts/forms.py](/courts/forms.py) 的 `BookingForm` 中，仿照 `clean_reason()` 的做法，新增一個 `clean_date()` 方法。
* 在方法中使用 `self.cleaned_data.get('date')` 取得使用者輸入的日期。
* 與 `date.today()` 進行比較，若日期早於今天，則拋出 `ValidationError`。

```python
def clean_date(self):
    selected_date = self.cleaned_data.get('date')
    # 請在此補上驗證邏輯
    return selected_date
```

---

### 練習二：驗證成員電話號碼格式

**目標**：在成員登錄資料中，要求 `phone` 欄位的格式必須只能包含數字與 `-`，例如 `0912-345-678`。

**提示**：
* 先為 `Member` 建立一個 `MemberForm`，放在 [/members/forms.py](/members/forms.py)（需新增此檔案）。
* 在 `MemberForm` 中新增 `clean_phone()` 方法。
* 可以使用 Python 的 `re` 模組（正則表達式）來驗證格式：

```python
import re

def clean_phone(self):
    phone = self.cleaned_data.get('phone')
    if not re.match(r'^[\d\-]+$', phone):
        raise ValidationError('電話號碼只能包含數字與「-」符號')
    return phone
```