
## 網球會員系統

本版本：form_post
前一版本：form_get

更新：
* 使用 ModelForm 來製作輸入介面

啟動：
* py manage.py runserver
* 開啟瀏覽器：[http://127.0.0.1:8000](http://127.0.0.1:8000)
* 點選 /members/new_member 連接

學習內容
* 了解 form 的設計: Form 和 Model 的差異
* get 和 post 的差異; 運作時機
* post 後, 如何 save 到資料庫

You should know
* 當我們連接到一個有 form 的頁面，先是一個 GET 的請求，當我們按下 submit 時，可能會送出 GET 或 POST -- 依據 form method 的指定。