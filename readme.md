# version img

前一版本：validation

資料庫的欄位可以存放影像檔。透過 admin 的介面，我們為每一個球場 (court) 加上照片。在觀看球場細部的時候，將之呈現。

[/courts/models.py](/courts/models.py)
* `Court` 的類別，加上 `photo` 的欄位，用來儲存照片。欄位的型態是 ImageField
* 透過 `upload_to` 來指定要上傳的目的地路徑。這裡路徑我們寫 `court_photos/`，是相對路徑，相對於 `setting` 中所設定的 `MEDIA_URL` 路徑。

[/my_tennis_club/settings.py](/my_tennis_club/settings.py)
* 新增 `MEDIA_URL` 及 `MEDIA_ROOT` 的路徑-- 這是所有上傳的檔案的根目錄。
    * [/my_tennis_club/urls.py](/my_tennis_club/urls.py) 需要新增 `urlpatterns: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`。因為會用到 `static` 和 `setting`, 所以也要記得做 `import`。

[/courts/admin.py](/courts/admin.py) 
* `list_display` 加上 `photo`, 以便在 admin 中呈現

[/courts/templates/all_courts.html](/courts/templates/all_courts.html) 
* 改用 bootstrap table 的方式呈現球隊列表
* `courttype` 如果直接印出，會印出他的 key ("G"), 我們想印出的是有意義的 value ("草地")，因此用 `{{ c.get_courttype_display }}`。 `get_xxx_display` 會印出 `xxx` 的 value。

[/courts/templates/court_details.html](/courts/templates/court_details.html) 印出球場的細節，這裡我們印出他的照片。用 bootstrap 的 `card` 元件來做輸出美化。

