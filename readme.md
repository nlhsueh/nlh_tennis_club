# 版本：HTMX 重構

## 概述
本分支旨在將傳統的全頁面刷新 Django 應用程式重構為使用 HTMX 的現代化動態應用程式。
使用 HTMX 可以提供更好的使用者體驗，減少頁面加載時間，並簡化前後端互動。

**前一版本**：bind_user

---

## 為什麼使用 HTMX？

### 傳統方式的問題
- 每次操作都需要完整頁面刷新
- 使用者體驗不流暢
- 需要寫大量 JavaScript 來處理非同步請求
- DOM 需要完全重新渲染

### HTMX 的優點
1. **直接在 HTML 中聲明互動**：使用 HTML 屬性（如 `hx-get`, `hx-post`）
2. **無縫頁面更新**：只更新需要變更的部分 DOM
3. **最小化 JavaScript**：大部分邏輯保持在後端
4. **改善使用者體驗**：快速響應，無頁面閃爍

---

## 快速開始指南

### ✨ 第一步：了解文件結構

**已存在的文件**（無需修改）：
- ✅ [members/templates/master.html](members/templates/master.html) - 主模板（已添加 HTMX）
- ✅ [members/templates/all_members.html](members/templates/all_members.html) - 成員列表頁面
- ✅ [members/templates/details.html](members/templates/details.html) - 成員詳情頁面
- ✅ [courts/templates/all_courts.html](courts/templates/all_courts.html) - 場館列表頁面
- ✅ [courts/templates/court_details.html](courts/templates/court_details.html) - 場館詳情頁面
- ✅ [members/views.py](members/views.py) - 成員視圖
- ✅ [courts/views.py](courts/views.py) - 場館視圖

**需要創建的目錄**：
```bash
mkdir -p members/templates/fragments
mkdir -p courts/templates/fragments
```

**需要創建的新片段文件**：

**成員模塊**：
- [members/templates/fragments/member_list.html](members/templates/fragments/member_list.html) - 成員列表片段
- [members/templates/fragments/member_item.html](members/templates/fragments/member_item.html) - 單個成員項目
- [members/templates/fragments/member_detail_modal.html](members/templates/fragments/member_detail_modal.html) - 成員詳情模態
- [members/templates/fragments/member_edit_form.html](members/templates/fragments/member_edit_form.html) - 成員編輯表單

**場館模塊**：
- [courts/templates/fragments/court_list.html](courts/templates/fragments/court_list.html) - 場館列表片段
- [courts/templates/fragments/booking_form.html](courts/templates/fragments/booking_form.html) - 預訂表單片段

---

## 重構計畫 (5 個階段)

### 📋 第 1 階段：基礎設置

#### 1.1 安裝 HTMX 庫
在 [master.html](members/templates/master.html) 中添加
```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
```

#### 1.2 創建 AJAX 響應視圖
傳統視圖返回完整 HTML 頁面，AJAX 視圖只返回 HTML 片段（fragment）。

**原理**：
- 新增一個參數檢查：`if request.headers.get('HX-Request')`
- 如果是 HTMX 請求，返回只含內容的片段
- 如果是普通請求，返回完整頁面

**範例**（修改 [members/views.py](members/views.py)）：
```python
def members(request):
    mymembers = Member.objects.all()
    
    # HTMX AJAX 請求 → 只返回列表片段
    if request.headers.get('HX-Request'):
        return render(request, 'fragments/member_list.html', {'mymembers': mymembers})
    
    # 普通請求 → 返回完整頁面
    return render(request, 'all_members.html', {'mymembers': mymembers})
```

#### 1.3 建立片段模板目錄

需要在 `members/templates/` 下創建新的 `fragments/` 資料夾及以下文件：
```
members/templates/
├── master.html                   # 已存在 ✓
├── all_members.html              # 已存在 ✓
├── details.html                  # 已存在 ✓
├── fragments/                    # 需要創建
│   ├── member_list.html          # 新建 - 成員列表片段
│   ├── member_item.html          # 新建 - 單個成員項目
│   ├── member_detail_modal.html  # 新建 - 成員詳情模態
│   └── member_edit_form.html     # 新建 - 成員編輯表單
```

---

### 👥 第 2 階段：成員應用增強

#### 2.1 實時搜尋/篩選（無頁面刷新）

**目標**：使用者輸入時，動態篩選成員列表

**實現步驟**：

1. **修改 [all_members.html](members/templates/all_members.html)（已存在）**，在其中添加搜尋表單：
```html
<!-- all_members.html -->
<input type="text" 
       name="search" 
       placeholder="搜尋成員..."
       hx-get="/members/"
       hx-target="#member-list"
       hx-trigger="input changed delay:500ms">

<div id="member-list">
  {% include "fragments/member_list.html" %}
</div>
```

2. **在 [members/views.py](members/views.py) 中處理搜尋參數**：
```python
def members(request):
    mymembers = Member.objects.all()
    
    # 處理搜尋
    search_query = request.GET.get('search', '')
    if search_query:
        mymembers = mymembers.filter(
            Q(firstname__icontains=search_query) | 
            Q(lastname__icontains=search_query)
        )
    
    if request.headers.get('HX-Request'):
        return render(request, 'fragments/member_list.html', {'mymembers': mymembers})
    
    return render(request, 'all_members.html', {'mymembers': mymembers})
```

**HTMX 屬性說明**：
- `hx-get="/members/"` - 執行 GET 請求到該 URL
- `hx-target="#member-list"` - 將響應內容放入此 ID 的元素
- `hx-trigger="input changed delay:500ms"` - 延遲 500ms 後才發送請求

#### 2.2 成員詳情模態視圖

**目標**：點擊成員時，在模態視窗中顯示詳情，而不刷新頁面

**實現步驟**：

1. **創建新文件 [member_item.html](members/templates/fragments/member_item.html)**（成員項目片段），在其中添加 HTMX 觸發器：
```html
<!-- fragments/member_item.html -->
<li class="list-group-item" 
    hx-get="{% url 'member_detail_modal' x.id %}"
    hx-target="#modal-content"
    data-bs-toggle="modal"
    data-bs-target="#memberModal"
    style="cursor: pointer;">
  {{ x.lastname }}{{ x.firstname }} ({{ x.age }} 歲)
</li>
```

2. **在 [members/views.py](members/views.py) 中創建返回模態內容的視圖**：
```python
def member_detail_modal(request, id):
    mymember = Member.objects.get(id=id)
    return render(request, 'fragments/member_detail_modal.html', {'mymember': mymember})
```

3. **創建新文件 [member_detail_modal.html](members/templates/fragments/member_detail_modal.html)**（詳情模態片段）：
```html
<!-- fragments/member_detail_modal.html -->
<div class="modal-header">
  <h5>成員詳情</h5>
</div>
<div class="modal-body">
  <p><strong>姓名</strong>：{{ mymember.lastname }}{{ mymember.firstname }}</p>
  <p><strong>電話</strong>：{{ mymember.phone }}</p>
  <p><strong>年齡</strong>：{{ mymember.age }}</p>
  <p><strong>入會日期</strong>：{{ mymember.joined_date }}</p>
</div>
```

#### 2.3 內聯編輯成員資訊

**目標**：直接在列表中編輯成員資訊，無需另開頁面

**實現步驟**：

1. **添加編輯按鈕**：
```html
<button hx-get="{% url 'edit_member_form' x.id %}"
        hx-target="#member-{{ x.id }}"
        hx-swap="outerHTML">
  編輯
</button>
```

2. **創建新文件 [member_edit_form.html](members/templates/fragments/member_edit_form.html)**（編輯表單片段）在 [members/views.py](members/views.py) 中返回編輯表單
```python
def edit_member_form(request, id):
    member = Member.objects.get(id=id)
    return render(request, 'fragments/member_edit_form.html', {'member': member})
```

3. **在 [members/views.py](members/views.py) 中處理表單提交**：
```python
def update_member(request, id):
    member = Member.objects.get(id=id)
    
    if request.method == 'POST':
        member.firstname = request.POST.get('firstname')
        member.lastname = request.POST.get('lastname')
        member.phone = request.POST.get('phone')
        member.age = request.POST.get('age')
        member.save()
        
        # 返回更新後的項目
        return render(request, 'fragments/member_item.html', {'x': member})
```

4. **創建新文件 [member_edit_form.html](members/templates/fragments/member_edit_form.html)**（編輯表單片段）：
```html
<!-- fragments/member_edit_form.html -->
<form hx-post="{% url 'update_member' member.id %}"
      hx-target="#member-{{ member.id }}"
      hx-swap="outerHTML">
  {% csrf_token %}
  <input type="text" name="firstname" value="{{ member.firstname }}" required>
  <input type="text" name="lastname" value="{{ member.lastname }}" required>
  <input type="number" name="phone" value="{{ member.phone }}">
  <input type="number" name="age" value="{{ member.age }}">
  <button type="submit">保存</button>
  <button type="button" hx-get="{% url 'member_detail' member.id %}" hx-target="this" hx-swap="outerHTML">
    取消
  </button>
</form>
```

---

### 🏓 第 3 階段：場館與預訂系統增強

#### 3.1 動態場館列表與篩選

**目標**：按場館類型和城市篩選，無需刷新頁面

**實現步驟**：

1. **修改 [all_courts.html](courts/templates/all_courts.html)（已存在）**，添加篩選器：
```html
<select name="court-type" 
        hx-get="/courts/"
        hx-target="#court-list"
        hx-include="[name='city']">
  <option value="">全部類型</option>
  <option value="G">草地</option>
  <option value="H">硬地</option>
</select>

<div id="court-list">
  {% include "fragments/court_list.html" %}
</div>
```

2. **在 [courts/views.py](courts/views.py) 中處理篩選**：
```python
def courts(request):
    courts = Court.objects.all()
    
    court_type = request.GET.get('court-type')
    city = request.GET.get('city')
    
    if court_type:
        courts = courts.filter(courttype=court_type)
    if city:
        courts = courts.filter(city=city)
    
    if request.headers.get('HX-Request'):
        return render(request, 'fragments/court_list.html', {'courts': courts})
    
    return render(request, 'all_courts.html', {'courts': courts})
```

#### 3.2 預訂表單動態加載

**目標**：點擊場館時，在模態中顯示預訂表單，實時驗證可用性

**實現步驟**：

1. **修改 [court_details.html](courts/templates/court_details.html)（已存在）**，添加觸發器：
```html
<div class="court-card"
     hx-get="{% url 'booking_form' court.id %}"
     hx-target="#booking-modal"
     style="cursor: pointer;">
  {{ court.courtname }}
</div>
```

2. **在 [courts/views.py](courts/views.py) 中新增視圖返回預訂表單**：
```python
def booking_form(request, court_id):
    court = Court.objects.get(id=court_id)
    existing_bookings = Booking.objects.filter(court=court)
    
    return render(request, 'fragments/booking_form.html', {
        'court': court,
        'existing_bookings': existing_bookings
    })
```

3. **創建新文件 [booking_form.html](courts/templates/fragments/booking_form.html)**（預訂表單片段），進行即時驗證日期可用性：
```html
<!-- fragments/booking_form.html -->
<form hx-post="{% url 'create_booking' %}"
      hx-target="#booking-result">
  {% csrf_token %}
  <input type="hidden" name="court_id" value="{{ court.id }}">
  
  <label>預訂日期</label>
  <input type="date" name="booking_date" 
         hx-post="{% url 'check_availability' %}"
         hx-target="#availability-check"
         required>
  <div id="availability-check"></div>
  
  <button type="submit">確認預訂</button>
</form>
```

4. **在 [courts/views.py](courts/views.py) 中新增檢查可用性視圖**：
```python
def check_availability(request):
    court_id = request.POST.get('court_id')
    booking_date = request.POST.get('booking_date')
    
    existing = Booking.objects.filter(
        court_id=court_id,
        booking_date=booking_date
    ).exists()
    
    if existing:
        return HttpResponse('<span class="text-danger">此日期已被預訂</span>')
    else:
        return HttpResponse('<span class="text-success">可預訂</span>')
```

---

### ✨ 第 4 階段：使用者體驗增強

#### 4.1 表單驗證反饋

**目標**：實時顯示表單驗證錯誤，無需提交

```html
<form hx-post="{% url 'update_member' member.id %}">
  {% csrf_token %}
  
  <input type="text" name="firstname" required
         hx-validate
         hx-target="next .error-message">
  <span class="error-message"></span>
</form>
```

#### 4.2 刪除確認對話框

**目標**：刪除前顯示確認，防止誤操作

```html
<button hx-delete="{% url 'delete_member' member.id %}"
        hx-confirm="確定要刪除此成員嗎？"
        class="btn btn-danger">
  刪除
</button>
```

#### 4.3 載入指示器與成功提示

**目標**：顯示操作狀態反饋

```html
<!-- 自動顯示載入中指示器 -->
<div id="member-list" 
     hx-get="/members/"
     hx-indicator="#loading">
  <img id="loading" class="htmx-indicator" src="/static/spinner.gif" />
  成員列表...
</div>

<!-- 操作後顯示成功訊息 -->
<button hx-post="{% url 'create_booking' %}"
        hx-on::after-request="if(event.detail.xhr.status===201) { alert('預訂成功！'); window.location.reload(); }">
  預訂
</button>
```

---

### 🚀 第 5 階段：進階功能（可選）

#### 5.1 即時通知系統
- 使用 Server-Sent Events (SSE) 推送預訂更新通知
- 實現長連接，無需輪詢

#### 5.2 拖放排序
- 使用 HTMX 重新排序預訂
- 前端拖放，後端持久化順序

#### 5.3 無限滾動分頁
- 頁面向下滾動時自動加載下一頁
- 實現 `hx-trigger="scroll end"`

---

## 實施建議

### ✅ 最佳實踐

1. **保持後端邏輯完整**
   - 所有驗證應在伺服器端進行
   - 前端 HTMX 只負責 UI 互動

2. **使用 HTML 片段（Fragments）**
   - 創建可重用的 HTML 片段
   - 在完整頁面和 AJAX 響應中使用

3. **CSRF 保護**
   - 在所有 POST/PUT/DELETE 請求中包含 CSRF token
   ```html
   <form hx-post="..." hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
   ```

4. **HTTP 方法語義**
   - `hx-get` - 獲取資料
   - `hx-post` - 創建/更新資料
   - `hx-put` - 完整替換資源
   - `hx-delete` - 刪除資源

5. **性能優化**
   - 使用 `hx-swap="outerHTML swap:1s"` 控制動畫
   - 使用 `hx-include` 包含多個表單字段
   - 實現伺服器端分頁，限制返回項目數

### 🧪 測試步驟

```bash
# 1. 啟動開發伺服器
python manage.py runserver

# 2. 在瀏覽器中開發者工具查看：
# - Network 標籤：檢查 HX-Request 頭
# - Console 標籤：HTMX 事件日誌

# 3. 測試各個功能
# - 搜尋篩選
# - 模態視窗加載
# - 表單提交與驗證
```

### 📚 學習資源

- [HTMX 官方文檔](https://htmx.org/)
- [HTMX 屬性參考](https://htmx.org/reference/)
- [HTMX 事件系統](https://htmx.org/events/)
- Django 與 HTMX 整合最佳實踐

---

## 版本歷史

- **htmx** (當前分支) - HTMX 重構版本
- **bind_user** - 前一個分支，使用傳統全頁刷新方式

---

## 🛠️ 已完成之實作細節 (Implementation Details)

在本次的更新中，我們已將原先預先準備好的 HTMX fragments 完全整合進系統頁面與後端視圖中，主要完成了以下項目：

### 1. UI 頁面的 HTMX 整合
* **`members/templates/all_members.html`**：
  - 移除了原本靜態渲染的迴圈，改以 `{% include "fragments/member_list.html" %}` 替代。
  - 新增了具備 HTMX 屬性的搜尋框 (`<input hx-get="{% url 'members' %}" hx-target="#member-list" hx-trigger="input changed delay:500ms">`)，達到輸入時即時過濾成員列表的效果。
  - 加入了 Bootstrap 的 Modal 容器 (`<div id="modal-content">`) 與 `showModal()` JavaScript 函式，供片段動態載入成員詳情與編輯表單。
* **`courts/templates/all_courts.html`**：
  - 移除了原先的靜態表格，改用 `{% include "fragments/court_list.html" %}`。
  - 實作了 HTMX 下拉選單 (`<select hx-get="{% url 'courts' %}" hx-target="#court-list">`)，實現不刷新頁面的場地類型與城市過濾。
  - 加入了對應的 Modal 容器與腳本，使場地詳情與預訂表單能在彈出視窗中無縫操作。

### 2. 後端視圖 (Views) 支援 HTMX 請求
* **`members/views.py` 與 `courts/views.py`**：
  - 於 `members()` 和 `courts()` 列表視圖中，加入了過濾器邏輯，並使用 `if request.headers.get('HX-Request'):` 進行判斷。若偵測到是 HTMX 發出的 AJAX 請求，則只回傳對應的局部 HTML 片段 (例如 `fragments/member_list.html`)，而非整個包含框架的完整頁面。
  - 於 `courts` 的 `details()` 視圖中，加入了相同的判斷以回傳新建立的 `court_detail_modal.html` 模態框片段，確保從列表點擊場館時可以完美顯示在彈出視窗中。

### 3. URL 路由與附屬端點擴充
* 為了讓前端的片段能正確與後端互動，我們在 `urls.py` 中新增了對應的路由與視圖處理：
  - **Members 模塊**：新增 `member_detail` (用於在 Modal 顯示詳情)、`edit_member_form` (用於載入內聯編輯表單) 以及 `update_member` (用於處理 POST 資料更新)。
  - **Courts 模塊**：新增 `booking_form` (用於在詳情 Modal 中非同步載入預訂表單)、`check_availability` (即時驗證日期是否已被預訂) 以及 `create_booking` (處理預訂請求並回傳成功/失敗提示)。

### 4. 修復體驗問題與新增進階功能 (Bug Fixes & Enhancements)
* **修復 Modal 無法開啟的問題**：移除了原先片段中不穩定的 `hx-on::after-swap="showModal()"`，改為使用原生的 Bootstrap 屬性 (`data-bs-toggle="modal" data-bs-target="..."`)。這可確保每次點擊時 Modal 必定彈出，並完美與 HTMX 的非同步內容載入結合。
* **修復未定義之 JavaScript 錯誤**：將 `booking_form.html` 中因找不到 `showSuccessNotification` 而導致的錯誤，暫時更換為原生的 `alert('預訂成功！')` 與 `window.location.reload()` 來確保操作回饋正常運作。
* ✨ **新增：我的預約清單即時取消 (動態動畫)**：在 `my_bookings.html` 中實作了 `hx-delete` 與 `hx-target="closest li"`。點擊取消預訂時，會發送刪除請求到後端，並且搭配 `hx-swap="outerHTML swap:0.5s"` 以及自訂 CSS 類別 `.htmx-swapping`，實現預約項目淡出並向右滑動消失的華麗過場效果。
* ✨ **新增：會員編輯成功後自動關閉 Modal**：在 `member_edit_form.html` 中加入了 `hx-on::after-request`，當表單送出且後端回傳 200 成功狀態時，自動呼叫 Bootstrap 的 JavaScript API 來把 Modal 關閉，同時主列表中的會員資料已經被 HTMX 完美替換，達成極致的順暢體驗！
