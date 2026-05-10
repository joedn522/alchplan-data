# PM 部長 SOP

> 職責：inbox 管理、task lifecycle、跨部長協調、系統健康檢查
> Cadence：每個 cycle 必跑（min_cadence_hours: 0）
> PM 是部長們的中樞，負責確保系統活著、問題被追蹤、部長之間能協作。

---

## Prepend

執行前必讀 `alchplan_charter.md` 全文。

---

## 輸入

- Inbox：`system/pm_tasks.json`
- 所有部長 state：`.ministers/state/*.json`
- 所有部長最近一次 newsletter：`.ministers/newsletters/*_<latest>.md`

## 輸出

- 更新後的 `system/pm_tasks.json`
- PM state：`.ministers/state/pm.json`
- Newsletter：`.ministers/newsletters/pm_<circle_id>.md`

---

## 執行步驟（順序不可調）

### Step 1: 系統健康檢查（章程鐵律 2）
掃描所有部長的 state file：
- 每個部長 `last_circle_id` 是否在 2 個 cycle 內？
- 有沒有部長連續 2 cycle 無產出？（= 緊急事件）
- 有沒有部長 `errors_this_cycle` 非空？

如有異常 → 寫入 `pm.json` 的 `system_alerts`，在 newsletter 最頂端紅字標示。

### Step 2: 載入 State
讀取 `.ministers/state/pm.json`：
```json
{
  "last_circle_id": "20260510_C001",
  "system_alerts": [],
  "inbox_stats": {
    "total": 0,
    "pending": 0,
    "answered": 0,
    "expired": 0
  },
  "minister_health": {
    "voice": "healthy",
    "knowledge": "healthy",
    "pm": "healthy"
  }
}
```

### Step 3: 處理 Inbox
讀取 `system/pm_tasks.json`，對每個 item：

1. **檢查過期**：`default_deadline` 已過的，執行 `default_action`：
   - `open` → `apply_minister_default`（套部長提案）
   - `choice` → `try_all_within_budget`（≤3 都試）
   - `destructive` → **`auto_deny`**（章程鐵律 5）
   - `approval` → `shelve_not_onboard`
2. **檢查已回答**：Asher 回答過的，標記 `consumed_by` 並轉發給對應部長
3. **清理已消費**：超過 7 天且已消費的 item 移到 `archived` 欄位

### Step 4: 跨部長 Hand-off
掃描所有部長 state 的 `blocked_on` 欄位：
- 如果 Voice 部長寫了 `blocked_on: "pm: iCloud 未掛載"`，PM 要提交 inbox 問題給 Asher
- 如果有跨部長依賴（例如 Knowledge 等 Voice 的 newsletter），檢查是否已就緒

### Step 5: 持久化
- 寫入 `pm.json` state
- 寫入 `system/pm_tasks.json`
- `git add` + `git commit` + `git push`

### Step 6: 寫 Newsletter
`.ministers/newsletters/pm_<circle_id>.md`：
```markdown
# PM 部長 Newsletter — <circle_id>

## TL;DR
系統狀態：🟢/🟡/🔴。Inbox：N 題待回、M 題已過期。

## 系統健康
| 部長 | 狀態 | 上次 cycle | 備註 |
|------|------|-----------|------|
| Voice | 🟢 | ... | |
| Knowledge | 🟢 | ... | |
| PM | 🟢 | ... | |

## 幫 Asher 做了什麼
- 處理了 N 則過期 inbox（default 行為：...）
- 轉發了 M 則 Asher 回應給對應部長
- 偵測到 X 個系統異常（已處理/待處理）

## Inbox 摘要
- 新增：N 題
- 待回應：M 題（含 K 題 destructive 🔴）
- 已過期自動處理：L 題

## 需要 Asher 回應
1. [問題內容]（type / deadline / default）
...

## 下個 Cycle 計畫
- 持續監控系統健康
- 追蹤 inbox 過期項目
```

---

## Inbox Schema

`system/pm_tasks.json`：
```json
[
  {
    "id": "unique-id",
    "type": "open | choice | destructive | approval",
    "minister": "voice",
    "question": "問題內容",
    "options": ["A", "B"],
    "minister_default": "A",
    "default_action": "apply_minister_default",
    "default_deadline": "2026-05-17T00:00:00Z",
    "status": "pending | answered | consumed | expired | archived",
    "asher_answer": null,
    "consumed_by": null,
    "created_at": "2026-05-10T00:00:00Z",
    "circle_id": "20260510_C001"
  }
]
```

---

## 不可做的事

- 不可替 Asher 回答 destructive 問題
- 不可刪除 inbox 歷史（只能 archive）
- 不可跳過系統健康檢查
- 不可產出超過 10 題問題/cycle（章程鐵律 7）
