## Django MVT 基礎課堂隨堂測驗 — 一對一關係綁定與自動創建 (Quiz)

本測驗旨在檢驗學生對於本單元（`bind_user` 分支：Django 一對一關係模型 `OneToOneField`、串聯刪除 `on_delete=models.CASCADE`、跨表欄位存取、以及利用 `hasattr()` 進行 Profile 自動補完與防呆）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 關於 Django 中的 `models.OneToOneField`（一對一關係）與 `models.ForeignKey`（外鍵關係），下列哪一個敘述完全正確？
* (A) `OneToOneField` 限制了 A 資料表中的一筆紀錄「最多只能關聯」到 B 資料表中的一筆紀錄；而 `ForeignKey` 則是多對一關係，允許 A 資料表的多筆紀錄關聯到 B 資料表的同一筆紀錄。
* (B) `OneToOneField` 可以自動同步兩個資料表的所有其他欄位，不需要透過關係查詢。
* (C) 兩者在底層資料庫的限制完全相同，僅是在 Python 程式碼中的名稱不同。
* (D) `OneToOneField` 只能用來連結自訂的 Model，不能用來連結 Django 內建的 `User` 模型。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(A)**

**解析**：
* 在資料庫層級，`OneToOneField` 其實相當於一個加上了 `unique=True` 唯一性約束的 `ForeignKey`。
* 它確保了關聯的唯一性（例如：一個 `Member` 成員設定檔，只能專屬於唯一一個 `User` 帳號；而一個 `User` 也只會有一個 `Member` Profile）。這與 `ForeignKey`（如多個 Booking 預約可以關聯至同一個 User）的多對一關係不同。
</details>

---

### 2. 在本單元中，我們在 `Member` 中設定了外鍵：`user = models.OneToOneField(User, on_delete=models.CASCADE, ...)`。當我們在 Django 後台手動「刪除（Delete）」某個系統帳號 `User` 物件時，會發生什麼事？
* (A) 系統會直接噴錯，拒絕刪除該 User，因為它已被 Member 關聯。
* (B) 該 User 帳號會被刪除，但對應的 `Member` 物件會被保留，其 `user` 欄位會被設為 `NULL`。
* (C) 該 User 帳號被刪除，且與其關聯的 `Member` 物件也會被「自動一併刪除」。
* (D) 該 User 帳號被刪除，且資料庫中所有的預約紀錄都會被自動清空。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* 參數 **`on_delete=models.CASCADE`** 代表「級聯/串聯刪除」。
* 由於 `OneToOneField` 宣告在 `Member` 模型上，代表 `Member` 依賴於 `User`。當被參考的父物件（`User`）被刪除時，依賴它的子物件（`Member`）也會自動被清理掉，以維持資料的關聯完整性。
</details>

---

### 3. 在 HTML 模板中，若我們手中有一個 `mymember` 物件（`Member` 類別的實例），而我們想要顯示其關聯之系統帳號（`User`）的電子郵件信箱（email），應該如何動態存取？
* (A) `{{ mymember.email }}`
* (B) `{{ mymember.user_email }}`
* (C) `{{ mymember.user.email }}`
* (D) `{{ mymember.get_email_display }}`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* 藉由一對一關係的綁定，我們可以利用 Python 的物件導向鏈式語法（Dot Notation）直接進行跨表查詢。
* `mymember.user` 能存取到對應的 `User` 物件，而 `User` 模型內建了 `email` 欄位，因此使用 `mymember.user.email` 即可在樣板中無縫輸出該使用者的信箱。
</details>

---

### 4. 在後端 Python 邏輯中，當我們要判定一個 `User` 物件（變數名為 `user`）是否「已經擁有」對應的 `Member` Profile 時，最優雅且符合 Python 慣例的檢查寫法為何？
* (A) `if user.member_id != None:`
* (B) `if hasattr(user, 'member'):`
* (C) `if Member.objects.filter(user_id=user.id).exists() == False:`
* (D) `if user.get_member() is not None:`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 在 Django 的一對一關係中，`User` 端（被關聯端）會自動獲得一個反向關係屬性（預設為小寫的模型名稱：`member`）。
* 如果該 `user` 有關聯的 `Member`，存取 `user.member` 會回傳該物件；若沒有，存取則會拋出 `DoesNotExist` 異常。
* 為了安全檢查，使用 Python 內建的 **`hasattr(user, 'member')`** 是最標準的寫法。若有 Profile 則回傳 `True`，否則回傳 `False`。
</details>

---

### 5. 在本單元的 `all_members.html` 中，我們改用了 Bootstrap 的清單元件來呈現成員。請問是用哪一組 class 的組合來將傳統的無序清單 `<ul>` 與 `<li>` 轉換成美觀的 Bootstrap 清單？
* (A) `class="list"` 與 `class="item"`
* (B) `class="list-group"` 與 `class="list-group-item"`
* (C) `class="nav"` 與 `class="nav-link"`
* (D) `class="table"` 與 `class="table-row"`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* Bootstrap 提供 **`list-group`**（列表群組）元件來美化清單呈現。
* 我們需要在外層的 `<ul>`（或 `<div>`）加上 `class="list-group"`，並在內層的每個 `<li>`（或 `<a>`）加上 `class="list-group-item"`，即可去除預設的小圓點，並渲染出帶有圓角與邊框的精美卡片清單。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請詳細說明：在 `Member` 與 `User` 的一對一關係中，若我們在後台手動「刪除（Delete）」某個 `Member`（會員 Profile）物件，與它關聯的 `User`（登入帳號）物件會被一併刪除嗎？為什麼？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **答案**：不會，與該 `Member` 關聯的 `User` 帳號**會被保留**，不會被刪除。
2. **原因分析**：
   - 級聯刪除的屬性 `on_delete=models.CASCADE` 是宣告在 `Member` 模型的 `user` 欄位上。這意味著「`Member` 依賴於 `User`」。
   - 因此，只有當主動刪除被參考的父物件（`User`）時，依賴它的子物件（`Member`）才會被串聯刪除。
   - 反之，刪除子物件（`Member`）時，並不會影響到被參考的父物件（`User`）。這符合資料庫設計的單向依賴原則，避免了反向級聯導致系統帳號被意外刪除的風險。
</details>

---

### 7. 在課堂練習二中，我們為什麼要在登入成功後的 View 裡，使用 `hasattr(user, 'member')` 來檢查並在必要時執行 `Member.objects.create(...)`？如果我們不進行這個檢查，而直接讓沒有 Member Profile 的帳號（如剛建立的 Superuser）造訪「我的預約」頁面，系統內部會發生什麼事？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **防呆與自動建立**：有些系統帳號（如超級管理員 `admin`）是直接透過終端機 `createsuperuser` 建立的，資料庫中只有 `auth_user` 的資料，並沒有在 `Member` 資料表中建立對應的 Profile。我們在登入後檢查並自動建立 Profile，能確保登入的使用者在系統中擁有完整的會員身分。
2. **不檢查的崩潰後果**：如果沒有這個檢查，當管理員造訪「我的預約」或執行 `getMember()` 時，代碼會嘗試讀取 `request.user.member`。由於資料庫中不存在對應的 `Member` 紀錄，Django 會直接拋出 **`User.member.RelatedObjectDoesNotExist`** 異常，導致網頁伺服器拋出 500 內部錯誤，系統直接崩潰。
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 請完成以下 `members/models.py` 中 `Member` 模型對 `User` 帳號的一對一連結宣告，使其能正常綁定、支援串聯刪除，且在資料庫中該欄位允許為空（Null）：
```python
# members/models.py
from django.db import models
# 1. 引入 Django 內建的 User 模型
from django.contrib.auth.models import ___(1)___

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    
    # 2. 宣告一對一欄位並綁定
    user = models.___(2)___(
        ___(1)___, 
        on_delete=models.___(3)___, 
        default=None, 
        blank=True, 
        null=True
    )
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `User`
* `(2)`: `OneToOneField`
* `(3)`: `CASCADE`
</details>

---

### 9. 以下是登入成功後，自動檢查並為 `User` 補建 `Member` Profile 的 View 邏輯。請在填充處填入正確的 Python 內建函數或 Django ORM 建立物件的方法名：

```python
# web/views.py
from django.shortcuts import render, redirect
from members.models import Member
from datetime import date

def login_success_handler(request, user):
    # 1. 檢查該 user 物件是否「不包含」名為 'member' 的關聯屬性
    if not ___(1)___(user, 'member'):
        # 2. 自動在資料庫中新建一筆關聯該 user 的 Member 紀錄
        Member.objects.___(2)___(
            user=user,
            firstname=user.username,
            lastname="系統預建",
            joined_date=date.today()
        )
    return redirect('/')
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `hasattr`
* `(2)`: `create`

**解析**：
* Python 內建的 `hasattr(object, name)` 函數接收一個物件與一個字串屬性名，若屬性存在則回傳 `True`，非常適合用來偵測關聯是否存在，且不會像直接存取那樣引發異常。
* Django ORM 中，`objects.create(...)` 是一步到位地在資料庫中建立並直接儲存新物件的便捷方法，相當於實例化後調用 `save()`。
</details>
