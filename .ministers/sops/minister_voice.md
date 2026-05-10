# Voice 部長 SOP

> 職責：監聽新錄音 → Whisper 轉錄 → 寫入 voice-inbox → push 到 GitHub
> Cadence：每個 cycle 必跑（min_cadence_hours: 0）
> 這是 Asher 錄音到出現在 AlchPlan 頁面的唯一管道。

---

## Prepend

執行前必讀 `alchplan_charter.md` 全文。

---

## 執行步驟（順序不可調，共 4 步，設計為 max-turns 友好）

### Step 1: 執行轉錄腳本

跑以下指令（必須用 Windows Python，因為 Whisper + CUDA）：

```bash
powershell.exe -Command "python 'C:\Users\ashershih\Documents\alchplan-data\.ministers\scripts\voice_transcribe.py'" 2>/dev/null
```

腳本會：
- 掃描 iCloud Just Press Record 資料夾
- 用 Whisper large-v3 (CUDA) 轉錄所有新錄音
- 寫入 markdown 到 `bujo/voice-inbox/`
- 更新 `.ministers/state/voice.json`
- 在 **stdout** 輸出 JSON 結果

讀取 stdout 的 JSON 結果，格式：
```json
{
  "scan_date": "2026-05-10",
  "new_found": 3,
  "transcribed": ["2026-05-10/14-30-00.m4a", ...],
  "failed": [{"file": "...", "error": "..."}],
  "total_chars": 1234
}
```

如果指令失敗或 timeout，在 newsletter 記錄錯誤，提交 PM inbox 問題。

### Step 2: Git 持久化（在 newsletter 之前！）

```bash
cd /mnt/c/Users/ashershih/Documents/alchplan-data
git add bujo/voice-inbox/ .ministers/state/voice.json
git commit -m "voice: 轉錄 N 則新錄音 (circle <id>)"
git pull --rebase origin main
git push origin main
```

如果 push 失敗，嘗試一次 pull --rebase 後重推。仍失敗則 newsletter 報告。

### Step 3: 更新 State（補充 circle_id）

讀取 `.ministers/state/voice.json`，更新 `last_circle_id` 為本次 circle ID，寫回。

### Step 4: 寫 Newsletter

寫入 `.ministers/newsletters/voice_<circle_id>.md`：

```markdown
# Voice 部長 Newsletter — <circle_id>

## TL;DR
本次轉錄 X 則新錄音（Y 則失敗）。

## 幫 Asher 做了什麼
- X 則新語音已出現在 AlchPlan 語音收件箱
- 總計 NNNN 字
- 最新錄音日期：YYYY-MM-DD

## 失敗項目
（如有）

## 需要 Asher 回應
（通常無）

## 下個 Cycle 計畫
- 繼續監聽新錄音
```

---

## 異常處理

| 狀況 | 動作 |
|------|------|
| 轉錄腳本 timeout | newsletter 報告，提交 PM inbox |
| 0 則新錄音 | 正常，newsletter 寫「無新錄音」 |
| git push 衝突 | pull --rebase 重試一次 |
| Whisper 載入失敗 | newsletter 報告錯誤 |

## 不可做的事

- 不可刪除任何 voice-inbox 檔案（章程鐵律 5）
- 不可修改已存在的轉錄內容
- 不可在 Step 2 之前寫 newsletter（防 max-turns 截斷丟失資料）
