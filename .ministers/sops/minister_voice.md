# Voice 部長 SOP

> 職責：監聽新錄音 → Whisper 轉錄 → 寫入 voice-inbox → push 到 GitHub
> Cadence：每個 cycle 必跑（min_cadence_hours: 0）
> 這是 Asher 錄音到出現在 AlchPlan 頁面的唯一管道。

---

## Prepend

執行前必讀 `alchplan_charter.md` 全文。

---

## 輸入

- iCloud 來源：`C:\Users\ashershih\iCloudDrive\iCloud~com~openplanetsoftware~just-press-record\`
- 既有 voice-inbox：`bujo/voice-inbox/` (alchplan-data repo)
- State file：`.ministers/state/voice.json`

## 輸出

- 新的 `bujo/voice-inbox/YYYY-MM-DD - <title> (HHMMSS).md` 檔案
- 更新後的 `voice.json` state
- Newsletter：`.ministers/newsletters/voice_<circle_id>.md`

---

## 執行步驟（順序不可調）

### Step 1: 環境檢查
- 確認 iCloud 目錄存在且可讀
- 確認 Whisper 可用（Windows Python + CUDA）
- 確認 alchplan-data repo clean（沒有未 commit 的衝突）

### Step 2: 載入 State
讀取 `.ministers/state/voice.json`：
```json
{
  "last_scan_date": "2026-05-10",
  "last_circle_id": "20260510_C001",
  "processed_files": ["2026-05-03/16-04-04.m4a", ...],
  "failed_files": [],
  "total_transcribed": 549,
  "errors_this_cycle": []
}
```

### Step 3: 掃描新檔案
- 遍歷 iCloud 目錄所有日期資料夾
- 比對 `processed_files` 清單，找出未處理的 .m4a/.wav/.mp3
- **最新的先處理**（reverse chronological）

### Step 4: 轉錄
對每個新檔案：
1. 呼叫 Windows Python 的 Whisper large-v3（CUDA）
2. 取得轉錄文字
3. 產生 markdown 檔案，格式：
```markdown
---
date: YYYY-MM-DD
source: Just Press Record
original_file: HH-MM-SS.m4a
type: voice-transcript
---

# 🎙️ 語音轉錄: <前40字>

> 轉錄日期: YYYY-MM-DD HH:MM:SS

## 轉錄內容
<完整轉錄文字>

---
#voice-inbox #justpressrecord
```
4. 寫入 `bujo/voice-inbox/`
5. 加入 `processed_files`
6. 失敗的加入 `failed_files` + `errors_this_cycle`

### Step 5: 持久化（在 newsletter 之前！）
- 寫入 `voice.json` state
- `git add bujo/voice-inbox/ .ministers/state/voice.json`
- `git commit -m "voice: 轉錄 N 則新錄音 (circle <id>)"`
- `git push origin main`

### Step 6: 寫 Newsletter
`.ministers/newsletters/voice_<circle_id>.md`：
```markdown
# Voice 部長 Newsletter — <circle_id>

## TL;DR
本次轉錄 X 則新錄音（Y 則失敗）。最新錄音日期：YYYY-MM-DD。

## 今日動作
- 掃描 iCloud：發現 X 則新錄音
- 成功轉錄：X 則（共 NNNN 字）
- 失敗：Y 則（原因：...）

## 幫 Asher 做了什麼
- N 則新語音已出現在 AlchPlan 語音收件箱
- 可在 BuJo tab 勾選並整合到日記

## 需要 Asher 回應
（通常無，除非有持續失敗的檔案需要 Asher 確認是否要刪除）

## 下個 Cycle 計畫
- 繼續監聽新錄音
- 如有 failed_files 積壓超過 3 個 cycle，提交 PM inbox 問題
```

### Step 7: 檢查 Inbox
- 讀取 PM inbox 中 `minister: "voice"` 的待處理問題
- 如有 Asher 回應，執行對應動作
- 標記已消費的問題

---

## 異常處理

| 狀況 | 動作 |
|------|------|
| iCloud 目錄不存在 | newsletter 寫「iCloud 未掛載」，提交 PM inbox 問題 |
| Whisper 載入失敗 | newsletter 寫錯誤，提交 PM inbox 問題（type: open） |
| 單檔轉錄失敗 | 加入 failed_files，繼續處理下一個，不中斷 |
| git push 衝突 | pull --rebase 後重試一次，仍失敗則 newsletter 報告 |
| 0 則新錄音 | 正常，newsletter 寫「無新錄音」即可 |

---

## 不可做的事

- 不可刪除任何 voice-inbox 檔案（章程鐵律 5）
- 不可修改已存在的轉錄內容
- 不可跳過失敗檔案不記錄
- 不可在 Step 5 之前寫 newsletter（防 max-turns 截斷丟失資料）
