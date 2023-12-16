## 登入
* [/web/form.py](/web/forms.py)
    * 設計一個登入的表單 LoginForm, 包含 username 與 password。其中password 在輸入時希望遮蔽，所以我們設定 `widget=forms.PasswordInput`
* [/web/view.py](/web/views.py)
    * 透過 urlpattern 引導到 views.login 後，此時的 request.method 為 GET, 我們建立一個 loginForm 後引導到 login.html。當我們填寫好 username, password 後按下 submit, 此時 request.method 為 POST。
    * 當 POST 時，透過 auth.login 來進行登入
    * login_form.clearned_data 的目的
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

## 預約表單 (BookingForm) 
* 當我們要預約一個網球場時，需要一個 form，在此我們設計一個 `BookingForm`, 在 [/courts/forms.py](/courts/forms.py)
* 需要繼承 `forms.ModelForm`
* 透過 `class Meta` 來宣告一些設定: 資料的綁定、要呈現哪些欄位？每個欄位的介面如何呈現？每個資料欄位的標記為何：
    * model: 對應的資料來源。此例為 `Booking`
    * fields: 要呈現哪些資料在 form 中？如果是全部就寫 __all__, 如果是部分就用一個 list 來表示，list 為欄位的集合。
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
* [/courts/templates/my_bookings](/courts/templates/my_bookings): 透過 for loop 把所有的預約都印出來。