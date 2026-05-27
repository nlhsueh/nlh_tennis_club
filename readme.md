
前一版本：courts

此一本版：web
* 可以登入
* 選擇球場後可進行預約; 預約時要選擇預約的時間。我們設定一個規則：一天內對於一個球場只能預約一次。
* 選擇我的預約可以觀看我的預約。
* 進行預約及觀看預約都需要登入。如果沒有登入就點擊，系統會直接導到登入頁。
* 回到主頁，如果是登入狀態的話，會出現登出的選項。

## 登入
* [/web/form.py](/web/forms.py)
    * 設計一個登入的表單 LoginForm, 包含 username 與 password。其中password 在輸入時希望遮蔽，所以我們設定 `widget=forms.PasswordInput`
* [/web/view.py](/web/views.py)
    * 透過 urlpattern 引導到 views.login 後，此時的 request.method 為 GET, 我們建立一個 loginForm 後引導到 login.html。當我們填寫好 username, password 後按下 submit, 此時 request.method 為 POST。
    * 當 POST 時，透過 auth.login 來進行登入
    * login_form.clearned_data 的目的在清除一些不適當的輸入，例如前置或後置空白等。LoginForm 內可以定義 clean() 來客製化資料驗證的邏輯（例如帳號和密碼的長度）
* [/members/templates/main.html](/members/templates/main.html)
    * 首頁我們希望在為登入時出現 logout 的選項，登出時出現登入的選項。可以使用 `user.is_authenticated` 來判斷

```python=
  {% if user.is_authenticated %}
    <a href="{% url 'logout' %}">Logout </a> (Your have login as {{ user }}) 
  {% else %}
    <a href="{% url 'login' %}">Login</a>
  {% endif %}
```
* `auth.login(username, password)` 做登入; `auth.logout(username, password)` 做登出。但登入前要先透過 `authenticate(username, password)` 做檢查。

## 預借 (booking)
* 網址 [/courts/urls.py](/courts/urls.py)
    * 添增 `bookings/` 做預約的列表。可以把 user 的所有預約列出來
    * `booking/<int:court_id>`: 針對某一個場館進行預約
* 流程控制 [/courts/views.py](/courts/views.py)
    * `booking(request, court_id)`: 如果是 GET 就先建立一個 `booking_form`, 然後開啟 `booking.html`; 如果是 POST 就進行檢查 (is_valid), 然後存起來 (`form.save()`)
    * 不論成功或失敗都轉到 `booking_result.html` 的頁面，但傳不同的訊息。
    * 預借需要先登入
        * 上述程式必須在 login 的情況下進行，可透過標記 `@login_required` 來註記。記得要匯入 `login_required`。
        * `my_bookings` 也是必須在登入後才能列出所有的預借，所以也加上 `@login_required`
        * 當我們執行 `@login_required` 所標註的方法時，如果當時沒有登入，就會預設的導到 `/account/login`, 但我們是將設置在 `/login/`, 所以必須要到 [/my_tennis_club/settings.py](/my_tennis_club/settings.py)下作修改，加入 `LOGIN_URL = '/login/'`

## 預約表單 (BookingForm) 
* 當我們要預約一個網球場時，需要一個 form，在此我們設計一個 `BookingForm`, 在 [/courts/forms.py](/courts/forms.py)
* `BookingForm` 需要繼承 `forms.ModelForm`
* 透過 `class Meta` 來宣告一些設定: 資料的綁定、要呈現哪些欄位？每個欄位的介面如何呈現？每個資料欄位的標記為何：
    * model: 對應的資料來源。此例為 `Booking`
    * fields: 要呈現哪些資料在 form 中？如果是全部就寫 `__all__`, 如果是部分就用一個 list 來表示，list 為欄位的集合。
    * widgets: 每個資料的呈現設定，例如是要用選擇，還是文字框。
    * labels: 每個資料的標記。因為 model 內的資料欄位是英文（例如 court），不容易理解。用 label 可以以解決此問題。

## 預約的頁面設計 
* [/courts/templates/booking.html](/courts/templates/booking.html))
* `form action='.'` 表示按下 submit 仍然執行此 url
* `method='POST'` 表示按下 submit 後為 POST request
* `{% csrf_token %}` 會產生一組 token, 以確保此 request 不是惡意的請求
* `views.booking` 會將 `booking_form` 傳到此頁，我們可以透過 `booking_form` 來讀取表單的訊息，包含 user, court, date 等。
* 因為我們在 `form model` 中有設計 label 了，所以可以直接取用，不用再特別設計 html 的 label。此例中，user 和 date 都是取 form model 的 label, 球場 court 則自刻，單純做比較。

## 我的預約

* 在網址（[/courts/urls.py](/courts/urls.py)）中新增一個 `/my_bookings`
* views 中透過 `Booking.objects.filter` 找出所有我的預約，在傳到 `my_bookings.html` 做呈現
* [/courts/templates/my_bookings.html](/courts/templates/my_bookings.html): 透過 for loop 把所有的預約都印出來。

## 資料庫重置與初始資料

如果你想要把本地資料庫清乾淨，重新建立 schema 並載入預設資料，可使用專案根目錄的 reset script。

- macOS / Linux: `./reset_db.sh`
- Windows: `reset_db.bat`

這個腳本會執行：

1. 刪除 `db.sqlite3`
2. `python manage.py migrate`
3. `python manage.py loaddata initial_data.json`

目前預設的初始帳號如下：

- `admin` / `Admin123!`
- `alice` / `Alice123!`
- `bob` / `Bob123!`
- `carol` / `Carol123!`

如果你要自行重置資料庫，也可以手動執行：

```bash
rm -f db.sqlite3 db.sqlite3-journal
python manage.py migrate
python manage.py loaddata initial_data.json
```

若要確認 `db.sqlite3` 不會被推到版本控制，請確保 `.gitignore` 中包含 `db.sqlite3`。

## 延伸練習題 (Classroom Exercises)

以下是兩個適合在課堂上進行的延伸練習題，供學生實作以深化對 Django Form 與 View 的理解：

### 練習題一：防止預約過去的日期（表單自訂驗證）
* **題目說明**：目前系統允許使用者預約過去的日期。請修改表單驗證邏輯，當使用者選擇的預約日期早於今天（系統當前日期）時，表單應該驗證失敗並顯示錯誤訊息：「預約日期不能是過去的日期」。
* **引導提示**：
    1. 前往 [/courts/forms.py](/courts/forms.py) 修改 `BookingForm`。
    2. 在 `BookingForm` 內新增一個 `clean_date(self)` 方法，或者覆寫 `clean(self)` 方法。
    3. 透過 `self.cleaned_data.get('date')` 取得使用者輸入的日期，並與當前日期（可使用 `django.utils.timezone.now().date()`）進行比較。
    4. 如果輸入的日期小於今天，使用 `raise forms.ValidationError("預約日期不能是過去的日期")` 拋出錯誤。

### 練習題二：取消預約功能（刪除資料與權限檢查）
* **題目說明**：目前使用者只能在「我的預約」頁面查看預約，但無法取消。請實作一個「取消預約」的功能，在「我的預約」清單中，為每筆預約旁加上一個「取消預約」的按鈕或連結，點擊後會刪除該筆預約並重新導向回「我的預約」頁面。
* **引導提示**：
    1. **設計網址**：在 [/courts/urls.py](/courts/urls.py) 中新增一個 URL pattern，例如 `cancel_booking/<int:booking_id>/`。
    2. **實作 View**：在 [/courts/views.py](/courts/views.py) 中新增一個 `cancel_booking(request, booking_id)` 的視圖：
        * 需使用 `@login_required` 裝飾器確保使用者已登入。
        * 根據 `booking_id` 取得該筆預約資料（例如 `Booking.objects.get(id=booking_id)`）。
        * **安全檢查**：務必確認該筆預約的 `user` 確實是當前登入的 `request.user`，避免惡意使用者透過更改網址上的 ID 刪除別人的預約。
        * 執行刪除動作（`.delete()`），並使用 `redirect` 重新導向回 `my_bookings`。
    3. **更新模板**：在 [/courts/templates/my_bookings.html](/courts/templates/my_bookings.html) 的迴圈中，為每筆預約加上一個指向取消預約網址的連結或按鈕（例如 `<a href="{% url 'cancel_booking' booking.id %}">取消預約</a>`）。

---

## 延伸練習解答與說明 (Branch `web.ex` Solution Guide)

本專案的 `web.ex` 分支中已包含此兩題練習的完整實作與解答，以下為解答說明：

### 練習題一：解答說明
在 [/courts/forms.py](/courts/forms.py) 中，我們為 `BookingForm` 類別新增了 `clean_date(self)` 方法：

```python
    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        if booking_date and booking_date < date.today():
            raise forms.ValidationError("預約日期不能是過去的日期。")
        return booking_date
```
* **運作機制**：Django 的表單在呼叫 `is_valid()` 時，會自動尋找符合 `clean_<fieldname>()` 格式的方法來驗證個別欄位。我們利用 Python 內建的 `datetime.date.today()` 取得今天日期，並與使用者選擇的日期進行比對，若早於今日則丟出 `ValidationError`，該錯誤將自動顯示在表單網頁的預約日期欄位旁。

### 練習題二：解答說明
本題包含了網址路由、後端視圖（含安全性檢查）與前端模板更新：

1. **設計網址** ([/courts/urls.py](/courts/urls.py))：
   ```python
   path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
   ```
2. **實作 View** ([/courts/views.py](/courts/views.py))：
   我們實作了 `cancel_booking` 視圖，並特別加入「安全檢查」：
   ```python
   @login_required
   def cancel_booking(request, booking_id):
       try:
           booking = Booking.objects.get(id=booking_id)
           # 安全檢查：只能取消屬於自己的預約
           if booking.user == request.user:
               booking.delete()
       except Booking.DoesNotExist:
           pass
       return redirect('my_bookings')
   ```
   * **安全性重點**：一定要比對 `booking.user == request.user`，防止使用者透過直接在網址輸入他人預約 ID（例如 `/courts/cancel_booking/999/`）惡意刪除別人的資料。
3. **更新前端模板** ([/courts/templates/my_bookings.html](/courts/templates/my_bookings.html))：
   在每筆預約的後方加上取消連結，並加上 JavaScript `onclick` 確認彈窗以防止誤點：
   ```html
   | <a href="{% url 'cancel_booking' booking.id %}" style="color: #dc3545; text-decoration: none; margin-left: 8px;" onclick="return confirm('確定要取消此預約嗎？');">取消預約</a>
   ```