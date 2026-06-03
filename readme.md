# version bs

using bootstrap

[/members/templates/master.html](/members/templates/master.html)
* 加上匯入 bs 的指令
* 透過 `class="p-5 bg-primary text-white rounded"` 建立一個首頁的標示牆
* 透過 `class="container-fluid"` 做一個大頁面，裡面放一個列表，透過 `class=nav, nav-item, nav-link`
* 列表：HOME, ADMIN, login/logout, My-booking
* 透過 <footer> 製作一個頁尾。

[/members/templates/main.html](/members/templates/main.html)
* 透過 container 製作一個非滿版的容器; 透過 col-sm-3 放置四個圖片 (12/3=4)
* 再放一個 container 容器，裡面放一些文字。假設我們一列要有兩行，所以用 `col-md-6` (12/6=2)。

[/web/templates/login.html](/web/templates/login.html)
* 登入頁面 label 標記為 form-label

[/web/forms.py](/web/forms.py)
* username 和 password 也需要改成 form-control, 所以設定 widget 的 attrs
```
    username = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
```

## 部署到 Render.com

本專案已完成所有的雲端部署配置（包含 `render.yaml`、`Procfile` 等部署檔案），並將靜態檔案管理設定為適用於 Production 環境的 `whitenoise`。請引導學生依照以下三大階段，完成專案的上傳與雲端部署：

---

### 第一階段：將本地專案上傳至個人的 GitHub 儲存庫

1. **在 GitHub 上建立儲存庫**：
   - 登入個人 [GitHub](https://github.com/) 帳號，點選右上角的 **New** 建立新儲存庫。
   - **Repository name**：輸入 `nlh_tennis_club` (或任何你喜歡的名稱)。
   - **權限選擇**：建議選擇 **Public** (公開) 或 **Private** (私有) 皆可。
   - **⚠️ 關鍵注意**：**「不要」**勾選 "Add a README file"、"Add .gitignore" 或 "Choose a license"。因為我們的本地專案中已經有這些配置檔案，勾選會導致兩端衝突。
   - 點選底部的 **Create repository**。

2. **在本地終端機（Terminal）設定遠端網址**：
   - 開啟你的命令提示字元（Windows 的 CMD 或 PowerShell）或終端機（Mac/Linux），切換到當前專案目錄。
   - 為了將你的專案推送到「你自己」的 GitHub，請先刪除原本綁定老師專案的 Remote 連線，並綁定為你的 GitHub 儲存庫：
     ```bash
     # 1. 移除預設的 remote 連線
     git remote remove origin

     # 2. 新增你剛剛在 GitHub 建立的專案網址（請將其中的 <your-github-username> 換成你的帳號）
     git remote add origin https://github.com/<your-github-username>/nlh_tennis_club.git
     ```

3. **提交本地代碼並推送至 GitHub**：
   - 確認你當前正處於正確的開發分支（例如本單元的 `bs` 分支）：
     ```bash
     # 檢查當前分支，確認有帶 * 號標記在 'bs' 上
     git branch
     ```
   - 執行以下指令，將所有程式碼提交並推送到 GitHub：
     ```bash
     # 1. 將所有修改與新檔案加入暫存區
     git add .

     # 2. 提交變更並撰寫提交訊息
     git commit -m "prepare for deployment"

     # 3. 將程式碼推送至你專屬的 GitHub 儲存庫 (以當前分支 bs 為例)
     git push -u origin bs
     ```

---

### 第二階段：在 Render.com 部署你的 Django 網站

我們提供兩種部署方式，**方式 A（最推薦，一鍵部署）** 或是 **方式 B（手動在網頁後台配置）**：

#### 💡 方式 A：使用 Blueprint 藍圖一鍵部署（最不易出錯）
因為專案根目錄中已內建寫好 [render.yaml](file:///Users/nickhsueh/MBAir22-tools/web/nlh_tennis_club_mba22/render.yaml) 藍圖設定檔，Render 能自動讀取它並建立網站與相關配置：
1. 登入 [Render.com](https://render.com/) (建議直接點選 **GitHub** 登入以連結帳號)。
2. 進入控制台首頁後，點選右上角的 **New +** ➔ 選擇 **Blueprint**。
3. 在下方儲存庫列表中，選取你剛剛上傳的 `nlh_tennis_club` 專案（若未顯示，可依提示點選連結進行授權）。
4. 進入 Blueprint 建立頁面：
   - **Service Group Name**：自訂一個服務組別名稱（例如 `tennis-club-group`）。
   - **Branch**：確認選擇你推送到 GitHub 的分支（例如 `bs`）。
5. 點選藍色的 **Approve** 按鈕。
6. Render 會自動啟動 Web 服務並開始安裝套件、轉移資料庫與收集靜態檔案。你只需靜待其建置完成即可！

---

#### 🛠️ 方式 B：手動建立 Web Service 部署（手把手配置）
如果你希望自己練習手動填寫每一項雲端設定，請依照以下步驟：
1. 登入 [Render.com](https://render.com/) ➔ 點選右上角的 **New +** ➔ 選擇 **Web Service**。
2. 選擇第一項 **Build and deploy from a Git repository**，然後點選你 GitHub 上的 `nlh_tennis_club` 專案。
3. 填寫 Web Service 基礎設定：
   - **Name**：輸入你的服務名稱（如 `my-tennis-club-app`）。
   - **Region**：建議選擇 `Singapore` (新加坡)，離台灣較近，連線速度較快。
   - **Branch**：選擇你推送程式碼的分支（例如 `bs`）。
   - **Runtime**：選擇 `Python`。
4. 設定建置指令與啟動指令：
   - **Build Command**：填入以下指令（安裝 requirements 套件、自動套用資料庫遷移、並執行靜態檔收集）：
     ```bash
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command**：填入以下啟動 Gunicorn 伺服器的指令：
     ```bash
     gunicorn my_tennis_club.wsgi:application --bind 0.0.0.0:$PORT
     ```
5. **設定環境變數 (Environment Variables)**：
   - 點選設定頁面下方的 **Advanced** 展開進階設定。
   - 點選 **Add Environment Variable** 新增以下三個關鍵變數（若無設定，網站將無法安全運行）：
     1. 鍵（Key）：`DJANGO_SECRET_KEY`  
        值（Value）：`輸入任意一長串隨機英數字或特殊符號`（作為 Django 運算加密憑證的安全金鑰）。
     2. 鍵（Key）：`DEBUG`  
        值（Value）：`False`（在雲端正式環境中，**必須關閉**除錯模式，以防系統敏感錯誤資訊外洩）。
     3. 鍵（Key）：`DJANGO_ALLOWED_HOSTS`  
        值（Value）：`*`（或輸入你部署成功後 Render 分配給你的網址，例如 `my-tennis-club-app.onrender.com`）。
6. 確認填寫無誤後，點選最下方的 **Create Web Service** 開始部署。

---

### 第三階段：確認與測試

1. **觀察建置日誌 (Build Logs)**：
   - 在 Render Dashboard 的 Logs 中可以看見伺服器正在執行套件安裝與 `collectstatic`。
   - 當 Logs 最後顯示出：
     ```text
     ==> Uploading build...
     ==> Deploying...
     ==> Your service is live.
     ```
     代表你的 Django 網站已在雲端成功上線！
2. **存取網站**：
   - 點選網頁左上角、服務名稱下方提供的免費專屬 URL（例如：`https://xxxx.onrender.com`），即可立即在瀏覽器中看到你的網球會員系統首頁！
3. **資料庫說明**：
   - 本專案預設使用本機 SQLite 資料庫，在 Render 容器中會產生本地 SQLite 檔案。
   - ⚠️ **備註**：由於免費版 Render Web Service 每隔一段時間未連線會進入休眠，且每次重啟時容器會重置（Ephesmeral File System），這會導致 SQLite 中新增的測試資料消失。若需要永久保存資料，實務上需付費升級，或將 `DATABASE_URL` 環境變數對接到外部的 PostgreSQL 資料庫（如 Render 提供之 Postgres Database 服務）。