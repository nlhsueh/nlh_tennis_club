
> [!NOTE]
> 🏈 You will learn
> * 如何建立資料庫的資料
>     * model 與 makemigrations, migrate
> * 如何透過 shell 新增資料
> * 如何讀取資料，並將之呈現在網頁中
>     * 網頁樣板標籤與樣板變數的意義
> See branch **[member](https://github.com/nlhsueh/nlh_tennis_club/tree/member)**

這個 lab 中，我們設計一個會員資料庫，並呈現之。

#### 1. Model

* Model 是設計資料的地方，每一個資料表用一個 class 來宣告設計:
    * 必須繼承 `models.Model`
* 每個資料欄位有不同的型態，常見的如
    * 字串 (`CharField`), 
    * 整數 (`IntegerField`), 
    * 日期 (`DateField`),
* 不同型態的資料有不同的參數設定，例如 `Charfield` 需要設定最大長度
* `__str__()` 用來設計該資料被要求顯示時，該如何顯示


```python
from django.db import models

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.firstname} {self.lastname}" 
```

#### 2. Migration

當我們對資料庫的格式進行了變更，就必須告知系統，有兩步驟：
1. 產生資料遷移檔 (makemigration)
2. 執行遷移 (migrate)

```shell
python manage.py makemigrations
python manage.py migrate
```

#### 3. 在終端機新增資料

進入終端機，進入 django 的環境：
```
python manage.py shell
```

查看資料

```python
from members.models import Member
Member.objects.all() # check all members
nick = Member(lastname='Hsueh',
              firstname='Nien-Lin') # new member
nick.save() 
Member.objects.all() # check again
Member.objects.all().values() # check detail values
```
❓ check the type of `Member.objects.all().values()`

❓ 如何在 shell 中直接執行一個 .py 檔來新增一群資料？

```shell
exec(open('path/to/your/file.py').read())
```

#### 4. 修改視界回應

```python
from django.http import HttpResponse
from django.template import loader
from .models import Member

def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('all_members.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))
```
* `context` 使用 `dict` 的結構封裝參數
* `template` 透過 `.render` 把參數 and 請求送到網頁 

#### 讀取與呈現資料


```html
<!DOCTYPE html>
<html>
<body>

<h1>Members</h1>
  
<ul>
  {% for x in mymembers %}
    <li>{{ x.firstname }} {{ x.lastname }}</li>
  {% endfor %}
</ul>

</body>
</html>
```
* 樣板變數 (template variable)
    * `{{ var }}`
* 樣板標籤 (template tag)
    * `{% for %}`, `{% endfor %}`
    * see [all template tag](https://docs.djangoproject.com/en/5.0/ref/templates/builtins/)