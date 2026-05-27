
## Version `index`

前一版本：`details`

> [!NOTE]
> 🏈 You will do
> * 一個系統的首頁，並且讓其他分頁可以快速回到首頁
> * 如何關閉與開啟除錯模式
> * 當除錯模式關閉時，如何將系統錯誤引導到錯誤說明頁面。

* 做一個系統的主畫面- [main.html](/members/templates/main.html); 路由要記得設定 ([urls.py](/my_tennis_club/urls.py))
* 再設定檔 [setting.py](/my_tennis_club/settings.py) 關閉除錯模式 -- 也就是設定 `default=False`。系統出錯時，就不會出現除錯資訊，會自動轉到 `404.html`。
* 修改 [view.py](/members/views.py), 加上 `main(request)` 的導向
* 建立一新檔 [404.html](/members/templates/404.html)-- 撰寫系統出現時，要給使用者的訊息。
* 修改 [master.html](/members/templates/master.html), 加上回到首頁的連接。
* Read [w3school example](https://www.w3schools.com/django/django_add_main.php) for more information.