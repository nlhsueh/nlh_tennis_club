## 登入
* [/web/form.py](/web/forms.py)
    * 設計一個登入的表單 LoginForm, 包含 username 與 password。其中password 在輸入時希望遮蔽，所以我們設定 `widget=forms.PasswordInput`
* [/web/view.py](/web/views.py)
    * 透過 urlpattern 引導到 views.login 後，此時的 request.method 為 GET, 我們建立一個 loginForm 後引導到 login.html。當我們填寫好 username, password 後按下 submit, 此時 request.method 為 POST。
    * 當 POST 時，透過 auth.login 來進行登入
* [/members/template/main.html](/members/template/main.html)
    * 首頁我們希望在為登入時出現 logout 的選項，登出時出現登入的選項。可以使用 `user.is_authenticated` 來判斷

```python=
  {% if user.is_authenticated %}
    <a href="{% url 'logout' %}">Logout </a> (Your have login as {{ user }}) 
  {% else %}
    <a href="{% url 'login' %}">Login</a>
  {% endif %}
```