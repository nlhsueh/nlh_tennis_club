## 103-2 Quiz

* 下載 form_post 版本，安裝並啟動成功 (50%)
* 加上並呈現性別 (20%)
  * 將 member 加上 gender 的性別屬性，其型態是列舉型態的：男、女。現有資料中，設定至少兩人是男，兩人是女。
  * 修改 http://127.0.0.1:8000/members/, 點擊後會出現男女的分類，而非年齡的分類。
* 查詢性別 (20%)
  * 首頁 Member 下，加上一個 Query 的連結，點擊後出現可以依據男女查詢畫面，用下拉式，或是 radio 的方式選擇，按下提交後出現對應的會員。
* 透過修改 master.html 改變整體版面（如下方畫面）(10%)

### 作法

version
* 前一版本：web
* 此一本版：gender

Solution
* MODELS
  * 將 [Member](/members/models.py) 加上 gender 的性別屬性，其型態是列舉型態的：男、女。現有資料中，設定至少兩人是男，兩人是女。
    * 記得要進行 makemigrations, 及 migrate
    * 到 admin 下增加性別資料
  * 修改 [all_members.html](/members/templates/all_members.html)，依據性別作分類呈現。
* QUERY
  * 到 [urls.py](/members/urls.py) 中加上路徑 query, 指向 query_member()
  * 新增查詢頁面 [query.html](/members/templates/query_member.html)
  * 新增一個 [query form](/members/forms.py), 透過 Meta 的設定呈現 gender
  * 修改 [views.py](/members/views.py)，加上 query_member(). query_member() 會依據表單的性別進行 filter 的查詢，最後傳到 [queried_member.html](/members/templates/queried_member.html)
* PAGES
  * 透過修改 [master.html](/members/templates/master.html) 改變整體版面
    * 登入登出頁統合在網頁的上方
    * Member 下方多加一個 Query Members
  * 修改其他頁面，如 [main.html](/members/templates/main.html)  