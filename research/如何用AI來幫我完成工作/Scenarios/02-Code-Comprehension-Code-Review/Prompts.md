# Prompts — Code Comprehension / Code Review

## 1) 10 分鐘理解 legacy module（導讀）
**Prompt**
```
你是資深軟體架構師。請把我貼的程式碼當成你第一次看到的 legacy code。

目標：讓我在 10 分鐘內掌握：它做什麼、誰依賴它、風險在哪。

程式碼/檔案（可多段）：
{{paste_code_or_files}}

請輸出：
- 這個模組的責任邊界（做/不做什麼）
- 主要資料流與控制流（用 5~10 點條列）
- 關鍵抽象/命名對照表（domain term → code symbol）
- 3 個最可能踩雷點（並指出對應行為/函式）
- 我如果要改動 X（{{change_goal}}），最安全的切入點是哪裡
```

## 2) 產生「我該問作者的問題」清單
**Prompt**
```
請根據這段 code/PR 內容，生成我在 review 時最該問作者的問題。

PR 目的：{{pr_goal}}
Diff/Code：
{{paste_diff_or_code}}

輸出格式：
- Must-ask（阻擋合併的問題）
- Should-ask（品質/維護性）
- Nice-to-ask（風格/一致性）
每一題都要附：為什麼問、預期好的答案長什麼樣。
```

## 3) Pre-review：先找出明顯問題（含嚴重性）
**Prompt**
```
你是 code reviewer。請針對以下 diff 做 pre-review。

Diff：
{{paste_diff}}

請輸出：
1) High risk（安全性/資料一致性/效能/並發）
2) Correctness（邏輯錯誤、edge case）
3) Maintainability（命名、抽象、重複）
4) Tests & Observability（該補的測試/監控）

每一點請附：
- 嚴重性：blocker/major/minor
- 建議修改（可直接貼建議程式碼片段）
```

## 4) 生成 review comment 草稿（口氣像我）
**Prompt**
```
請把以下 issues 轉成「我可以直接貼到 code review 的留言」。

我的風格：
- 直接、友善、具體
- 先肯定再指出風險
- 提供可行替代方案

Issues：
{{paste_issue_list}}

請輸出每則 comment 都包含：
- 背景（為何重要）
- 風險（具體會怎麼壞）
- 建議（prefer + alternative）
```
