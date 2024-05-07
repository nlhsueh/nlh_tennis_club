
## 網球會員系統

前一版本：admin

更新：
* master-details 來呈現資料：all_members.html 呈現所有資料的概述; details 呈現個別資料的內容。
* 使用 master-extending 來組織網頁，master 的頁面可以被其他頁面來擴充，達到一致風格。

啟動：
* py manage.py runserver
* 開啟瀏覽器：[http://127.0.0.1:8000/members](http://127.0.0.1:8000/members)

學習內容
* 學習 master-details 的架構，包含 urls 的設定，view 的寫法與 template 的設計
* 了結 master-extending 的 web 組織架構