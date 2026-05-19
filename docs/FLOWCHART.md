# 流程圖設計 (FLOWCHART)

**專案名稱：** 糞便日誌 (Poop Journal)
**建立日期：** 2026-05-19

---

## 1. 使用者流程圖 (User Flow)

這張圖描述了使用者從進入網站開始，在系統中可能進行的各種操作路徑，包含新增紀錄、查看歷史以及獲取飲食建議。

```mermaid
flowchart LR
    A([使用者進入網站]) --> B[首頁 / Dashboard]
    
    B --> C{選擇操作}
    
    C -->|新增記錄| D[填寫排便日誌表單]
    D -->|填寫形狀/顏色/心情等| E[送出表單]
    E --> F[檢視 AI 分析與健康說明]
    F --> G([返回首頁或列表])
    
    C -->|檢視歷史| H[瀏覽歷史記錄列表]
    H -->|篩選日期| H
    H -->|點擊單筆記錄| I[檢視詳細資訊]
    I -->|編輯記錄| J[修改並儲存]
    I -->|刪除記錄| K[確認並刪除]
    J --> H
    K --> H
    
    C -->|查看飲食建議| L[瀏覽個人化飲食建議]
    L --> G
```

## 2. 系統序列圖 (Sequence Diagram)

這張圖詳細描述了「使用者填寫新增表單並送出」到「資料存入資料庫並顯示分析結果」的完整系統互動過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route<br/>(logs.py / analysis.py)
    participant Model as SQLAlchemy ORM
    participant DB as SQLite
    participant Service as Service Layer<br/>(bristol.py)

    User->>Browser: 填寫排便記錄並點擊送出
    Browser->>Route: POST /logs/new
    Route->>Model: 建立排便記錄 (PoopLog) 物件
    Model->>DB: INSERT INTO logs
    DB-->>Model: 儲存成功，回傳紀錄 ID
    Route-->>Browser: HTTP 302 Redirect 重導向至分析結果頁
    
    Browser->>Route: GET /analysis/<log_id>
    Route->>Model: 透過 ID 查詢該筆記錄
    Model->>DB: SELECT * FROM logs WHERE id = <log_id>
    DB-->>Model: 回傳記錄資料
    Route->>Service: 呼叫布里斯托分析邏輯 (analyze)
    Service-->>Route: 回傳健康狀態與說明結果
    Route->>Browser: 渲染並回傳 HTML (result.html)
    Browser-->>User: 顯示 AI 分析結果卡片
```

## 3. 功能清單對照表

根據 PRD 與系統架構，規劃出對應的 URL 路徑與 HTTP 方法，為後續的 API 設計與實作打下基礎。

| 功能 | 說明 | URL 路徑 | HTTP 方法 | 對應 Blueprint |
|---|---|---|---|---|
| **首頁 / Dashboard** | 進入系統的第一頁，顯示簡單摘要與操作入口 | `/` | GET | `main` |
| **填寫記錄表單** | 顯示新增排便記錄的表單頁面 | `/logs/new` | GET | `logs` |
| **新增記錄** | 接收表單提交的資料並存入資料庫 | `/logs/new` | POST | `logs` |
| **歷史記錄列表** | 列出所有的排便記錄，支援日期篩選功能 | `/logs` | GET | `logs` |
| **記錄詳細頁** | 查看單筆排便記錄的詳細資料與心情 | `/logs/<id>` | GET | `logs` |
| **編輯記錄表單** | 顯示編輯特定記錄的頁面 | `/logs/<id>/edit` | GET | `logs` |
| **更新記錄** | 接收編輯後的資料並更新資料庫 | `/logs/<id>/edit` | POST | `logs` |
| **刪除記錄** | 刪除特定的排便記錄 | `/logs/<id>/delete` | POST | `logs` |
| **AI 分析結果** | 根據記錄 ID 顯示當次糞便的健康分析與說明 | `/analysis/<id>` | GET | `analysis` |
| **飲食建議** | 根據近期歷史紀錄提供綜合的飲食調整建議 | `/analysis/suggestion` | GET | `analysis` |

---
*本文件由 Antigravity AI 根據 PRD 與 ARCHITECTURE 產生，供團隊確認整體流程與頁面規劃。*
