# 網球俱樂部 (Tennis Club) - 基礎起始專案

這是一個乾淨的、已初始化好基礎結構的 Django 起始專案。本專案作為課堂教學與學生實作的起點，不包含任何自訂的應用程式（Apps）、模型（Models）或視圖（Views），供您與學生從零開始學習並建立專案。

---

## 🛠️ 開發環境準備與執行步驟

請依照以下步驟在您的電腦上啟動此專案：

### STEP 1: 建立並啟用虛擬環境 (Virtual Environment)
虛擬環境能確保此專案的套件版本與您電腦中其他專案完全隔離，避免套件衝突。

* **建立虛擬環境**：
  ```bash
  # macOS / Linux / Windows (Python 3.12+)
  python -m venv venv
  ```

* **啟用虛擬環境**：
  * **macOS / Linux**：
    ```bash
    source venv/bin/activate
    ```
  * **Windows (PowerShell)**：
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
  * **Windows (CMD)**：
    ```cmd
    .\venv\Scripts\activate.bat
    ```

---

### STEP 2: 安裝必要套件
本專案已備妥 `requirements.txt`，請在**啟用虛擬環境後**執行以下指令安裝 Django 及其相依套件：

```bash
python -m pip install -r requirements.txt
```

---

### STEP 3: 執行資料庫遷移
初次執行前，請先執行資料庫遷移以初始化 Django 內建系統（如管理者、使用者驗證等）所需的資料庫結構：

```bash
python manage.py migrate
```

---

### STEP 4: 啟動 Django 開發伺服器
執行以下指令來啟動本機伺服器：

```bash
python manage.py runserver
```

啟動後，開啟瀏覽器並輸入 `http://127.0.0.1:8000/`，即可看到 Django 的火箭歡迎頁面，代表系統已成功順利運作！
