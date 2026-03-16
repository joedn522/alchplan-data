# Prompts — Spec / Design / Doc

## 1) 從聊天/雜記整理成設計文件（一頁版）
**Prompt**
```
你是 Staff engineer。請把以下素材整理成一份「一頁式設計文件」。

素材（聊天/雜記/會議紀錄）：
{{paste_notes}}

輸出章節：
- Problem statement（含非目標）
- Requirements（功能/非功能）
- Proposed solution（架構圖用文字描述即可）
- Alternatives considered（至少 2 個）
- Risks & mitigations
- Rollout plan
- Open questions
```

## 2) 把設計文件轉成可執行 tasks / tickets
**Prompt**
```
請把以下設計文件拆成可執行的工程 tasks。

設計文件：
{{paste_design_doc}}

請輸出表格（用 markdown）：
- Task id
- Title
- Description（驗收標準 Given/When/Then）
- Owner role（BE/FE/SRE/Data）
- Dependencies
- Estimation（S/M/L）
- Risk
```

## 3) 產生 API doc + usage examples
**Prompt**
```
你是技術寫作者。請根據以下 API 介面/程式碼註解，產生 API 文件。

API：
{{paste_api_or_code}}

輸出：
- Overview
- Authentication / Error model
- Endpoints / Methods
- Request/Response examples（至少 2 個常見情境）
- Edge cases
- Versioning notes
```
