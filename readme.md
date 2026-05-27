
## version `admin`

> 前一版本：`members`

更新：
* 加入 joined_date 及 phone 等欄位，設定這些欄位的屬性，例如 default, verbose_name 等
* admin.py 中，admin 對 member 的註冊
* **批次新增會員資料**：可在 Django Shell 環境下執行 [/members/addMember.py](/members/addMember.py) 腳本，一次快速匯入 10 筆測試會員資料。
  ```shell
  python manage.py shell
  # 進入 shell 後執行下列指令：
  exec(open('members/addMember.py').read())
  ```

學習內容
* 進入 admin 請觀察欄位的變化
* null=True 及 blank=Ture 的必要與差異
* makemigrations, migrate

### 建立管理者

```
py manage.py createsuperuser
```
* 你可以用 admin 或是取其他的名字，接著設定密碼。
* 建立後就可以到 [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) 操作。
* 在 admin 的管理中加上 members 等模組，如此 admin 才看得到這些資料。See [W3School- admin include models](https://www.w3schools.com/django/django_admin_include_members.php)

```python
from django.contrib import admin
from .models import Member

# Register your models here.
admin.site.register(Member)
```

> [!TIP]
> **視覺化管理會員資料**：
> 註冊完成後，當您登入並進入後台管理頁面（[/admin/](http://127.0.0.1:8000/admin/)）時，您會看到一個名為 **Members** 的區塊。您可以點擊進入，直接在網頁上視覺化地進行會員資料的**新增（Create）**、**查看（Read）**、**修改（Update）**與**刪除（Delete）**等 CRUD 資料操作。

---

## 資料庫限制

在設計資料庫時，為了確保資料的**完整性 (Integrity)** 和**有效性 (Validity)**，我們需要定義各種限制 (Constraints)。這些限制會在資料庫層級強制執行，防止不符合規則的資料被寫入。

以下是一些常見的資料庫限制及其在 Django 模型中的對應方式：

* **1. 資料類型限制 (Data Type Constraints)**

  * **定義：** 每個欄位都必須儲存特定類型 (例如：整數、字串、日期等) 的資料。這是最基本的限制。
  * **Django 範例：** Django 模型中的每個欄位都必須指定一個 Field 類型，例如 `IntegerField`, `CharField`, `DateField`, `EmailField` 等。

      ```python
      from django.db import models

      class Product(models.Model):
          name = models.CharField(max_length=100)  # 字串類型，限制最大長度
          price = models.DecimalField(max_digits=10, decimal_places=2)  # 十進位類型，限制總位數和小數位數
          quantity = models.IntegerField()  # 整數類型
          is_available = models.BooleanField(default=True)  # 布林類型
          created_at = models.DateTimeField(auto_now_add=True)  # 日期時間類型
      ```

* **2. 非空限制 (NOT NULL Constraint)**

  * **定義：** 確保欄位的值不能為 `NULL`。
  * **Django 範例：** 在 Django 模型中，預設情況下欄位允許 `NULL` 值。要設定非空限制，需要將 `null` 參數設為 `False`。

      ```python
      class Category(models.Model):
          name = models.CharField(max_length=50, null=False)  # name 欄位不能為 NULL
      ```

**null 與 blank**

  `null` 和 `blank` 常常搞混，前者是**資料庫限制**，後者是**表單限制**。基於 `phone = models.CharField(max_length=20, null=False, blank=True)` 對應 TT, TF, FT, FF 四種狀況，說明了 `null` 和 `blank` 的組合及其含義：

  |  `null`   |  `blank`  |  狀況  | 含義 (針對 `phone` 欄位)                                                                                                                                                                         |
  | :-------: | :-------: | :----: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | **True**  | **True**  | **TT** | 資料庫**允許** `NULL` 值。Django 表單**允許**留空字串 (`''`)。電話號碼在資料庫中可以是沒有值 (`NULL`) 的，使用者在表單中也可以不填寫。                                                           |
  | **True**  | **False** | **TF** | 資料庫允許 `NULL` 值。Django 表單**不允許**留空字串 (`''`)。電話號碼在資料庫中可以是沒有值 (`NULL`) 的，但是使用者在表單中**必須填寫**，不能留空。                                               |
  | **False** | **True**  | **FT** | 資料庫**不允許** `NULL` 值。Django 表單允許留空字串 (`''`)。電話號碼在資料庫中**必須有值** (但可以是空字串 `''`)，使用者在表單中可以不填寫。當表單留空提交時，資料庫會儲存空字串 (`''`)。        |
  | **False** | **False** | **FF** | 資料庫**不允許** `NULL` 值。Django 表單**不允許**留空字串 (`''`)。電話號碼在資料庫中**必須有值** (且不能是 `NULL`)，使用者在表單中**必須填寫**，不能留空。這是強制要求使用者提供電話號碼的設定。 |


* **3. 唯一性限制 (UNIQUE Constraint)**

  * **定義：** 確保欄位中的所有值都是唯一的。
  * **Django 範例：** 使用 `unique=True` 參數可以為欄位增加唯一性限制。

      ```python
      class User(models.Model):
          username = models.CharField(max_length=30, unique=True)  # username 必須是唯一的
          email = models.EmailField(unique=True)  # email 也必須是唯一的
      ```
      也可以在模型層級定義多個欄位的聯合唯一性約束：

      ```python
      class Meta:
          unique_together = (('first_name', 'last_name'),)  # first_name 和 last_name 的組合必須是唯一的
      ```
      或者使用 `UniqueConstraint` (Django 2.2+):

      ```python
      from django.db.models import UniqueConstraint

      class Person(models.Model):
          first_name = models.CharField(max_length=30)
          last_name = models.CharField(max_length=30)

          class Meta:
              constraints = [
                  UniqueConstraint(fields=['first_name', 'last_name'], name='unique_full_name')
              ]
      ```

* **4. 主鍵限制 (PRIMARY KEY Constraint)**

  * **定義：** 唯一標識資料表中的每一行。每個資料表只能端有一個主鍵。主鍵通常是非空且唯一的。
  * **Django 範例：** Django 模型預設會自動建立一個名為 `id` 的 `AutoField` 欄位作為主鍵。你可以選擇其他欄位作為主鍵，但通常不建議修改預設行為。

      ```python
      class Book(models.Model):
          book_id = models.AutoField(primary_key=True)  # 明確指定 book_id 為主鍵 (通常不需要)
          title = models.CharField(max_length=200)
      ```

* **5. 外鍵限制 (FOREIGN KEY Constraint)**

  * **定義：** 用於建立和強制執行不同資料表之間的關係。外鍵欄位的值必須參考另一個資料表的主鍵。
  * **Django 範例：** 使用 `ForeignKey` 欄位來定義外鍵關係。

      ```python
      class Author(models.Model):
          name = models.CharField(max_length=100)

      class Article(models.Model):
          title = models.CharField(max_length=200)
          author = models.ForeignKey(Author, on_delete=models.CASCADE)  # author 是外鍵，參考 Author 模型
      ```
      * `on_delete`: 定義當參考的父物件被刪除時，子物件應該如何處理 (`CASCADE`, `PROTECT`, `SET_NULL`, `SET_DEFAULT`, `DO_NOTHING` 等)。
          * `CASCADE`: author 被刪除，其所關聯 the article 一起被刪除。
          * `PROTECT`: 刪除 author 時，因為已有 book 與之關聯，會跳出警告避免被刪。
          * `SET_NULL`: author 被刪除，Article 相關聯的 author 欄位被設為 null。Article 的 author 必須允許為 null (`null=True`)。
          * `SET_DEFAULT`: author 被刪除時，Article 中的 author 設為預設值(如 `default="unknown"`)。
          * `DO_NOTHING`: author 被刪就被刪，不做任何處理，強烈不建議，會造成資料的不完整。

* **6. 檢查限制 (CHECK Constraint)**

  * **定義：** 定義一個布林表達式，用於限制欄位中允許的值。只有滿足表達式的值才能被接受。
  * **Django 範例：** Django 模型在早期版本中沒有直接支援 CHECK constraint。從 Django 3.2 開始，可以使用 `CheckConstraint` (Django 3.2+)。

      ```python
      from django.db.models import CheckConstraint, Q

      class Order(models.Model):
          quantity = models.IntegerField()
          status = models.CharField(max_length=20)

          class Meta:
              constraints = [
                  CheckConstraint(check=Q(quantity__gt=0), name='quantity_greater_than_zero'),
                  CheckConstraint(check=Q(status__in=['pending', 'processing', 'shipped', 'delivered']), name='valid_status')
              ]
      ```

* **7. 預設值限制 (DEFAULT Constraint)**

  * **定義：** 為欄位指定一個預設值，當在插入新記錄時沒有提供該欄位的值時，將使用預設值。
  * **Django 範例：** 使用 `default` 參數為欄位設定預設值。

      ```python
      class Task(models.Model):
          description = models.TextField()
          is_completed = models.BooleanField(default=False)  # 預設為 False
          priority = models.IntegerField(default=3)  # 預設優先級為 3
      ```

* **8. 長度限制 (LENGTH Constraint)**

  * **定義：** 限制字串或二進制資料欄位的最大長度。
  * **Django 範例：** `CharField` 和 `TextField` 可以使用 `max_length` 參數來設定最大長度。

      ```python
      class BlogPost(models.Model):
          title = models.CharField(max_length=255)  # 標題最大長度為 255
          content = models.TextField()
      ```

* **9. 列舉限制 (ENUM Constraint)**

  * **定義：** 限制欄位只能從預先定義的一組值中選擇。
  * **Django 範例：** Django 雖然有 Enum 類型，也常用 `TextChoices` 搭配 `choices` 參數來模擬列舉限制。

      ```python
      class OrderStatus(models.TextChoices):
          PENDING = 'PD', 'Pending'
          PROCESSING = 'PR', 'Processing'
          SHIPPED = 'SH', 'Shipped'
          DELIVERED = 'DE', 'Delivered'

      class Shipment(models.Model):
          status = models.CharField(max_length=2, choices=OrderStatus.choices, default=OrderStatus.PENDING)
      ```

**總結**

合理地使用資料庫的各種限制對於建立一個健壯、可靠的應用程式至關重要。它們有助於確保資料的準確性、一致性和完整性。Django 的模型定義提供了方便的方式來聲明這些限制，並且 Django 的 ORM 會在與資料庫互動時考慮這些限制。在設計模型時，仔細思考每個欄位的限制，將有助於避免後續的資料問題。