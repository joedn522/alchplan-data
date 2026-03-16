# Prompts — 溝通 / 協作

## 1) 技術內容 → PM/非技術版（一分鐘能懂）
**Prompt**
```
請把以下技術內容改寫成 PM/非技術同事聽得懂的版本。

技術內容：
{{paste_technical}}

要求：
- 先講結論與影響（成本/風險/時程）
- 避免行話，必要行話要加括號解釋
- 最後給 3 個決策選項（含 trade-off）
```

## 2) Meeting notes → summary + action items
**Prompt**
```
你是會議記錄員。請把以下會議逐字/雜記整理成：摘要 + 決議 + 行動項。

內容：
{{paste_notes}}

輸出：
- Summary（5~10 點）
- Decisions
- Action items（Owner + Due）
- Open questions
```

## 3) RFC / 設計提案初稿（可被 review）
**Prompt**
```
你是技術寫作 + 架構顧問。請替以下提案生成 RFC 初稿。

提案目的：{{goal}}
背景：{{background}}
限制：{{constraints}}

請輸出章節：
- Motivation
- Goals / Non-goals
- Proposal
- Detailed design
- Security/Privacy
- Rollout & Migration
- Drawbacks
- Alternatives
- Unresolved questions
```
