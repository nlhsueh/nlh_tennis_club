# version validation

在 form 物件中，加上驗證的邏輯程式碼

[/courts/models.py](/courts/models.py)
* `Booking` 的類別，加上 `reason` 的欄位，用來描述預約的目的

[/courts/forms.py](/courts/forms.py)
* `BookingForm` 也同步加上 `reason` 的設定，特別是的加上 `clean_reason(self)` 的方法用來檢查 reason 輸入是否超過 10 個字。
* `clean_xxx()` 表示要對 `xxx` 欄位進行檢查
    * `reason = self.cleaned_data.get('reason')` 會對使用者輸入的資料進行清理，例如前置空白或是不安全的程式碼。大家可以輸入 `    this is a test, many space before the text   ` 來進行測試-- 輸入後前置空白會被清掉。
    * 我們要求使用者輸入的理由不可以少於 10 個字，所以做 `len(reason) <= 10` 的檢查。如果使用者違反，會產出 `ValidationError` 的錯誤。這可以在 `booking_form.errors` 來呈現。
* [/courts/views.py](/courts/views.py)
    * `booking_form.is_valid()` 會呼叫 `clean_xxx()`, 所以沒有通過的話，就會跳到 53 行，此時我們 `context` 會包裝錯誤訊息與 `booking_form`, 傳到 `booking_result.html` 中。
* [/courts/templates/booking_result.html](/courts/templates/booking_result.html): 透過 `if booking_form.errors` 來檢查是否有錯誤，有的話就印出。