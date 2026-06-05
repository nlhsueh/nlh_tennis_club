# Render.com 部署與排錯指南 (htmx 分支)

本指南詳細說明了 NLH Tennis Club 專案在 Render.com 上的部署配置、相關設定檔的作用，以及針對 SQLite 部署時常見問題的排除步驟。

---

## 📋 1. 部署環境設定檔說明

專案根目錄中新增了以下設定檔以支援 Render 雲端運作：

*   **[render.yaml](file:///Users/nickhsueh/MBAir22-tools/web/nlh_tennis_club_mba22/render.yaml)**：Render 的藍圖部署（Blueprints）描述檔，定義了 Web 服務的規格、建置及啟動命令，以及 Python 版本限制。
*   **[Procfile](file:///Users/nickhsueh/MBAir22-tools/web/nlh_tennis_club_mba22/Procfile)**：平台標準的程序設定檔。**在 Render 上，手動部署時 `Procfile` 定義的啟動命令擁有最高優先權**，會覆蓋 `render.yaml` 裡的 `startCommand`。
*   **[runtime.txt](file:///Users/nickhsueh/MBAir22-tools/web/nlh_tennis_club_mba22/runtime.txt)**：用於宣告雲端所安裝的 Python 環境版本（`python-3.11.15`），是 Render 手動部署與許多 Python Buildpack 偵測版本時的標準檔。
*   **[.python-version](file:///Users/nickhsueh/MBAir22-tools/web/nlh_tennis_club_mba22/.python-version)**：給本機開發工具（如 `pyenv`、`asdf`）自動切換 Python 版本的設定檔。

---

## ⚙️ 2. 部署方案與資料庫配置

依據您的需求，專案支援以下兩種資料庫部署方案。請配合修改 Render 後台的 **Start Command**（啟動指令）：

### 方案 A：使用 PostgreSQL（建議，可永久保存資料）
適合正式上線環境。資料庫為獨立服務，重啟網頁時資料不會遺失。

1. **Render 後台環境變數設定 (Environment)**：
   * 新增 `DATABASE_URL`，值填入您的 PostgreSQL **Internal Connection String**。
2. **Start Command** 設為：
   ```bash
   gunicorn my_tennis_club.wsgi --bind 0.0.0.0:$PORT
   ```
3. **備註**：在此方案下，您可以在 `render.yaml` 中使用 `releaseCommand: python manage.py migrate`，讓每次發布前自動進行結構遷移。

---

### 方案 B：使用 SQLite（簡易 Demo，重啟時會重置資料）
適合學生專案或快速展示。資料庫儲存在網頁容器內，無須額外付費建立資料庫服務。

> [!WARNING]
> Render 免費方案的網頁容器每 24 小時或在每次重新部署時都會重啟，**重啟後 SQLite 寫入的任何新資料（例如新的球場預約）都會被抹除並重置**。

1. **Render 後台環境變數設定 (Environment)**：
   * **不要**設定 `DATABASE_URL`。Django 會自動退回本機 `db.sqlite3` 檔案。
2. **Start Command** 必須設為（亦已寫入 `Procfile`）：
   ```bash
   python manage.py migrate && python manage.py loaddata initial_data.json && gunicorn my_tennis_club.wsgi --bind 0.0.0.0:$PORT
   ```
3. **為什麼要寫在啟動指令中？**
   因為 Render 的 `releaseCommand` 是在臨時的獨立容器中執行，跑完後變更隨即丟棄。我們必須在**真正的網頁服務容器啟動時（Start Command）**即時執行 `migrate` 建立資料表並 `loaddata` 載入初始成員與球場，網頁才能正常載入資料。

---

## 🛠️ 3. Render 後台手動部署步驟

如果您在 Render 控制台使用手動連線 GitHub 部署，請在服務的 **Settings** 中確認以下欄位：

*   **Runtime**：`Python`
*   **Build Command**：
    ```bash
    pip install -r requirements.txt && python manage.py collectstatic --noinput
    ```
*   **Start Command**（手動部署最關鍵，以**方案 B（SQLite）**為例）：
    ```bash
    python manage.py migrate && python manage.py loaddata initial_data.json && gunicorn my_tennis_club.wsgi --bind 0.0.0.0:$PORT
    ```
*   **Environment Variables**（環境變數頁籤）：
    *   `DJANGO_SECRET_KEY`：填入您的 Django Secret Key（非必填，預設有 fallback 替代）。
    *   `DEBUG`：設為 `False`（若需要偵錯可暫時設為 `True`）。
    *   `DJANGO_ALLOWED_HOSTS`：設為 `*` 或您的 Render 網域名稱（例如 `nlh-tennis-club.onrender.com`）。

---

## ❓ 4. 常見問題與排錯 (FAQ)

### Q1：點擊成員或球場頁面出現 500 錯誤，日誌顯示 `no such table: members_member`？
*   **原因**：這代表 Django 目前運行在 SQLite 下，但啟動時沒有順利執行資料庫遷移，導致資料庫檔案完全是空的。
*   **解決方法**：請前往 Render 後台的 **Settings** -> **Start Command**，確保設定值為下方指令，並手動點擊 **Manual Deploy -> Clear cache and deploy** 重新部署：
    ```bash
    python manage.py migrate && python manage.py loaddata initial_data.json && gunicorn my_tennis_club.wsgi --bind 0.0.0.0:$PORT
    ```

### Q2：`DEBUG = False` 在 Render 上運行，網頁上的圖片（例如球場照片）打不開？
*   **原因**：Django 預設在生產環境 (`DEBUG=False`) 下是不會主動回傳 `/media/` 底下的上傳圖片的。
*   **解決方法**：我們已在 `my_tennis_club/urls.py` 中加入了自動判定，當偵測到生產環境時會以 `django.views.static.serve` 當作備用回傳，因此無須任何額外設定，您的球場圖片即能在 Render 上流暢載入。

---

## 💻 5. 本機開發自動化（模擬雲端）

為了讓本機開發與雲端行為一致，我們提供了一個 [run_local.sh](file:///Users/nickhsueh/MBAir22-tools/web/nlh_tennis_club_mba22/run_local.sh) 腳本。

您在本機開發時，只需在終端機輸入：
```bash
./run_local.sh
```
即可自動「**啟用 venv 虛擬環境 ➡️ 套用最新 Database Migrations ➡️ 自動載入預設資料 ➡️ 啟動本機開發伺服器**」，無須手動輸入多個指令。
