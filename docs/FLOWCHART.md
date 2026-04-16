# 流程圖設計 (Flowchart) - 食譜收藏夾系統

本文件基於 `docs/PRD.md` 需求與 `docs/ARCHITECTURE.md` 系統架構，繪製食譜收藏夾系統的使用者流程圖與系統序列圖。

## 1. 使用者流程圖 (User Flow)

描述使用者進入系統後，可以進行的各項主要操作路徑。

```mermaid
flowchart LR
    A([使用者開啟網站]) --> B[首頁 - 食譜總覽]
    
    B --> C{選擇操作}
    
    %% 瀏覽與搜尋流程
    C -->|搜尋或點擊分類/標籤| D[篩選後的食譜清單]
    D --> E[點擊任一食譜]
    E --> F[食譜詳細閱讀頁]
    
    %% 新增流程
    C -->|點擊「新增食譜」| G[填寫新增表單]
    G --> H{資料驗證}
    H -->|不完整或錯誤| G
    H -->|成功| I[儲存並導向該篇食譜頁]
    
    %% 編輯與刪除流程
    F --> J{食譜管理操作}
    J -->|點擊「編輯」| K[修改食譜資料表單]
    K --> L[儲存變更並更新食譜頁]
    J -->|點擊「刪除」| M{確認刪除？}
    M -->|是| N[刪除資料並導回首頁]
    M -->|否| F
```

## 2. 系統序列圖 (Sequence Diagram)

以「新增一筆食譜」為例，展示前端瀏覽器、後端介接 (Flask Controller) 以及資料庫間的互動與資料流動。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML 介面)
    participant Flask as Flask Route (Controller)
    participant Model as SQLAlchemy (Model)
    participant DB as SQLite (Database)

    User->>Browser: 點擊「新增食譜」，進入表單頁面
    Browser->>Flask: GET /recipe/new
    Flask-->>Browser: 回傳 Jinja2 渲染的 form.html (空白表單)
    
    User->>Browser: 填寫名稱、食材、步驟後，點選「儲存」
    Browser->>Flask: POST /recipe/new (攜帶表單資料 Form Data)
    
    Flask->>Flask: 後端驗證必填欄位
    alt 驗證失敗 (例如未填寫標題)
        Flask-->>Browser: 重新回傳 form.html 加上錯誤訊息
    else 驗證成功
        Flask->>Model: 建立 Recipe 物件
        Model->>DB: 執行 INSERT 語法
        DB-->>Model: 儲存成功，獲得新 ID
        Model-->>Flask: 完成新增
        Flask-->>Browser: HTTP 302 重導向至該食譜頁 (/recipe/{id})
        Browser->>Flask: GET /recipe/{id}
        Flask-->>Browser: 回傳詳細頁面 detail.html
    end
```

## 3. 功能清單對照表

彙集上述流程中，後端 API 路由與各個功能對應的 HTTP 方法。

| 模組 | HTTP 方法 | URL 路徑 | 功能說明 |
| :--- | :--- | :--- | :--- |
| **主畫面** | GET | `/` | 進入系統首頁，顯示全部食譜清單與分類快篩 |
| **瀏覽與搜尋** | GET | `/search` | 根據條件（關鍵字、標籤、時間）回傳篩選結果 |
| **食譜檢視** | GET | `/recipe/<int:id>` | 呈現單一食譜的詳細圖文、食材及步驟 |
| **新增食譜** | GET | `/recipe/new` | 回傳新增食譜用的空白表單頁面 |
| **新增食譜** | POST | `/recipe/new` | 接收表單並將新食譜寫入資料庫 |
| **編輯食譜** | GET | `/recipe/<int:id>/edit` | 回傳帶有舊有資料的編輯表單頁面 |
| **編輯食譜** | POST | `/recipe/<int:id>/edit` | 接收編輯後的表單並覆蓋資料庫原有紀錄 |
| **刪除食譜** | POST | `/recipe/<int:id>/delete`| 將特定 ID 的食譜從資料庫移除，後重導至首頁 |
