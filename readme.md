# version validation

在 form 物件中，加上驗證的邏輯程式碼

[/courts/models.py](/courts/models.py)
* `Booking` 的類別，加上 `reason` 的欄位，用來描述預約的目的

[/courts/forms.py](/courts/forms.py)
* `BookingForm` 也同步加上 `reason` 的設定，特別是加上 `clean_reason(self)` 的方法用來檢查 reason 輸入是否超過 10 個字（至少 11 個字）。
* `clean_xxx()` 表示要對 `xxx` 欄位進行檢查
    * `reason = self.cleaned_data.get('reason')` 會對使用者輸入的資料進行清理，例如前置空白或是不安全的程式碼。大家可以輸入 `    this is a test, many space before the text   ` 來進行測試-- 輸入後前置空白會被清掉。
    * 我們要求使用者輸入的理由不可以少於 10 個字，所以做 `len(reason) <= 10` 的檢查。如果使用者違反，會產出 `ValidationError` 的錯誤。這可以在 `booking_form.errors` 來呈現。

[/courts/views.py](/courts/views.py)
* `booking_form.is_valid()` 會呼叫所有 `clean_xxx()` 方法。
    * 如果驗證通過（第 46 行）：儲存預約，並設定 `result = '預約成功！'`、`success = True`。
    * 如果驗證失敗（第 51 行）：使用 `booking_form.errors.as_text()` 取得錯誤訊息，設定 `result = '預約失敗：...'`、`success = False`。
* 不論成功或失敗，都將 `result`、`success`、`booking_form` 包進 `context`，傳給 `booking_result.html`。

[/courts/templates/booking_result.html](/courts/templates/booking_result.html)
* 透過 `{% if success %}` 來判斷預約是否成功，成功顯示 🎉，失敗顯示 😞。
* 透過 `{% if booking_form.errors %}` 來檢查是否有錯誤，有的話就印出。
* 透過 `{{ result }}` 顯示結果訊息（成功文字或包含錯誤詳情的失敗訊息）。

---

## 🏋️ 課堂練習與延伸練習題 (Classroom Exercises)

以下提供了四個非常適合在課堂上進行的欄位驗證練習題，供學生實作以深化對 Django Form 驗證與自訂規則的理解：

### 練習題一：限制預約日期不得為過去的日期（基本日期驗證）
* **題目說明**：目前系統允許使用者預約過去的日期。請修改驗證邏輯，當使用者選擇的預約日期早於今天（系統當前日期）時，表單應該驗證失敗並顯示錯誤訊息：「預約日期不能是過去的日期」。
* **引導提示**：
    1. 前往 [/courts/forms.py](/courts/forms.py) 修改 `BookingForm`。
    2. 新增一個 `clean_date(self)` 方法來驗證 `date` 欄位。
    3. 使用 `self.cleaned_data.get('date')` 取得輸入日期，並與當前日期 `date.today()` 進行比較。
    4. 若輸入日期小於今天，拋出 `ValidationError` 錯誤。
    ```python
    def clean_date(self):
        selected_date = self.cleaned_data.get('date')
        # 請在此補上驗證邏輯，小於今天則拋出 ValidationError
        return selected_date
    ```

### 練習題二：驗證成員電話號碼格式（自訂格式驗證）
* **題目說明**：在成員登錄資料中，要求 `phone` 欄位的格式必須只能包含數字與 `-`，例如 `0912-345-678`。
* **引導提示**：
    1. 為 `Member` 建立一個 `MemberForm`，放在 [/members/forms.py](/members/forms.py)（需新增此檔案）。
    2. 在 `MemberForm` 中新增 `clean_phone()` 方法。
    3. 可以使用 Python 的 `re` 模組（正規表示式）來驗證格式：
    ```python
    import re
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^[\d\-]+$', phone):
            raise ValidationError('電話號碼只能包含數字與「-」符號')
        return phone
    ```

### 練習題三：過濾敏感或測試字詞（理由內容檢查）
* **題目說明**：目前使用者可以隨意輸入無效的預約理由（例如：只輸入 `"testtesttest"` 或 `"測試測試測試測試"`）。請修改驗證邏輯，當使用者的預約原因包含 `test`、`demo`、`測試` 或 `範例` 等無效測試關鍵字時，表單應該驗證失敗並顯示錯誤訊息：「預約原因不能包含測試或範例字詞（如 test, demo, 測試, 範例）」。
* **引導提示**：
    1. 前往 [/courts/forms.py](/courts/forms.py) 修改 `BookingForm` 的 `clean_reason(self)` 方法。
    2. 定義一個禁止關鍵字清單，例如 `forbidden_words = ['test', 'demo', '測試', '範例']`。
    3. 檢查使用者輸入的 `reason`（轉為小寫）中是否包含任何禁止關鍵字，若有則 `raise ValidationError(...)`。

### 練習題四：限制只能預約 30 天以內的日期（日期範圍檢查）
* **題目說明**：目前使用者可以預約任意未來的日期（例如預約明年）。請限制使用者最多只能預約自今天起算 **30 天以內** 的日期。若選擇的日期超過今天加 30 天，表單應驗證失敗並顯示錯誤訊息：「預約日期最多只能是自今天起算 30 天以內的日期」。
* **引導提示**：
    1. 前往 [/courts/forms.py](/courts/forms.py) 修改 `BookingForm` 的 `clean_date(self)` 方法。
    2. 透過 `datetime.timedelta(days=30)` 計算出 30 天後的上限日期。
    3. 比對使用者輸入的日期，若大於上限日期，則 `raise ValidationError(...)`。