# 路由設計 (Routes Design) - 食譜收藏夾系統

本文件基於 `docs/PRD.md` 的功能規劃與 `docs/DB_DESIGN.md` 的資料庫設計，擬定了本系統的 URL 路由結構、對應的處理邏輯與 Jinja2 網頁模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :-- | :-- | :-- | :-- | :-- |
| **首頁/食譜清單** | GET | `/` | `templates/index.html` | 顯示預設的食譜列表以及分類導覽 |
| **搜尋與篩選** | GET | `/recipes/search` | `templates/index.html` | 接收 query string 後篩選資料庫並呈現在清單頁 |
| **新增食譜頁面** | GET | `/recipes/new` | `templates/form.html` | 回傳新增食譜之空白表單 |
| **建立食譜** | POST | `/recipes/new` | — | 接收並驗證表單寫入資料庫，完成後重導向至該食譜 |
| **食譜詳細展示** | GET | `/recipes/<int:recipe_id>` | `templates/detail.html` | 取得單一食譜的詳細食材與步驟內容並顯示 |
| **編輯食譜頁面** | GET | `/recipes/<int:recipe_id>/edit`| `templates/form.html` | 回傳帶入預設舊資料的表單 |
| **更新食譜** | POST | `/recipes/<int:recipe_id>/edit`| — | 接收表單更新，存入資料庫後重導向至詳細頁 |
| **刪除食譜** | POST | `/recipes/<int:recipe_id>/delete`| — | （透過表單觸發）刪除資料後回到首頁，無須渲染模板 |

## 2. 每個路由的詳細說明

### 2.1 首頁與食譜清單 (`GET /`)
- **輸入**：無
- **處理邏輯**：呼叫 `Recipe.get_all()` 取得所有食譜，同時取得所有 `Category` 供版面側邊欄或頂部過濾使用。
- **輸出**：渲染 `index.html`。
- **錯誤處理**：如果資料庫完全沒資料，畫面提示「目前尚無食譜，趕快新增第一篇吧！」。

### 2.2 搜尋與篩選 (`GET /recipes/search`)
- **輸入**：URL 參數 `?q=關鍵字&category_id=類別ID`。
- **處理邏輯**：組裝 SQLAlchemy 條件查詢。可以根據關鍵字過濾 `title`，如果帶有類別參數就繼續過濾。
- **輸出**：渲染 `index.html`，並將原先輸入的關鍵字帶回表單。

### 2.3 新增食譜頁面 (`GET /recipes/new`)
- **輸入**：無
- **處理邏輯**：從資料庫取得所有分類（Categories）以及所有的標籤（Tags），提供給渲染時的 `<select>` 或 checkbox 組合。
- **輸出**：渲染 `form.html`。

### 2.4 建立食譜 (`POST /recipes/new`)
- **輸入**：包含 `title`, `ingredients`, `steps`, `cooking_time` 等等之 Form Data 表單格式。
- **處理邏輯**：
  1. 檢查必填參數是否有遺漏。
  2. 把資料拆解，如有 tag_id 需關聯出對應 Tag 物件。
  3. 執行 `Recipe.create()` 。
- **輸出**：成功後呼叫 `redirect()` 重新導向至 `/recipes/<new_id>`。
- **錯誤處理**：如果有欄位空白，透過 `flask.flash()` 傳遞錯誤訊息，並立刻重新回傳渲染包含已填寫欄位的 `form.html`。

### 2.5 食譜詳細展示 (`GET /recipes/<int:recipe_id>`)
- **輸入**：網址路徑變數 `recipe_id`。
- **處理邏輯**：呼叫 `Recipe.get_by_id(recipe_id)`。
- **輸出**：渲染 `detail.html`。
- **錯誤處理**：如果這個 ID 不存在，回傳 `abort(404)` 的 HTTP 狀態。

### 2.6 編輯食譜頁面 (`GET /recipes/<int:recipe_id>/edit`)
- **輸入**：網址路徑變數 `recipe_id`。
- **處理邏輯**：獲取目標食譜的所有屬性（及其附帶之標籤），一併傳遞給頁面。
- **輸出**：渲染 `form.html`，並且模板內部透過判斷使介面呈現「儲存變更」的樣態。
- **錯誤處理**：跟隨 HTTP 404 機制處理。

### 2.7 更新食譜 (`POST /recipes/<int:recipe_id>/edit`)
- **輸入**：網址路徑變數與更新後的 Form Data。
- **處理邏輯**：檢查參數與驗證後，執行該物件的 `.update()` 覆蓋舊資料。
- **輸出**：`redirect` 回該篇修改好的食譜詳細頁 `GET /recipes/<int:recipe_id>`。

### 2.8 刪除食譜 (`POST /recipes/<int:recipe_id>/delete`)
- **輸入**：網址路徑變數 `recipe_id`。
- **處理邏輯**：呼叫 `Recipe.delete()` 解除關聯並移除資料列。
- **輸出**：完成後重新導向至首頁 `/` 。

## 3. Jinja2 模板清單

預計在 `app/templates/` 建立的 HTML 模板檔案如下：

1. **`base.html`**
   - 用途：為其餘所有的父親版型。包含 HTML 的 Header、專案整體色調 CSS 引入與一致的導覽列（Navbar）。
2. **`index.html`**
   - 用途：食譜首頁。顯示格狀或列表狀的食譜縮圖卡片（繼承自 `base.html`）。
3. **`detail.html`**
   - 用途：單篇食譜的深度閱讀區（繼承自 `base.html`）。包含了「編輯」與「刪除」的捷徑按鈕。
4. **`form.html`**
   - 用途：新增食譜與編輯食譜高度重合，考量到可維護性以此共同表單實作（繼承自 `base.html`）。包含所有的 `<input>` 與 `<textarea>`。

## 4. 路由骨架程式碼
API 控制器分成兩塊已在開發階段先行建立空架構，分別為：
- `app/routes/main.py` 用於處理首頁共用資源。
- `app/routes/recipe.py` 用於專門處理食譜的增刪改查邏輯。
