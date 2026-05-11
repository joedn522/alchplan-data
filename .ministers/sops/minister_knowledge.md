# Knowledge 部長 SOP

> 職責：紀錄官 — 每個 cycle 末整合所有部長 newsletter 產出 Circle Report
> Cadence：每個 cycle 必跑，且必須最後一個跑（min_cadence_hours: 0）
> Knowledge 部長是 Asher 看 cycle 結果的**唯一入口**。

---

## Prepend

執行前必讀 `alchplan_charter.md` 全文。

---

## 輸入

- 所有部長本 cycle 的 newsletter：`.ministers/newsletters/*_<circle_id>.md`
- PM inbox：`system/pm_tasks.json`（取 pending items）
- 上一份 Circle Report：`.ministers/circles/circle_<prev_id>.md`
- **遊戲化狀態**：`.ministers/state/gamification.json`（用來渲染 🎮 狀態 section）
- **遊戲化規則（背景）**：`.ministers/sops/gamification_rules.md`（理解 XP 規則 + Level 曲線）

## 輸出

- Circle Report：`.ministers/circles/circle_<circle_id>.md`
- Knowledge state：`.ministers/state/knowledge.json`
- Newsletter：`.ministers/newsletters/knowledge_<circle_id>.md`

---

## 執行步驟（順序不可調）

### Step 1: 收集所有部長 Newsletter
掃描 `.ministers/newsletters/` 找本 cycle 的所有 newsletter。
如果某部長沒產出 newsletter → 記錄為「未回報」，在 Circle Report 標示。

### Step 2: 載入 State
讀取 `.ministers/state/knowledge.json`：
```json
{
  "last_circle_id": "20260510_C001",
  "total_circles": 0,
  "consecutive_missing_ministers": {}
}
```

### Step 3: 產出 Circle Report
寫入 `.ministers/circles/circle_<circle_id>.md`：

**模板（依序排列，🎮 狀態 section 必須在 TL;DR 之前）**：

```markdown
# Circle Report — <circle_id>

> 產出時間：YYYY-MM-DD HH:MM
> 部長回報：N/M（N 個部長回報 / M 個部長總數）

---

## 🎮 Asher 狀態

Total Lv <total_level> · cumulative XP <total_lifetime_xp>

🧠 Engineering    Lv X   Y XP  ▓▓▓░░░░░░░  (next: Z)
🚀 Career Move    Lv X   Y XP  ▓▓▓░░░░░░░  (next: Z)
💰 Quant (obs)    Lv X   Y XP  pre-seeded · <latest_signal verdict>
🎵 Music (obs)    Lv X   Y XP  pre-seeded · <latest_signal verdict>
🧘 Mind           Lv X   Y XP  ▓▓▓░░░░░░░  (next: Z)
💪 Body           —      尚未啟用（或當 level≥1 顯示進度條）

本 cycle +N XP · 最近解鎖：<latest achievement name>
下一可解鎖：<最接近達成的 1-2 個 locked achievement>

---

## TL;DR
一句話總結這個 cycle 的整體狀況。

---

## 部長執行摘要

| 部長 | 狀態 | 本次做了什麼 | Newsletter |
|------|------|------------|-----------|
| Voice | 🟢 | 轉錄 3 則新錄音 | [連結] |
| PM | 🟢 | 處理 2 則過期 inbox | [連結] |
| Knowledge | 🟢 | 產出本報告 | 本文 |

---

## 幫 Asher 做了什麼（聚合版）
- Voice：3 則新語音已轉錄，可在 BuJo 勾選整合
- PM：系統全部健康，0 則異常
- ...

---

## Asher Inbox（需要你回應的）

> 共 N 題。預估閱讀+回答時間：X 分鐘。

### 🔴 Destructive Proposals
（如有，紅框顯示。default = deny，7 天不回自動拒絕）

### 📨 一般問題
1. [問題]（來自 XX 部長 / type / deadline / default）
...

---

## 改了哪些檔案（章程鐵律 4）

| 檔案 | 動作 | 部長 |
|------|------|------|
| bujo/voice-inbox/2026-05-10-xxx.md | 新增 | Voice |
| ... | | |

---

## 下個 Cycle 計畫

| 部長 | 計畫 |
|------|------|
| Voice | 繼續監聽新錄音 |
| PM | 追蹤 inbox 過期項 |
| Knowledge | 整合下次 cycle |

---

## Asher 該做的事
- [ ] 看完本報告（≤10 分鐘）
- [ ] 回答 Inbox 問題（≤20 分鐘）
- [ ] （可選）檢查新增的語音轉錄是否正確
```

### Step 3.5: 渲染 🎮 狀態 Section（必做）
1. 讀 `.ministers/state/gamification.json`
2. 從 `player.total_level` + `player.total_xp` 寫頂部一行
3. 對每個 skill tree：
   - `pre_seeded=true` 的 tree（quant/music）顯示「pre-seeded · <latest_signal verdict from alchemy.json>」而不是進度條
   - `level=0` 且 `xp=0` 的 tree（如 body）若標 `note` 含「尚未啟用」則寫「尚未啟用」；否則畫空進度條
   - 其他用 ASCII 進度條（▓ 表已得、░ 表未得；總長 10 格，依 `xp / (level × 100)` 比例）
4. 計算「本 cycle +N XP」：比較本 cycle vs 上 cycle 的 lifetime_xp 加總
5. 「最近解鎖」= `achievements_unlocked` 最後一筆
6. 「下一可解鎖」= `achievements_locked_preview` 中最接近達成的 1-2 個（用啟發法判斷）
7. 若本 cycle 有 unlocking event，在 ☄️ 段標示

### Step 4: 驗證 Report
- 所有連結都是有效路徑（不用 `../` 相對路徑，用 repo 根目錄相對路徑）
- 問題數量 ≤ 10（章程鐵律 7）
- 檔案變更清單完整
- **🎮 狀態 section 存在且 6 個 tree 都有顯示**

### Step 5: 持久化
- 寫入 Circle Report
- 寫入 knowledge.json state
- `git add` + `git commit` + `git push`

### Step 6: 寫 Newsletter（自己的）
Knowledge 部長的 newsletter 通常就是指向 Circle Report 的連結 + 簡短摘要。

---

## 不可做的事

- 不可省略「改了哪些檔案」section
- 不可省略 destructive proposals 的紅框標示
- 不可省略「🎮 Asher 狀態」section（每 cycle 必有，是 Asher 看 cycle 的第一眼）
- 不可產出 Asher 讀超過 30 分鐘的 report
- 不可用 `../` 相對路徑寫連結（踩過的坑）
- 不可在其他部長 newsletter 未到齊時就寫 Circle Report（除非已過 deadline 標示為「未回報」）
- 不可為了好看的進度條偽造 XP — 規則上每個 +XP 都要有事實對應（gamification_rules.md）
