# Django MVT 基礎課堂隨堂測驗 — 用戶登入與球場預約系統 (Quiz)

本測驗旨在檢驗學生對於本單元（`web` 分支：用戶登入表單、@login_required、ModelForm 宣告、動態首頁登入登出、預約防重與資安刪除驗證）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 當我們在設計登入表單（如 `LoginForm`）時，通常希望使用者在輸入密碼時不要以明文顯示（即進行遮蔽，呈現為圓點或星號）。在 Django 表單類別中，應如何設定該欄位？
* (A) `password = forms.CharField(mask=True)`
* (B) `password = forms.PasswordField()`
* (C) `password = forms.CharField(widget=forms.PasswordInput)`
* (D) `password = forms.CharField(widget=forms.HiddenInput)`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* Django 的表單欄位中並沒有內建的名為 `PasswordField` 的類別。
* 密碼欄位本質上仍然是 `CharField`，但需要透過傳入 `widget=forms.PasswordInput` 參數，通知前端 HTML 渲染為 `<input type="password">` 來達到密碼遮蔽效果。
</details>

---

### 2. 當我們在視圖（Views）上加上 `@login_required` 裝飾器來保護頁面時，若未登入的使用者試圖瀏覽，預設會被導向至 `/accounts/login/`。如果我們的自訂登入路徑是 `/login/`，應該在專案的哪一個檔案中新增哪一項設定？
* (A) 在 `/web/views.py` 中，新增 `LOGIN_REDIRECT_URL = '/login/'`
* (B) 在 `/my_tennis_club/settings.py` 中，新增 `LOGIN_URL = '/login/'`
* (C) 在 `/my_tennis_club/urls.py` 中，新增 `path('accounts/login/', redirect('/login/'))`
* (D) 在 `/courts/views.py` 中，新增 `@login_required(url='/login/')`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* Django 全域的登入導向設定是寫在專案的主設定檔 `settings.py` 中。
* 變數名稱為 **`LOGIN_URL`**。將其設定為 `LOGIN_URL = '/login/'` 後，全專案所有被 `@login_required` 標記的視圖，在使用者未登入時都會被正確引導到 `/login/`。
</details>

---

### 3. 我們在首頁模板（`main.html`）中，希望在「已登入」狀態下呈現「登出（Logout）」按鈕，而在「未登入」狀態下呈現「登入（Login）」按鈕。下列哪一個 Django 模板語法能夠正確判斷使用者是否已經登入？
* (A) `{% if request.user.has_login %}`
* (B) `{% if auth.user %}`
* (C) `{% if user.is_authenticated %}`
* (D) `{% if user.logged_in %}`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* Django 的模板引擎會自動將當前請求的 `user` 物件傳入 context 中。
* `user` 物件擁有一個 **`is_authenticated`** 屬性（在 Django 2.0+ 後為屬性，非方法），當用戶已登入時它會回傳 `True`，否則回傳 `False`。
* 故標準寫法為 `{% if user.is_authenticated %}`。
</details>

---

### 4. 關於使用 `forms.ModelForm` 來快速產生與資料庫模型（如 `Booking`）綁定的表單，下列哪一個 `class Meta` 的設定能夠「自動包含該模型的所有資料欄位」？
* (A) `class Meta: model = Booking; fields = '__all__'`
* (B) `class Meta: model = Booking; fields = '*'`
* (C) `class Meta: source = Booking; fields = '__all__'`
* (D) `class Meta: model = Booking; all_fields = True`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(A)**

**解析**：
* 在 Django `ModelForm` 的內部類別 `class Meta` 中：
  * **`model`** 指定要對應綁定的 Model 類別。
  * **`fields = '__all__'`**（雙底線 `__all__`）代表將該 Model 中的所有欄位都包含進表單中進行渲染。
</details>

---

### 5. 在實作「取消預約功能」的 `cancel_booking(request, booking_id)` 視圖時，為了避免惡意用戶透過修改網址上的 `booking_id` 來越權刪除其他使用者的預約資料，下列哪一項安全驗證最為關鍵？
* (A) 只要有加上 `@login_required` 限制登入即可，不需做額外檢查
* (B) 比對該筆預約的擁有者是否為目前發送請求的用戶：`booking.user == request.user`
* (C) 在前端 HTML 檔案中把刪除按鈕隱藏起來
* (D) 確認 `booking_id` 是否為整數

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 這屬於資安上的「不安全的直接物件參照 (IDOR)」漏洞防範。
* 即使使用者已登入（有 `@login_required`），他們仍可能手動修改網址（例如將 `cancel_booking/5/` 改成 `cancel_booking/6/`）來嘗試刪除別人的資料。
* 因此，在後台處理刪除前，**必須**從資料庫撈出該筆預約物件，並嚴格比對 `booking.user == request.user`，符合後才執行 `.delete()`。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請簡述在 Django 認證系統中，`authenticate(username, password)` 與 `auth.login(request, user)` 兩者扮演的角色與本質上的差異。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **`authenticate(username, password)`**：
   - **角色**：身分憑證驗證器。
   - **功能**：負責檢查使用者提供的帳號與密碼是否與資料庫中已儲存的紀錄吻合。若帳密正確，會回傳對應的 `User` 物件；若不正確或帳號被禁用，則回傳 `None`。此步驟**不會**改變使用者的登入狀態（Session）。
2. **`auth.login(request, user)`**：
   - **角色**：登入狀態建立器。
   - **功能**：接收一個已經過驗證的 `User` 物件，並在伺服器端建立 Session 紀錄、在瀏覽器端寫入 Session Cookie，正式將該用戶標記為「已登入狀態」。
3. **結論**：必須先調用 `authenticate()` 確認身分成功後，再將回傳的 `user` 傳入 `auth.login()` 執行登入，兩者相輔相成。
</details>

---

### 7. 在實作預約表單的 HTML 模板時，我們使用了 `<form method="POST">`。請說明為什麼一定要在 Form 標籤內部放置 `{% csrf_token %}` 標籤？如果遺漏了此標籤，當使用者提交表單時會看到什麼結果？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
* **放置原因**：
  - `{% csrf_token %}` 用於防範「跨站請求偽造（Cross-Site Request Forgery, CSRF）」攻擊。
  - Django 模板引擎會在此處自動渲染出一個隱藏的 `<input>` 欄位，內含隨機且安全的 Token。當表單提交時，Django 的 CSRF 中間件（Middleware）會驗證此 Token，以確保該 POST 請求確實是由使用者從我們的網站頁面發出，而非來自外部惡意釣魚網站。
* **遺漏結果**：
  - 如果未放置 `{% csrf_token %}`，當使用者按下提交（Submit）時，Django 的安全機制會拒絕接收該請求，並直接拋出 **`403 Forbidden`** 錯誤頁面，提示「CSRF 驗證失敗。相應請求已被中斷。」
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 請協助完成 [/courts/forms.py](/courts/forms.py) 中 `BookingForm` 的程式碼宣告，使其成為一個 ModelForm，綁定 `Booking` 模型，呈現所有欄位，並將 `date` 欄位的輸入介面自訂為「HTML5 日期選擇器」（`type="date"`）：

```python
# courts/forms.py
from django import forms
from .models import Booking

class BookingForm(forms.____(1)____):
    class Meta:
        model = ____(2)____
        fields = '____(3)____'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `ModelForm`
* `(2)`: `Booking`
* `(3)`: `__all__`

**完整程式碼呈現**：
```python
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
```
</details>

---

### 9. 為了限制「同一個網球場，在同一天內只能被預約一次」（一天內對一個球場只能預約一次），我們需要在 `views.booking` 儲存前先進行重疊檢查。請在下方程式碼的空缺處（標示為 `___(1)___`、`___(2)___`、`___(3)___`）填入正確的 ORM 查詢語法：

```python
# courts/views.py
from django.shortcuts import render
from .models import Booking
from .forms import BookingForm

def booking(request, court_id):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_date = form.cleaned_data.get('date')
            
            # 檢查資料庫是否已存在該場館在該日期的預約
            already_booked = Booking.objects.filter(
                court_id = ___(1)___,
                date = ___(2)___
            ).___(3)___()
            
            if already_booked:
                return render(request, 'booking_result.html', {'message': '該時段已有人預約！'})
                
            # 若無衝突則進行儲存
            form.save()
            return render(request, 'booking_result.html', {'message': '預約成功！'})
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `court_id`
* `(2)`: `booking_date`
* `(3)`: `exists`

**解析**：
* 透過將篩選條件設定為 `court_id=court_id` 與 `date=booking_date`。
* 調用 **`.exists()`** 方法可以極速檢查資料庫中是否存在符合該條件的資料（回傳 `True` 或 `False`），而不需要將整筆資料加載到記憶體中，效能最佳。
</details>
