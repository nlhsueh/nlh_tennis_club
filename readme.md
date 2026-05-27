# version validation

在 form 物件中，加上驗證的邏輯程式碼

[/courts/models.py](/courts/models.py)
* `Booking` 的類別，加上 `reason` 的欄位，用來描述預約的目的

[/courts/forms.py](/courts/forms.py)
* `BookingForm` 也同步加上 `reason` 的設定，特別是的加上 `clean_reason(self)` 的方法用來檢查 reason 輸入是否超過 10 個字（至少 11 個字）。
* `clean_xxx()` 表示要對 `xxx` 欄位進行檢查
    * `reason = self.cleaned_data.get('reason')` 會對使用者輸入的資料進行清理，例如前置空白或是不安全的程式碼。大家可以輸入 `    this is a test, many space before the text   ` 來進行測試-- 輸入後前置空白會被清掉。
    * 我們要求使用者輸入的理由必須超過 10 個字（至少 11 個字），所以做 `len(reason) <= 10` 的檢查。如果使用者違反，會產出 `ValidationError` 的錯誤。這可以在 `booking_form.errors` 來呈現。
* [/courts/views.py](/courts/views.py)
    * `booking_form.is_valid()` 會呼叫 `clean_xxx()`, 所以沒有通過的話，就會跳到 53 行，此時我們 `context` 會包裝錯誤訊息與 `booking_form`, 傳到 `booking_result.html` 中。
* [/courts/templates/booking_result.html](/courts/templates/booking_result.html): 透過 `if booking_form.errors` 來檢查是否有錯誤，有的話就印出。

---

## 延伸練習題 (Classroom Exercises)

以下是兩個適合在課堂上進行的延伸驗證練習題，供學生實作以深化對 Django Form 欄位驗證與自訂規則的理解：

### 練習題一：過濾敏感或測試字詞（理由內容檢查）
* **題目說明**：目前使用者可以隨意輸入無效的預約理由（例如：只輸入 `"testtesttest"` 或 `"測試測試測試測試"`）。請修改驗證邏輯，當使用者的預約原因包含 `test`、`demo`、`測試` 或 `範例` 等無效測試關鍵字時，表單應該驗證失敗並顯示錯誤訊息：「預約原因不能包含測試或範例字詞（如 test, demo, 測試, 範例）」。
* **引導提示**：
    1. 前往 [/courts/forms.py](/courts/forms.py) 修改 `BookingForm` 的 `clean_reason(self)` 方法。
    2. 定義一個禁止關鍵字清單，例如 `forbidden_words = ['test', 'demo', '測試', '範例']`。
    3. 檢查使用者輸入的 `reason`（轉為小寫）中是否包含任何禁止關鍵字，若有則 `raise ValidationError(...)`。

### 練習題二：限制只能預約 30 天以內的日期（日期範圍檢查）
* **題目說明**：目前使用者可以預約任意未來的日期（例如預約明年）。請限制使用者最多只能預約自今天起算 **30 天以內** 的日期。若選擇的日期超過今天加 30 天，表單應驗證失敗並顯示錯誤訊息：「預約日期最多只能是自今天起算 30 天以內的日期」。
* **引導提示**：
    1. 前往 [/courts/forms.py](/courts/forms.py) 修改 `BookingForm`。
    2. 新增一個 `clean_date(self)` 方法來驗證 `date` 欄位。
    3. 透過 `datetime.timedelta(days=30)` 計算出 30 天後的上限日期。
    4. 比對使用者輸入的日期，若大於上限日期，則 `raise ValidationError(...)`。

---

## 延伸練習解答與說明 (Branch `validation.ex` Solution Guide)

本專案的 `validation.ex` 分支中已包含此兩題練習的完整實作與解答，以下為解答說明：

### 練習題一：解答說明
在 [/courts/forms.py](/courts/forms.py) 中，我們修改了 `BookingForm` 類別的 `clean_reason(self)` 方法：

```python
    def clean_reason(self):
        print ('clean_reason is called')
        reason = self.cleaned_data.get('reason')
        if not reason:
            raise ValidationError('預約原因不能為空。')
        if len(reason) <= 10:
            raise ValidationError(f'用途必須超過 10 個字元（至少 11 字）。目前只有 {len(reason)} 個字')
        
        # 練習題一：過濾敏感或測試字詞
        forbidden_words = ['test', 'demo', '測試', '範例']
        reason_lower = reason.lower()
        for word in forbidden_words:
            if word in reason_lower:
                raise ValidationError(f'預約原因不能包含測試或範例字詞（如 {word}）。')
        return reason        
```
* **運作機制**：藉由設定禁止關鍵字陣列 `forbidden_words`，並使用 `in` 關鍵字來比對轉為小寫的 `reason_lower`。一旦偵測到包含禁止字詞，即丟出包含具體敏感關鍵字的 `ValidationError`。

### 練習題二：解答說明
在 [/courts/forms.py](/courts/forms.py) 中，我們為 `BookingForm` 類別新增了 `clean_date(self)` 方法，並導入了 `timedelta`：

```python
    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        if booking_date:
            # 練習題二：限制只能預約 30 天以內的日期
            max_date = date.today() + timedelta(days=30)
            if booking_date > max_date:
                raise ValidationError(f'預約日期最多只能是自今天起算 30 天以內的日期（最晚為 {max_date}）。目前您選擇了 {booking_date}。')
        return booking_date
```
* **運作機制**：Django 的表單提供 `clean_<fieldname>()` 鉤子來針對個別欄位做深度檢驗。我們藉由 `from datetime import date, timedelta` 取得今天的日期並透過 `date.today() + timedelta(days=30)` 計算出最遠的允許預約日，最後比對使用者所選的日期是否超限。