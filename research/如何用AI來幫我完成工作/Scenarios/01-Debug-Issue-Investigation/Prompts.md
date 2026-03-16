# Prompts — Debug / Issue Investigation

> 用法：把對應區塊複製到你慣用的 AI（OpenClaw / ChatGPT / Gemini / Claude / IDE agent），並把 `{{...}}` 補齊。

## 1) 快速縮小範圍（先問 5 個問題）
**Prompt**
```
你是資深 SRE/後端工程師。請先不要猜結論。

我遇到的問題：
- 現象：{{symptom}}
- 影響範圍：{{impact}}
- 發生時間/版本：{{time_or_version}}
- 最近改動：{{recent_changes}}
- 我目前有的線索：{{clues}}

請你：
1) 先問我最多 5 個「最有信息量」的澄清問題（按優先順序）
2) 給出 3 個最可能根因假說（含支持/反駁證據需要看什麼）
3) 給我下一步排查計畫（每一步預期看到什麼、看到 A/B 各代表什麼）
```

## 2) 解析 stack trace / error log（找出第一個有效訊號）
**Prompt**
```
請分析以下錯誤訊息/stack trace，目標是「找到第一個可行動的線索」。

輸入：
{{paste_logs_or_trace}}

輸出請包含：
- TL;DR：一句話描述最可能的失敗點
- Error chain：從最底層 root exception 往外整理（用條列）
- Suspect component：最可能出問題的模組/服務
- 需要補充的資訊（最少集合）：我還要提供哪些 log/環境/版本資訊才能鎖定
- 2 條最短實驗（10 分鐘內能做的）
```

## 3) 大量 log（用 trace id / correlation id 做故事）
**Prompt**
```
你是 incident investigator。請把大量 log 整理成一個「時間線敘事」。

背景：
- 期待行為：{{expected_behavior}}
- 實際行為：{{actual_behavior}}
- request/trace id：{{ids_if_any}}

log：
{{paste_logs}}

請輸出：
1) 時間線（按時間排序，合併重複訊息）
2) 關鍵分岔點（哪一行 log 讓你改變判斷）
3) 最可疑根因（含可信度 0-100%）
4) 建議新增的觀測點（metric/log field/span）
```

## 4) Flaky test / race condition 排查
**Prompt**
```
你是測試穩定性專家。以下是 flaky test 的資訊：
- 測試名稱：{{test_name}}
- 失敗比例：{{fail_rate}}
- 常見錯誤：{{common_error}}
- 近期變動：{{recent_changes}}
- 測試/程式碼片段：
{{code_snippet}}

請你給：
1) 可能原因清單（按優先順序：時間、共享狀態、非決定性、外部依賴）
2) 每個原因對應的驗證方式（怎麼證明/排除）
3) 最小修復方案（prefer：隔離、注入時間、mock、重試策略）
4) 長期方案（架構層面）
```
