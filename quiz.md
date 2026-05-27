# Quiz

本測驗旨在檢驗學生對於本單元（`admin` 分支：Django Admin、Database Constraints 資料庫限制、欄位異動處理與管理者建立）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 關於 Django 模型中 `null` 與 `blank` 的設定，下列哪一個選項正確描述了「**FT（null=False, blank=True）**」的組合對應字串欄位（如 CharField）的行為？
* (A) 資料庫允許 `NULL` 值，且 Django 表單不允許留空。
* (B) 資料庫允許 `NULL` 值，且 Django 表單允許留空。
* (C) 資料庫**不允許** `NULL` 值，但 Django 表單**允許**留空。當表單留空提交時，資料庫會儲存空字串 `''`。
* (D) 資料庫**不允許** `NULL` 值，且 Django 表單**不允許**留空。使用者必須強制填寫。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* **`null`** 控制的是**資料庫限制**是否可以儲存 `NULL`。
* **`blank`** 控制的是**表單驗證限制**是否可以留空。
* 當設定為 **FT (null=False, blank=True)** 時，表單允許留空（不填寫），但因為資料庫不允許寫入 `NULL`，Django 在表單留空提交時會將其轉為空字串 `''`（對於字串欄位）並安全地寫入資料庫，從而避免資料庫拋出 `NOT NULL` 錯誤。這是一種常見的字串選填欄位配置方式。
</details>

---

### 2. 在 Django 中設定外鍵關係時，如果我們希望在刪除父物件（例如 Author）時，**阻止 (Prevent)** 該刪除操作，因為已經有子物件（例如 Article）與之關聯，避免意外刪除造成資料毀損，應在 `on_delete` 中設定哪一個參數？
* (A) `models.CASCADE`
* (B) `models.PROTECT`
* (C) `models.SET_NULL`
* (D) `models.DO_NOTHING`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* (A) `CASCADE`：當父物件被刪除時，所有關聯的子物件會被自動串聯刪除。
* (B) `PROTECT`：**阻止刪除**。如果父物件底下已有被關聯的子物件，Django 會拋出 `ProtectedError` 警告，阻止管理員刪除該父物件。
* (C) `SET_NULL`：當父物件被刪除時，子物件的外鍵欄位會被設為 `NULL`（需要該外鍵支援 `null=True`）。
* (D) `DO_NOTHING`：什麼都不做，不建議使用，容易導致資料完整性毀損。
</details>

---

### 3. 要在 Django 專案中建立一個全域的管理者（後台系統管理員）帳號與密碼，應在終端機中執行哪一個命令？
* (A) `python manage.py createsuperuser`
* (B) `python manage.py createadmin`
* (C) `python manage.py makemigrations`
* (D) `python manage.py runserver`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(A)**

**解析**：
* 在終端機執行 `python manage.py createsuperuser`（或 `py manage.py createsuperuser`）會啟動互動式提示，引導您輸入管理員用戶名稱、Email 與密碼，成功後即可登入後台系統管理介面（`/admin`）。
</details>

---

### 4. 下列關於資料庫唯一性限制（UNIQUE Constraint）的描述，何者是**錯誤**的？
* (A) 可以使用 `unique=True` 為單一欄位加上唯一性限制。
* (B) 可以在 Model 的內部 `Meta` 類別中，使用 `unique_together` 來設定多個欄位的聯合唯一性限制。
* (C) Django 預設的自動主鍵 `id` 欄位在資料庫層級自動帶有唯一性限制。
* (D) 在 Django 模型中，設定為 `unique=True` 的欄位，不論如何都不允許寫入 `NULL` 值。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(D)**

**解析**：
* (D) 錯誤：如果模型設定了 `unique=True`，但同時設定了 `null=True`，則該唯一性欄位是**允許**儲存 `NULL` 值的。在大多數資料庫中，多個紀錄同時為 `NULL` 是被允許的（因為 `NULL` 代表無值，互不相等）。
* (A), (B), (C) 的敘述均為完全正確的唯一性限制設定與行為。
</details>

---

### 5. 如果我們希望將自訂的資料模型 `Member` 註冊到 Django Admin 管理後台，使管理員能透過後台進行新增、修改與刪除，應該在 `/members/admin.py` 中撰寫哪一段程式碼？
* (A) `admin.site.add(Member)`
* (B) `admin.site.register(Member)`
* (C) `admin.register_model(Member)`
* (D) `admin.register(MemberAdmin)`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 在 Django 中，要將模型載入 Admin 管理系統，必須在該 App 的 `admin.py` 中使用 `admin.site.register(<ModelName>)` 來註冊，使其自動在後台生成資料管理表格介面。
</details>
---

### 6. 關於外鍵限制（FOREIGN KEY Constraint）的刪除行為，若我們設定當作者（Author）被刪除時，其發表的文章（Article）依然保留，但將該文章的 `author` 欄位設為一個特定的預設值，應在 `on_delete` 中使用哪一個參數？
* (A) `models.CASCADE`
* (B) `models.SET_NULL`
* (C) `models.SET_DEFAULT`
* (D) `models.PROTECT`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* (A) `CASCADE`：級聯刪除，父物件被刪，子物件一併被刪。
* (B) `SET_NULL`：將子物件的外鍵欄位設為 `NULL`（需要支援 `null=True`）。
* (C) `SET_DEFAULT`：當父物件被刪除時，會自動將子物件的外鍵欄位設為其宣告時指定的 `default` 預設值（外鍵必須設定有預設值）。
* (D) `PROTECT`：阻止刪除父物件。
</details>

---

### 7. 關於資料庫的非空限制（NOT NULL）與 Django 表單的空值處理，若我們宣告一個整數欄位為 `phone = models.IntegerField(null=False, blank=True)`，當使用者提交空白表單且未輸入任何值時，會發生什麼情況？
* (A) 資料庫會成功寫入 `NULL` 值。
* (B) 資料庫會自動寫入 `0` 作為預設值。
* (C) 資料庫會寫入空字串 `''` 作為值。
* (D) 系統會拋出錯誤（如 `IntegrityError` 或 `ValidationError`），因為整數欄位無法接收空字串 `''` 且不允許寫入 `NULL`。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(D)**

**解析**：
* 對於 `CharField`（字串型態），當 `null=False, blank=True` 時，留空表單會成功轉為空字串 `''` 存入。
* 但對於 `IntegerField`（整數型態），Django 表單留空時無法將空字串 `''` 轉為整數，因此會嘗試寫入 `NULL`。但因為設定了 `null=False`，這會直接在資料庫層級或表單驗證層級觸發非空限制錯誤（`IntegrityError` 或驗證失敗），導致資料無法寫入。因此整數欄位若要選填，通常必須設定 `null=True, blank=True`（即 TT 狀況）。
</details>

---

### 8. 關於列舉限制（ENUM Constraint / choices 限制）的行為，下列哪一個說法是正確的？
* (A) 在 Django 中設定 `choices` 屬性後，所有的資料庫系統（包括 SQLite）都會在資料庫欄位自動生成實體的 `ENUM` 型態。
* (B) `choices` 限制主要是由 Django 的**表單驗證與後台介面**在應用程式層面進行防呆與限制，並不會自動在所有資料庫底層建立強制的 ENUM 類型。
* (C) Django 的 `choices` 屬性只能接受字串型態，不能使用整數型態。
* (D) 設定 `choices` 後，我們如果透過外部 SQL 工具強行寫入一個不在 choices 選項內的值，Django 項目在讀取該資料時會直接崩潰。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* (A) 錯誤：並非所有資料庫都支援 ENUM。Django 的 `choices` 主要是由應用程式（表單與後台）進行下拉選單渲染與驗證，資料庫欄位本質上依然是 `CharField` 或 `IntegerField` 等。
* (B) 正確：`choices` 提供便捷的防呆驗證，但並不會自動修改底層資料庫使之變成嚴格的 ENUM Constraint，資料庫底層依然由原欄位型態決定。
* (C) 錯誤：`choices` 支援任何型態，例如 `IntegerChoices`。
* (D) 錯誤：若用外部 SQL 強行寫入不在 choices 內的值，資料庫會接受且 Django 讀取時可正常讀出，只是 `get_xxx_display()` 時會退回顯示原值，不會導致系統崩潰。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 9. 請說明 Django 模型定義中的 `null` 屬性與 `blank` 屬性的根本差異為何？（分別從「資料庫」與「表單驗證」層面說明）

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
* **`null`（資料庫層面限制）**：
  這是資料庫欄位屬性的約束。如果 `null=True`，表示在資料庫（DB Table）中該欄位可以儲存 `NULL` (也就是無值、空值)；如果為 `False`，則該欄位被約束為 `NOT NULL`，資料庫拒絕寫入空值。
* **`blank`（表單/驗證層面限制）**：
  這是 Django 表單驗證的約束。如果 `blank=True`，代表在網頁表單或後台管理介面編輯時，該欄位是**選填**的（允許留空不填寫）；如果為 `False`，則該欄位是**必填**的，留空提交時表單驗證會報錯。
</details>

---

### 10. 請簡述 `on_delete=models.CASCADE` 在建立外鍵關係時的作用與行為。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
* **`models.CASCADE`** 代表**級聯刪除（串聯刪除）**。
* 當被參考的父物件（例如 Author 作者）被刪除時，所有關聯到該父物件的子物件（例如該作者所發表的所有 Article 文章）也會在資料庫中被**一併自動刪除**，以確保資料的一致性，防止出現指向不存在對象的無效外鍵紀錄。
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 11. 在 `members/models.py` 中，我們需要替會員模型加上 `phone`（整數，允許資料庫為 NULL 與表單留空）與 `joined_date`（日期，允許資料庫為 NULL 與表單留空，預設為當天日期）欄位。請在下列程式碼的空缺處（標示為 `___(1)___`、`___(2)___`、`___(3)___`）填入正確的 Django 欄位型態或參數代碼：

```python
from django.db import models
import datetime

class Member(models.Model):
    firstname = models.CharField(max_length=255, verbose_name='名字')
    lastname = models.CharField(max_length=255, verbose_name='姓')
    
    phone = models.___(1)___(null=True, blank=True, verbose_name='電話')
    joined_date = models.___(2)___(null=True, blank=True, verbose_name='入會日期', default=datetime.date.___(3)___())
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `IntegerField`
* `(2)`: `DateField`
* `(3)`: `today`

**完整程式碼呈現**：
```python
class Member(models.Model):
    firstname = models.CharField(max_length=255, verbose_name='名字')
    lastname = models.CharField(max_length=255, verbose_name='姓')
    
    phone = models.IntegerField(null=True, blank=True, verbose_name='電話')
    joined_date = models.DateField(null=True, blank=True, verbose_name='入會日期', default=datetime.date.today())
```
</details>

---

### 12. 我們希望在 Django 中，為一個名為 `Order` 的訂單模型在內部 `Meta` 中加上「檢查限制（CHECK Constraint）」，規定訂單的數量（`quantity`）必須大於 `0`。請在下列 Python 程式碼的空缺處（標示為 `___(1)___`、`___(2)___`、`___(3)___`、`___(4)___`）填入正確的 Django ORM 或限制類別代碼：

```python
from django.db import models
from django.db.models import ___(1)___, Q

class Order(models.Model):
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)

    class Meta:
        constraints = [
            ___(2)___(check=Q(quantity___(3)___0), name='___(4)___')
        ]
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `CheckConstraint`
* `(2)`: `CheckConstraint`
* `(3)`: `__gt=`
* `(4)`: `quantity_greater_than_zero`

**完整程式碼呈現**：
```python
from django.db import models
from django.db.models import CheckConstraint, Q

class Order(models.Model):
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(quantity__gt=0), name='quantity_greater_than_zero')
        ]
```
</details>
