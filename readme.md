# version Static

加上 static files, 例如 .css, .js, images 等靜態檔案。路徑要對，程式才能抓得到

## Steps
* 在專案目錄下新增 [/static](/static) 目錄，裡面再新增 css, js, img 等目錄
  * 放一些圖片，和設定檔到適當的目錄下
* 到 [/my_tennis_club/settings.py](/my_tennis_club/settings.py) 下找到 `STATIC_URL` 的設定，在下方新增：
```python
STATICFILES_DIRS = [BASE_DIR / "static"]
```
* 你可以到 shell 中檢測這些變數的值
```
python manage.py shell
```
```
from django.conf import settings
print("BASE_DIR:", settings.BASE_DIR)
print("STATICFILES_DIRS:", settings.STATICFILES_DIRS)
```
* 引用這些檔案：
  * [/members/templates/master.html](/members/templates/master.html) 我們在母片檔將這些設置加進去。注意要先執行 `{% load static %}`。

```html
{% load static %}
<link rel="stylesheet" href="{% static '/css/club.css' %}"> 
... 
<br><img src='/static/img/garros.png' width='200' height='150'>
<img src= {% static '/img/centre.jpeg' %} width='200' height='150'>
```
* 上方的 img 我特別寫了兩種方式，展示 static 的意義。