# OpenClaw Skill Map（依 Asher 的使用情境整理）

> 目的：不是「裝一堆 skill」，而是把你**最近實際用我的情境**拆成模組，對應到「哪些 skill 類型 / 候選 skill」最能補齊能力；並把待研究清單歸檔在 Obsidian，讓你有空可以慢慢看。

## 0) 你的主要使用情境（我目前掌握）

### (A) Obsidian 中心化知識/日記系統（落地到 Vault）
- 每日 OpenClaw Tip → 寫入 `openclaw/daily/YYYY-MM-DD.md`
- 每日台股量化 Tip → 同步追加到同一份 daily 檔
- 每日技能打撈（skill survey）→ 寫入 `openclaw/dailySkill/YYYY-MM-DD-Skill-Survey.md`
- 語音/錄音 → 轉寫 → 丟進 Obsidian inbox（你已經把 Notion 當成 deprecated）

### (B) 自動化 pipeline / cron / scripts
- 你要的是「我能自動跑完」而不是只給建議
- 典型流程：抓資料 → 摘要/整理 → 寫入 Obsidian → 留下可追溯的 log

### (C) 研究/蒐集/整理
- 你會把連結貼來叫我摘要、做行動點
- 你希望我把「工具/skill 的研究結果」也落地在 Obsidian，可回顧、可迭代

### (D) 次要但重要：自架/維運/安全
- 同步（iCloud / LiveSync / CouchDB）
- cron 穩定性、備份、權限最小化、避免供應鏈風險

---

## 1) 你選的方向 C：A + B 都要（我的執行拆解）

### A：Browser & Automation（登入網站、抓資料、填表）
**你會立刻感受到的提升：**
- 需要登入才能讀/抓的內容（不靠 API、或 API 很難接）→ 我能直接做 UI automation
- 自動把資料抓回來，變成 Obsidian 內的 note / table / checklist

### B：Obsidian Inbox → 自動歸檔/摘要/每日戰情室
**你會立刻感受到的提升：**
- 任何輸入（語音、網頁、訊息、截圖）都有一致的「落地格式」
- 每天自動生成：今日戰情室（行程/任務/今日 tip/昨日回顧/今日 focus）

---

## 2) Skill 來源與風險說明（先講清楚）

- `awesome-openclaw-skills` 是「索引/清單」，不是單一 skill。
- 社群 skill：**curated ≠ audited**。很多 skill 可能會碰到：
  - `exec`（能跑本機命令）
  - 檔案系統讀寫（可能讀到 Vault / 私人資料）
  - 網路連線 / 上傳資料
- 所以本文件會把 skill 分成：**值得優先審查** / **候補** / **低優先**。

---

## 3) 你今天打撈到的 10 個候選（先歸檔、待你有空審）

來源：`openclaw/dailySkill/2026-02-27-Skill-Survey.md`

### 第一優先（可能高回報，但必須審 code/權限）
- tools-ui
- pls-agent-tools
- elite-tools
- composio-integration
- mcp-adapter
- webmcp / web-mcp

### 第二優先（看你是否真的需要）
- qveris
- ydc-ai-sdk-integration

### 低優先（除非你近期要做內容/行銷輸出）
- engineering-as-marketing

---

## 4) 從 awesome list 抽出的「跟你情境最相關」類別（閱讀索引）

> 我先各抓一小段 sample（每類前 15 個）讓你快速感受風格；之後你如果要，我可以再針對某類往下挖「更像你會用的那幾個」。

### 4.1 Browser & Automation（A 路線核心）
- [Agent Browser](https://github.com/openclaw/skills/tree/main/skills/thesethrose/agent-browser/SKILL.md) - Rust-based headless browser automation
- [anycrawl](https://github.com/openclaw/skills/tree/main/skills/techlaai/anycrawl/SKILL.md) - Scrape/Crawl/Search web
- [android-adb](https://github.com/openclaw/skills/tree/main/skills/staticai/android-adb/SKILL.md) - 控 Android（如果你要把手機當 worker/感測器會很有用）

### 4.2 Notes & PKM（B 路線核心）
- [agent-memory-ultimate](https://github.com/openclaw/skills/tree/main/skills/globalcaos/agent-memory-ultimate/SKILL.md) - 進階 memory system（SQLite/FTS）
- [chaos-mind](https://github.com/openclaw/skills/tree/main/skills/hargabyte/chaos-mind/SKILL.md) - hybrid search memory
- [blogwatcher](https://github.com/openclaw/skills/tree/main/skills/steipete/blogwatcher/SKILL.md) - RSS/Blog 監控（很適合「每日戰情室」的輸入源）

### 4.3 Speech & Transcription（你的錄音/語音輸入管線）
- [assemblyai-transcribe](https://github.com/openclaw/skills/tree/main/skills/tristanmanchester/assemblyai-transcribe/SKILL.md)
- [deepgram](https://github.com/openclaw/skills/tree/main/skills/nerkn/deepgram/SKILL.md)
- （你現在已有本機 Whisper 流程；若要雲端/更快/更準再考慮）

### 4.4 Calendar & Scheduling（做「今日戰情室」必備）
- [apple-calendar](https://github.com/openclaw/skills/tree/main/skills/tyler6204/apple-calendar/SKILL.md)
- [apple-reminders](https://github.com/openclaw/skills/tree/main/skills/steipete/apple-reminders/SKILL.md)
- [cron-scheduling](https://github.com/openclaw/skills/tree/main/skills/gitgoodordietrying/cron-scheduling/SKILL.md)

### 4.5 Search & Research（你貼連結叫我整理/摘要）
- [agent-deep-research](https://github.com/openclaw/skills/tree/main/skills/24601/agent-deep-research/SKILL.md)
- [aluvia-brave-search](https://github.com/openclaw/skills/tree/main/skills/bertxtrella)
- [aluvia-web-proxy](https://github.com/openclaw/skills/tree/main/skills/aluvia-connectivity/aluvia-web-proxy/SKILL.md)

### 4.6 Self-Hosted & Automation（穩定性/維運）
- [cron-backup](https://github.com/openclaw/skills/tree/main/skills/zfanmy/cron-backup/SKILL.md)
- [cron-retry](https://github.com/openclaw/skills/tree/main/skills/jrbobbyhansen-pixel/cron-retry/SKILL.md)
- [gotify](https://github.com/openclaw/skills/tree/main/skills/jmagar/gotify/SKILL.md)
- [freshrss-reader](https://github.com/openclaw/skills/tree/main/skills/nickian/freshrss-reader/SKILL.md)

### 4.7 Security & Passwords（擴充能力前先打底）
- [1password](https://github.com/openclaw/skills/tree/main/skills/steipete/1password/SKILL.md)
- [bitwarden](https://github.com/openclaw/skills/tree/main/skills/asleep123/bitwarden/SKILL.md)
- [claw-permission-firewall](https://github.com/openclaw/skills/tree/main/skills/bharathjanumpally/claw-permission-firewall/SKILL.md)
- [authensor-gateway](https://github.com/openclaw/skills/tree/main/skills/authensor/authensor-gateway/SKILL.md)

---



## 4.x 名詞/工具速查（你說的：文件裡提到很多 tool，這裡先寫清楚）

> 這一段的目的：讓你回頭看這份筆記時，不需要再猜每個東西是什麼、為什麼跟你有關、以及主要風險點。

### Browser Automation / Headless Browser
- **是什麼**：用程式控制瀏覽器（登入、點按、抓內容、填表）。
- **對你有什麼用**：把「需要登入才能看的網站」自動抓取並落地到 Obsidian。
- **主要風險**：憑證/Session 管理、被網站封鎖、以及 automation 可能誤操作（所以要驗收/回放）。

### RSS / Feed 監控（例如 blogwatcher）
- **是什麼**：訂閱網站更新（RSS/Atom），自動抓新文章標題與內容。
- **對你有什麼用**：做「每日戰情室」的輸入源，不用你手動巡。
- **主要風險**：相對低；注意來源品質與噪音。

### MCP（Model Context Protocol）/ Adapter / WebMCP
- **是什麼**：一種把外部工具（或工具伺服器）標準化接進 agent 的協定/轉接層。
- **對你有什麼用**：把很多外部能力變成「可插拔積木」，後續擴充成本更低。
- **主要風險**：接到的 MCP server 若權限過大，等於把你的資料與機器暴露給更多外部程式；必須做權限最小化與來源審查。

### Composio Integration（SaaS 工具聚合）
- **是什麼**：用一套整合層接很多 SaaS（信箱、日曆、文件、CRM…）。
- **對你有什麼用**：你要的「抓資料→整理→寫入 Obsidian」pipeline 會變得更好串。
- **主要風險**：token 權限範圍很容易開太大；需要嚴格控管 secrets 與 scope。

### Secrets 管理（1Password / Bitwarden）
- **是什麼**：把 API keys / tokens / 密碼用專門工具管理，而不是散在腳本或環境變數裡。
- **對你有什麼用**：你越自動化，越需要一個「可控、可撤銷、可輪替」的憑證策略。
- **主要風險**：幾乎是「減風險」的工具；但要避免把 master password/解鎖流程寫死。

### Policy Gate / Permission Firewall（權限保護類）
- **是什麼**：在技能/工具執行前做檢查與限制（例如：限制網路、限制檔案路徑、限制 exec）。
- **對你有什麼用**：你要裝社群 skill 時的安全護欄。
- **主要風險**：設定錯會「太嚴導致不好用」或「太鬆導致沒保護」，需要迭代。

### Cron Retry / Backup / Gotify（穩定性三件套）
- **cron-retry**：任務失敗自動重試（例如網路抖動、暫時性錯誤）。
- **cron-backup**：定期備份（包含清理策略/版本保留）。
- **gotify**：任務完成/失敗推播（你不必一直盯著）。


### 具體工具/skill 範例（本頁出現過的連結）

> 這裡不是要你全裝，而是讓你看到名字時能立刻知道它大概在解什麼問題。

- **Agent Browser**：偏「可程式化的 headless browser」工具鏈。適合做登入後抓資料/批次操作。風險：需要管好 cookies/session。
- **AnyCrawl**：偏 API 形式的 crawl/scrape/search。適合把網頁變成可結構化輸入源。風險：第三方服務/成本。
- **android-adb**：用 ADB 控 Android（截圖、取 UI 結構、點按）。如果你未來要把手機當「感測器/worker」很有用。

- **agent-memory-ultimate / chaos-mind**：偏「外掛記憶/檢索系統」（常見會用 SQLite/FTS、embedding）。對你這種 Obsidian 長期累積很有幫助，但要注意資料落地位置與隱私。

- **blogwatcher / freshrss-reader**：RSS/Feed 監控與閱讀。你如果要做「每日戰情室」資訊源，這兩類很搭。

- **assemblyai-transcribe / deepgram**：雲端語音轉文字（STT）。你現在已有本機 Whisper；這兩個主要價值是速度/語言模型/額外功能（但會把音檔送出機器）。

- **apple-calendar / apple-reminders**：把 macOS 內建行程/提醒事項接進來。用來做「今日戰情室」很直接。

- **agent-deep-research / aluvia-brave-search**：研究/搜尋增強，用來做「貼網址→摘要→存 Obsidian」會更強。
- **aluvia-web-proxy**：解 403/反爬或網路封鎖類問題（視情境）。風險：代理來源與資料外流。

- **cron-scheduling / cron-retry / cron-backup**：排程、失敗重試、備份（穩定性三件套）。
- **gotify**：把任務完成/失敗推播到手機/通知中心，避免你一直盯著。

- **1password / bitwarden**：secrets 管理（強烈建議至少選一個當底座）。
- **claw-permission-firewall**：執行時的權限護欄（限制技能能做什麼）。
- **authensor-gateway**：偏 policy gate / 安全閘門概念；用來在「裝社群 skill」時做風險控管。


#### 建議用法四欄表（先補最相關的 12 個；其餘我再續補）

> 欄位定義：
> - **適用情境**：什麼情況下你會真的用到
> - **建議用法（依你的系統）**：我會怎麼把它接到 Obsidian / cron / dashboard
> - **是否值得裝**：以你的使用頻率與槓桿評估（優先 / 次要 / 觀望）
> - **需要哪些權限/風險點**：你審查時要看的重點

| Tool/Skill | 適用情境 | 建議用法（依你的系統） | 是否值得裝 | 需要哪些權限 / 風險點 |
|---|---|---|---|---|
| Agent Browser | 你想把「登入後才能看的內容」自動抓回來（PressPlay/會員後台/儀表板） | 先做一個最小驗收：固定頁面→抓取→摘要→寫入 `Reading/`，並在 `dashboard/War-Room.md` 放今日更新連結 | **優先（但先緩緩，等你有空再做）** | 需要瀏覽器控制、可能保存 cookies/session；誤操作風險；被網站封鎖風險 |
| AnyCrawl | 你需要大規模抓取/整理網站內容（不一定要登入） | 當「資料來源層」：每天抓新文章→摘要→落地 Obsidian；比起 UI automation 通常更穩 | 優先/次要（視你是否常抓網站資料） | 走第三方 API：成本、速率限制、資料外流風險 |
| blogwatcher | 你有一堆固定追蹤的內容來源（RSS/Atom） | 變成「每日戰情室」的 feed：早上自動抓新文章標題→你只看我整理的 shortlist | **優先** | 主要是噪音/來源品質；權限風險低 |
| freshrss-reader | 你有自架 FreshRSS（或願意自架）想集中管理訂閱 | 我幫你把 FreshRSS 當 single source：每天拉 headlines→寫入 Obsidian daily digest | 次要（你有沒有 FreshRSS 決定一切） | 需要連自架服務；API key/帳密管理 |
| apple-calendar | 你想做真正可用的「今日戰情室」 | 每天固定時間同步今日行程→寫入 `dashboard/War-Room.md` + Daily Note | **優先** | 需要讀行事曆；注意不要把私人行程外送到雲端模型 |
| apple-reminders | 你有在用 Reminders 當快速待辦 | 把今日待辦同步到 War-Room；或把你訊息裡講的待辦直接寫進 Reminders | 次要（看你是否用 Reminders） | 需要讀寫提醒事項；資料隱私 |
| cron-scheduling | 你想用自然語言管理/生成 cron | 把「每日戰情室」「每日 digest」這些排程更系統化，避免散落在腳本 | 次要 | 會改你的排程；需要審清楚它會寫哪些檔案/命令 |
| cron-retry | 你不想因為網路抖動/暫時失敗就漏資料 | 對抓取/同步任務加上 retry，提升穩定性 | **優先（穩定性）** | 可能造成重複寫入；要有去重策略 |
| cron-backup | 你要保證 Obsidian/設定/輸出檔可回復 | 對 `openclaw/` 產出的資料做版本化備份（含保留策略） | **優先（安全感）** | 需要讀寫備份位置；空間管理 |
| gotify | 你想任務跑完立刻知道，不用一直問我 | 任務成功/失敗推播到手機；適合長流程（抓取/整理/備份） | 次要 | 需要連 Gotify server；通知內容可能含敏感摘要 |
| 1password / bitwarden | 你開始接一堆 API/服務 token | 用 secrets manager 統一管理；腳本從 vault 讀取，避免硬編碼 | **優先（底座）** | 解鎖流程、權限 scope、避免把 master secret 暴露在 log |
| claw-permission-firewall / authensor-gateway | 你要裝社群 skill，又怕供應鏈/提示注入 | 當「安全閘門」：新 skill 先跑在受限模式；或要求人工核准高風險動作 | **優先（裝多 skill 前先上）** | 設太鬆沒意義；設太嚴會卡；需要明確策略（網路/檔案/exec） |


## 5) 我建議的「安裝/驗收」節奏（避免只裝到簡單玩具）

### Phase 0：安全底座（先做）
- Secrets 管理（1Password/Bitwarden 其一）
- 權限最小化 / policy gate（若適用）

### Phase 1：Browser Automation（A）
**驗收任務：**你指定 1 個需要登入的網站 → 我做到「抓取→摘要→寫入 Obsidian」。

### Phase 2：Obsidian Inbox/歸檔（B）
**驗收任務：**你指定 inbox 來源 → 我做到「套模板→自動歸檔→每日戰情室」。

### Phase 3：工具接入基建（MCP/Composio 類）
**驗收任務：**串 1 個 SaaS（Gmail/Calendar/Drive…）但輸出一律落地 Obsidian。

---

## 6) 我需要你回的兩個資訊（用來真的把 A+B 跑起來）
1) **你最想自動化的「需要登入的網站」是哪一個？**（最多 1–2 個）
2) 你希望「今日戰情室」存到哪個路徑？（預設：`openclaw/daily/`；或你指定 `dashboard/`）

