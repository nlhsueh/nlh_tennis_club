## Django MVT 基礎課堂隨堂測驗 — Bootstrap 整合與生產部署 (Quiz)

本測驗旨在檢驗學生對於本單元（`bs` 分支：Bootstrap 網格排版系統、Django Form 樣式注入、Git 遠端連接重設、以及 Render.com 雲端部署配置）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 當我們在 Django 表單類別中（例如 `LoginForm`），希望讓 Django 自動渲染的輸入欄位套用 Bootstrap 的外觀樣式（需要加上 `class="form-control"`），最符合 Django 規範的作法是下列何者？
* (A) 在 HTML 模板中手動用正則表達式取代 `{{ form.username }}`。
* (B) 在 `forms.py` 宣告欄位時，透過 `widget=forms.TextInput(attrs={'class': 'form-control'})` 來注入 CSS 類別屬性。
* (C) 在 `models.py` 的模型欄位中加上 `class_name='form-control'` 屬性。
* (D) 在 `settings.py` 中全域設定 `BOOTSTRAP_ALL_FIELDS = True`。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* Django Form 允許我們透過 `widget` 的 **`attrs`** 參數傳入一個字典，用來定義渲染出來的 HTML 標籤屬性。
* 藉由在 `attrs` 中設定 `{'class': 'form-control'}`，Django 在將表單元件轉為 HTML 時，就會自動加上該 class，從而完美套用 Bootstrap 的輸入框樣式。
</details>

---

### 2. 關於 Bootstrap 的網格系統（Grid System），當我們在 HTML 中使用 `<div class="col-md-6">`，下列哪一個敘述是正確的？
* (A) 該元件在所有尺寸的螢幕下，都只會佔用螢幕總寬度的 6 像素。
* (B) 該元件會在中等螢幕尺寸（Medium devices, $\ge 768\text{px}$）及以上佔用 6 個網格（即整行 12 網格的一半，佔 $50\%$ 寬度）。
* (C) 該元件會把畫面強制切割成 6 等分，並在每一等分中垂直堆疊。
* (D) `col-md-6` 代表此區塊最多只能容納 6 張圖片或 6 行字。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* Bootstrap 網格系統將整行寬度劃分為 **12 個虛擬網格（Columns）**。
* `col-md-6` 的含義是：在 `md`（中等螢幕，如平板與小型筆電）及以上解析度時，該區塊佔用 $6/12 = 50\%$ 的寬度。當螢幕小於 `md` 閥值時，則會自動降級為預設的 $100\%$ 寬度（垂直堆疊），以實現響應式排版（Responsive Layout）。
</details>

---

### 3. 當我們將專案部署至 Render.com 等雲端平台上時，專案根目錄必須包含一個名為 `Procfile` 的檔案。關於該檔案的用途，下列敘述何者正確？
* (A) 它是用來告訴系統安裝哪些 Python 套件的版本清單。
* (B) 它是用來定義資料庫結構的備份腳本檔案。
* (C) 它是用於宣告該 Web 服務「啟動指令（Start Command）」的設定檔（例如指定使用 gunicorn 啟動並綁定 Port）。
* (D) 它是用來檢測使用者密碼強度的安全原則檔。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(C)**

**解析**：
* **`Procfile`**（沒有副檔名）是許多雲端部署平台（如 Render, Heroku）用來識別應用程式類型與啟動指令的檔案。
* 內容通常寫入如 `web: gunicorn my_tennis_club.wsgi --bind 0.0.0.0:$PORT`，指明這是一個 Web 服務，並在啟動時執行 Gunicorn 伺服器來監聽平台動態分配的連接埠。
</details>

---

### 4. 為了讓 Django 網站能安全且正確地在 Render.com 等 Production 環境中執行，我們在 `settings.py` 中進行了環境變數讀取。關於以下設定，哪一個敘述**錯誤**？
* (A) `DEBUG = False` 可以防止網站報錯時外洩內部程式碼與資料庫密碼。
* (B) `DJANGO_ALLOWED_HOSTS` 限制了哪些網址域名可以存取我們的 Django 服務，能防範 HTTP Host Header 攻擊。
* (C) 靜態檔案套件 `whitenoise` 允許 Django 在不依賴 Nginx 的情況下，安全地直接託管並壓縮 CSS/JS 等靜態資源。
* (D) 在 Production 環境中，我們應該繼續將 `DEBUG` 設為 `True`，以便隨時在瀏覽器上查看最新的報錯日誌。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(D)**

**解析**：
* 正式部署上線時，為了資訊安全，**必須將 `DEBUG` 設為 `False`**。
* 若持續開啟 `DEBUG=True`，任何造訪者一旦遇到 404 或 500 錯誤，都能在瀏覽器中直接看到伺服器內部堆疊 Traceback、環境變數與金鑰，造成極大資安風險。
</details>

---

### 5. 如果你想將一個原本綁定了老師 GitHub 專案的本地 Git 儲存庫，改為推送到「你自己」新建的 GitHub 儲存庫，應在終端機依序執行哪些 Git 命令？
* (A) `git clone` ➔ `git push`
* (B) `git remote remove origin` ➔ `git remote add origin <你的儲存庫網址>` ➔ `git push -u origin bs`
* (C) `git init` ➔ `git checkout` ➔ `git merge`
* (D) `git pull` ➔ `git config --global user.name`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 為了重置遠端連線，必須先使用 `git remote remove origin` 斷開原本的關聯。
* 再使用 `git remote add origin <URL>` 綁定你自己的 GitHub 新建儲存庫。
* 最後使用 `git push -u origin <分支名>` 將代碼推送到你自己的遠端儲存庫中。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請詳細說明：在 Production 生產環境中，Django 預設的靜態檔案機制會遇到什麼問題？我們在本單元中引入的 `whitenoise` 套件，是如何協助解決這個問題的？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **Django 預設問題**：Django 的設計理念是只負責動態邏輯。當 `DEBUG = False` 時，Django 會自動**停止**託管靜態檔案（CSS、JS、Images）。在傳統部署中，必須在 Django 前方架設一個專門的網頁伺服器（如 Nginx 或 Apache）來處理靜態檔，這對簡單的雲端部署（如 Render 免費版）來說非常複雜。
2. **Whitenoise 的解決方案**：`whitenoise` 是一個專為 Python Web 應用設計的輕量級靜態檔案管理套件。它以中間件（Middleware）的形式直接嵌入 Django 中（透過 `WhiteNoiseMiddleware`）。當瀏覽器請求靜態檔案時，`whitenoise` 會在 Django 層級直接攔截並處理，且支援檔案壓縮（gzip/brotli）與快取標頭設定。這讓 Django 能夠在不架設額外 Nginx 的情況下，獨立、高效、安全地託管自己所有的靜態檔案，極大簡化了部署架構。
</details>

---

### 7. 請解釋在 Render.com 部署中，`render.yaml`（Blueprint Spec）檔案的主要用途是什麼？它對於團隊協作或學生交作業有什麼好處？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **主要用途**：`render.yaml` 是 Render 平台的基礎設施即代碼（Infrastructure as Code, IaC） Spec 檔案。它用來以代碼形式宣告該專案所需的所有雲端基礎設施設定，包括服務類型（`web`）、名稱、運行環境（`python`）、建置指令（`buildCommand`）、啟動指令（`startCommand`）以及 Python 版本。
2. **好處**：
   - **一鍵部署**：學生或團隊成員不需要手動在網頁後台點選、記憶並填寫複雜的指令與路徑，Render 會直接讀取此檔案並自動組裝完畢。
   - **一致性**：確保每個人部署出來的環境（包含 Python 版本、資料庫遷移命令）完全一致，避免因手動設定出錯（Human Error）而導致的「在我的電腦可以跑，但部署上去就壞掉」的問題。
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 請完成以下 `views.py` 或 `forms.py` 的表單類別填空，使其能夠在渲染為 HTML 表單時，自動為 input 輸入框注入 Bootstrap 的 `form-control` 樣式：
```python
# web/forms.py
from django import forms

class LoginForm(forms.Form):
    # 1. 宣告一個 TextInput 元件，並在 attrs 中設定 class 屬性為 form-control
    username = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(
            attrs={___(1)___: ___(2)___}
        )
    )
    
    password = forms.CharField(
        max_length=20, 
        widget=forms.PasswordInput(
            attrs={___(1)___: ___(2)___}
        )
    )
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `'class'` (或 `"class"`)
* `(2)`: `'form-control'` (或 `"form-control"`)
</details>

---

### 9. 以下是專案根目錄下 `render.yaml` 藍圖設定檔與部分 `settings.py` 內容。請填入正確的設定屬性或指令參數，以確保雲端平台能正確編譯並執行網站：

```yaml
# render.yaml
services:
  - type: web
    name: nlh-tennis-club
    env: python
    branch: bs
    # 1. 填入建置指令：安裝依賴 ➔ 資料庫遷移 ➔ 靜態檔案收集
    buildCommand: pip install -r requirements.txt && python manage.py migrate && python manage.py ___(1)___ --noinput
    # 2. 填入啟動指令：使用 gunicorn 啟動服務並綁定 Port
    startCommand: ___(2)___ my_tennis_club.wsgi:application --bind 0.0.0.0:$PORT
```

```python
# my_tennis_club/settings.py
# 3. 讀取環境變數中的金鑰，若無則使用預設值
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-key')

# 4. 讀取環境變數中的 DEBUG 設定，並轉為布林值
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

# 5. 啟用 whitenoise 的中間件，使其託管靜態檔案 (必須放在 SecurityMiddleware 之後)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.___(3)___',
    # ... 其他中間件 ...
]
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `collectstatic`
* `(2)`: `gunicorn`
* `(3)`: `WhiteNoiseMiddleware`

**解析**：
* `collectstatic` 是 Django 用於將所有 App 與全域的靜態資源統整並複製到 `STATIC_ROOT`（本例中為 `staticfiles/`）的終端機管理命令。
* `gunicorn` 是一個 Python WSGI HTTP 伺服器，常用於 Production 環境中啟動 Django。
* `WhiteNoiseMiddleware` 中間件必須緊跟在 `SecurityMiddleware` 之後，以便在第一時間攔截並回應靜態檔案請求，提供最高效的靜態檔案託管服務。
</details>
