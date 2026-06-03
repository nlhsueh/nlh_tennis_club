## Django MVT 基礎課堂隨堂測驗 — HTMX 局部刷新與非同步互動 (Quiz)

本測驗旨在檢驗學生對於本單元（`htmx` 分支：HTMX 屬性應用、局部片段（Fragment）渲染、AJAX 請求標頭偵測、與 Bootstrap Modal 的聯動、以及 CSS 動態淡出動畫）核心概念的理解。

---

## 📝 一、單選題 (Multiple Choice Questions)

### 1. 在 Django 視圖（Views）中，我們該如何偵測當前請求是否是由 HTMX 所發送的非同步 AJAX 請求，進而決定是要返回「局部 HTML 片段」還是「完整 HTML 頁面」？
* (A) `if request.is_ajax():`
* (B) `if request.headers.get('HX-Request'):`
* (C) `if request.GET.get('htmx') == 'true':`
* (D) `if request.META.get('HTTP_HTMX_RESPONSE'):`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* 當 HTMX 發送非同步 AJAX 請求時，會在 HTTP 請求標頭中自動附帶一個 `HX-Request: true` 的標頭。
* 在 Django（以 3.x/4.x 版本為例）中，我們可以透過 **`request.headers.get('HX-Request')`** 來檢查該標頭是否存在，從而精準判定是否需要回傳局部片段（如 `fragments/member_list.html`），以實現不重整頁面的局部更新。
</details>

---

### 2. 當我們在設計「實時搜尋框」時，使用 `<input hx-trigger="input changed delay:500ms" ...>` 的主要目的是什麼？
* (A) 讓使用者輸入字元後，強行延遲 500 毫秒才將文字顯示在網頁上。
* (B) 設定防震（Debounce）機制，避免使用者每敲擊一次鍵盤就立刻對伺服器發送一次請求，降低伺服器負載。
* (C) 為了配合 CSS 動畫的淡入速度。
* (D) 設定網路超時（Timeout）限制，若伺服器 500 毫秒內未回應則放棄連線。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* `hx-trigger="input changed delay:500ms"` 代表：當輸入框的值發生改變時，必須在使用者「停止輸入滿 500 毫秒後」才真正發送 AJAX 請求。
* 這在實時搜尋中非常重要，可以防止使用者快速輸入單字時（例如輸入 "apple" 產生 5 次按鍵事件），向伺服器連續發送 5 次不必要的查詢請求，達到極佳的流量防呆與優化。
</details>

---

### 3. 關於 HTMX 的置換屬性 `hx-swap`，當設定為 `hx-swap="outerHTML"` 與預設的 `hx-swap="innerHTML"`，兩者在 DOM 替換時的根本差異是什麼？
* (A) `innerHTML` 會替換目標元素內部的子元素，但保留目標元素本身；`outerHTML` 則會連同目標元素本身一起被新回傳的 HTML 替換掉。
* (B) `innerHTML` 只能替換文字；`outerHTML` 可以替換圖片與多媒體。
* (C) `outerHTML` 會開啟新的瀏覽器視窗；`innerHTML` 則在當前分頁替換。
* (D) 兩者完全沒有差別，只是名稱不同。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(A)**

**解析**：
* 這是 HTMX 中控制 DOM 置換的關鍵：
  - **`innerHTML`（預設）**：僅替換目標容器「裡面」的內容。
  - **`outerHTML`**：將整個目標容器（包含其本身的 `<div>` 或 `<li>` 標籤）全部替換為新回傳的 HTML 片段。在本單元的內聯編輯表單儲存後，我們希望將 `<form>` 整體替換回原來的 `<li>` 項目，此時就必須使用 `outerHTML`。
</details>

---

### 4. 當我們在取消預訂（Delete）時，設定了 `hx-swap="outerHTML swap:0.5s"`，這在 CSS 動態過場動畫中扮演了什麼角色？
* (A) 限制刪除請求在 0.5 秒內必須完成，否則自動取消。
* (B) 告訴 HTMX 在接收到響應後，延遲 0.5 秒再執行刪除動作；在這 0.5 秒內，該元素會被自動套用 `.htmx-swapping` CSS 類別，讓我們可以撰寫淡出（Fade-out）與滑動動畫。
* (C) 讓伺服器強制休眠 0.5 秒。
* (D) 為了防止網路延遲而設定的快取時間。

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* `swap:0.5s` 會延長 HTMX 執行置換與移除的生命週期。
* 在這指定的 0.5 秒緩衝期內，該被刪除的元件會被自動加上 **`.htmx-swapping`** class。我們可以利用 CSS Transition（如 `opacity: 0; transform: translateX(50px); transition: all 0.5s;`）讓該項目在畫面上優雅地滑動並淡出，時間結束後 HTMX 才會真正將它從 DOM 中移除，使互動極具流暢感。
</details>

---

### 5. 在本單元中，當我們編輯會員並點選儲存後，表單成功送出並希望「自動關閉 Bootstrap Modal 彈出視窗」，我們是使用哪一個 HTMX 屬性來監聽請求結束，並呼叫 Bootstrap JS API 的？
* (A) `hx-trigger="click"`
* (B) `hx-on::after-request="bootstrap.Modal.getInstance(document.getElementById('memberModal')).hide()"`
* (C) `hx-target="#memberModal"`
* (D) `hx-close="modal"`

<details>
<summary>🔑 點擊查看答案與解析</summary>

**正確答案**：**(B)**

**解析**：
* **`hx-on::after-request`** 允許我們在 HTMX AJAX 請求完成並處理完畢後，直接在 HTML 屬性中執行 inline 的 JavaScript 腳本。
* 本單元藉由該事件，於後端回傳 200 成功後，呼叫 `bootstrap.Modal.getInstance(...).hide()`，實現表單儲存後，主列表局部更新、且模態視窗自動隱藏的完美閉環體驗。
</details>

---

## 💬 二、簡答題 (Short Answer Questions)

### 6. 請簡述傳統「單頁面應用 (SPA，如 React / Vue)」與使用「HTMX」在實現「無刷新網頁互動」時的架構差異。為什麼 HTMX 被稱為「回歸 HTML 本質」的超輕量替代方案？

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **SPA 架構（React/Vue）**：
   - 前後端完全分離。後端只負責提供 JSON API，前端必須撰寫大量的 JavaScript 來進行路由管理、狀態管理（Redux/Pinia），並在瀏覽器端把 JSON 解析並動態渲染成 HTML。這導致專案架構變複雜，開發與維護成本高。
2. **HTMX 架構**：
   - 依然保持 Django 的伺服器端渲染（SSR）優勢。HTMX 讓 HTML 元素可以直接發送 AJAX 請求，且伺服器直接回傳「局部 HTML 片段」（而不是 JSON）。HTMX 在前端只做一件事：用回傳的 HTML 替換掉指定的 DOM 元素。
3. **回歸本質的原因**：
   - HTMX 不需要編寫複雜的前端 JS 框架與打包工具，只用 HTML 自訂屬性即可達成 AJAX。所有的資料驗證、商務邏輯與 HTML 渲染依然完整保留在 Django 的後端 Python 中，簡化了架構，對中小型專案與教學而言更易於開發。
</details>

---

### 7. 在實作「取消預訂」功能時，我們在 `my_bookings.html` 中撰寫了如下的程式碼。請解釋這三個 HTMX 屬性的用途，並說明它們是如何協同完成「無刷新淡出刪除項目」的？
```html
<li hx-delete="{% url 'cancel_booking' x.id %}"
    hx-target="this"
    hx-swap="outerHTML swap:0.5s">
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**參考解答**：
1. **屬性用途**：
   - `hx-delete`：當用戶點擊（或觸發）該 `<li>` 內的刪除按鈕時，向後端發送 HTTP `DELETE` 請求。
   - `hx-target="this"`：指定 AJAX 響應的回傳內容要置換的目標是「此元素本身」（即當前的整個 `<li>` 項目）。
   - `hx-swap="outerHTML swap:0.5s"`：採用 `outerHTML` 置換（將整個 `<li>` 移除），並將置換與移除動作延遲 0.5 秒執行。
2. **協同運作流程**：
   - 當後端確認刪除並回傳空響應（200 OK）時，HTMX 會先在該 `<li>` 元素上自動加上 `.htmx-swapping` 的 CSS 類別，並開啟 0.5 秒的計時器。
   - CSS 中針對 `.htmx-swapping` 撰寫了過渡效果（例如將不透明度 `opacity` 設為 0，且向右位移），元素便會在畫面上呈現 0.5 秒的滑動淡出動畫。
   - 0.5 秒時間一到，HTMX 正式將該 `<li>` 從 DOM 樹中徹底移除，完美實現了無重新整理的流暢淡出刪除體驗。
</details>

---

## 💻 三、程式碼填充題 (Fill in the Blank Questions)

### 8. 以下是 `members/views.py` 中處理成員列表的視圖。我們希望它能兼容傳統的全頁載入與 HTMX 的局部過濾。請填入正確的 Django 屬性與 HTTP 標頭檢查名稱：
```python
# members/views.py
from django.shortcuts import render
from .models import Member

def members(request):
    mymembers = Member.objects.all()
    
    # 處理前端 HTMX 傳來的即時搜尋參數
    search_query = request.GET.get('search', '')
    if search_query:
        mymembers = mymembers.filter(firstname__icontains=search_query)
        
    # 1. 檢查當前請求標頭（Headers）中是否包含 HTMX 的標記
    if request.___(1)___.get('___(2)___'):
        # 2. 如果是 HTMX 請求，只渲染並返回成員列表的「局部 HTML 片段」
        return render(request, 'fragments/member_list.html', {'mymembers': mymembers})
        
    # 3. 如果是普通瀏覽器訪問，則返回包含完整外殼的頁面
    return render(request, 'all_members.html', {'mymembers': mymembers})
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `headers`
* `(2)`: `HX-Request`
</details>

---

### 9. 我們想在網頁表單中，利用 HTMX 來完成內聯編輯（Inline Edit）的提交與自動 Modal 關閉。請填寫對應的 HTMX 屬性名稱以完成此功能：
```html
<!-- members/templates/fragments/member_edit_form.html -->

<!-- 1. 當表單送出時，以 POST 方式非同步發送資料到更新路由 -->
<form ___(1)___="{% url 'update_member' member.id %}"
      # 2. 指定更新的目標是包裹該成員的整列項目本身
      ___(2)___="#member-{{ member.id }}"
      # 3. 設定置換模式為外殼替換 (連同 form 標籤本身一起換掉)
      ___(3)___="outerHTML"
      # 4. 當請求結束且狀態碼為 200 時，利用 inline JS 呼叫 API 關閉 Modal 彈出視窗
      ___(4)___="if(event.detail.xhr.status === 200) { bootstrap.Modal.getInstance(document.getElementById('memberModal')).hide(); }">
  
  {% csrf_token %}
  <input type="text" name="firstname" value="{{ member.firstname }}" required>
  <input type="text" name="lastname" value="{{ member.lastname }}" required>
  <button type="submit">儲存</button>
</form>
```

<details>
<summary>🔑 點擊查看答案與解析</summary>

**填空答案**：
* `(1)`: `hx-post`
* `(2)`: `hx-target`
* `(3)`: `hx-swap`
* `(4)`: `hx-on::after-request`
</details>
