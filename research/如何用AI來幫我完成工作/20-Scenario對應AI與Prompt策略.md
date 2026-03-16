# 20 - Scenario 對應 AI 與 Prompt 策略

目標：針對 `10-工作情境Scenario盤點` 中的每個情境，為「AI 可以怎麼幫忙」定義具體的使用方式（prompt pattern / workflow / 限制）。

## 結構建議

每個情境用以下格式記錄：

```markdown
## 情境名稱

### 1. 目標
（我要用 AI 達成什麼？）

### 2. 可用工具
- Antigravity / Gemini
- OpenAI / Claude（如適用）
- OpenClaw 內的 agent / node
- Google 內部專用工具（若有）

### 3. Prompt / Workflow 模板
- Step 1: 我先準備什麼資訊？
- Step 2: 丟給 AI 的指令長什麼樣子？
- Step 3: AI 回傳後，我怎麼驗證 / 再 refine？

### 4. 風險與限制
- 資料安全 / 權限
- 容易 hallucinate 的地方

### 5. 與現有流程的整合
- 可以取代 or 強化哪一步？
```

> 註：這一份檔案先放「格式 + 幾個代表性的情境」，之後可以逐一把 scenario 補上。
