# version bind_user

前一版本：img

[/members/models.py](/members/models.py)
* 加上 `user` 的外鍵
```python
user = models.OneToOneField(User, on_delete=models.CASCADE, default= None, blank=True, null=True)
```
* 因為一個 `user` 對應一個 `member`, 所以採用 `OneToOneField` 來建立 `user`。

[/courts/views.py](/courts/views.py)
* 把對應的 `member` 找出來傳過去，我們宣告了一個新的 function `getMember()`

[/members/templates/all_members.html](/members/templates/all_members.html)
* 把對應的 `user` 也印出來
* 這個版本也改用 bootstrap 來做 list 的呈現。 (`list-group`, `list-group-item`)

```html
      <ul class="list-group">
        {% for x in mymembers %}
          <li class="list-group-item  bg-transparent"><a href="details/{{ x.id }}">{{ x.lastname }}{{ x.firstname }}</a>, ({{ x.user }}) {{x.age}} 歲</li>
        {% endfor %}
      </ul>
```      

[/members/admin.py](/members/admin.py)
* 新增 `user` 的欄位

```python
  list_display = ("firstname", "lastname", "joined_date","age", "user")
```

[/courts/templates/my_bookings.html](/courts/templates/my_bookings.html)
* 前一版只印出 `user`，這一版我們把 `member` 的姓名也印出來。所以在 [my_bookings()](/courts/views.py) 中，`context` 加上 `member` 的資訊傳到 html。應用 `getMember()` 的函式來取得 member 物件。

---

## 🏋️ 課堂練習

### 練習一：在成員詳情頁面顯示其 Django 系統帳號資訊

**目標**：當我們查看成員的詳細資料（`/members/details/<id>/`）時，若該成員有綁定 `User` 帳號，請一併顯示該帳號的電子郵件（email）與加入系統的時間（date_joined），加深對一對一關係（OneToOneField）跨表欄位存取的理解。

**提示**：
1. 開啟 [/members/templates/details.html](/members/templates/details.html)。
2. 在 `detail-card` 中，使用 `{% if mymember.user %}` 進行判斷。
3. 利用關係路徑讀取與顯示相關欄位：
   * 電子郵件：`{{ mymember.user.email }}`
   * 帳號啟用日期：`{{ mymember.user.date_joined }}`
4. 完成後，點選任一成員，確認頁面能正確渲染出關聯 User 的系統資料。

---

### 練習二：防呆與自動綁定（當登入帳號沒有 Member Profile 時）

**目標**：有時可能會有管理員（如 `admin`）或其他帳號直接在系統中被建立，但忘記在 `Member` 中建立對應的 Profile，導致點擊「我的預約」等功能時出現錯誤。請設計防呆機制，當帳號登入成功後，若發現該 `User` 沒有綁定任何 `Member` Profile，則自動為其建立一個，避免系統崩潰。

**提示**：
1. 開啟 [/web/views.py](/web/views.py) 的 `login` 視圖函數，定位到登入成功（`auth.login(...)`）後的區塊。
2. 匯入 `Member` 模型：`from members.models import Member`。
3. 使用 `hasattr(user, 'member')` 或 `try-except` 來檢查此 `user` 是否已綁定 `member`：
   ```python
   # 檢查該 user 是否有 Member Profile，如果沒有則自動新建一個
   if not hasattr(user, 'member'):
       Member.objects.create(
           user=user,
           firstname=user.username,
           lastname="系統預建",
           phone=None,
           joined_date=date.today()
       )
   ```
4. 測試使用 `admin` 帳號登入，確認登入後系統不會崩潰，且可以在「成員列表」中看到自動建立好的 `admin` 成員 Profile！
