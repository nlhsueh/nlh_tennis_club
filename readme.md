
## 網球會員系統

前一版本：members

更新：
* 加入 joined_date 及 phone 等欄位，設定這些欄位的屬性，例如 default, verbose_name 等
* admin.py 中，admin 對 member 的註冊

啟動：
* py manage.py runserver
* 開啟瀏覽器：[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin), 使用 admin 和密碼 123 登入

學習內容
* 進入 admin 請觀察欄位的變化
* null=True 及 blank=Ture 的必要與差異
* makemigrations, migrate