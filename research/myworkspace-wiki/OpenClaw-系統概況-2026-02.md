# OpenClaw 系統概況（草稿）

> 目的：把你目前的 OpenClaw / Obsidian / Windows WSL 架構完整記錄下來，之後可以整包丟給 Gemini 做討論與優化。
> 
> 狀態：這份是我先把你剛剛口述內容結構化成文件；下面有幾個「待確認」我用 ✅/❓標註，請你回我，我再補齊並修正版。

---

## 0) 一句話總結
- 你現在把 **Pi（我）當成 OpenClaw 的主要大腦/總控**：finlab 以外的事情先丟給我（特別是 Obsidian 筆記維護）。
- Windows 上用兩個 WSL 做不同角色：
  - `finlab`：量化交易/台股預測 + finlab_v2 web service
  - `voicebot`：未完成；預計做 Obsidian 維護與語音互動（Qwen 16B + Whisper）
- Obsidian（筆記系統）目前打算以 **NAS + CouchDB** 做核心儲存/同步方案（你希望所有節點都能回寫 Obsidian）。

---

## 1) 核心資料層（Knowledge Base）
### 1.1 Obsidian
- 角色：你的主知識庫 / BuJo / 任務與研究歸檔中心
- 同步/儲存：**NAS 端透過 CouchDB 儲存**（LiveSync 型態）
- 多節點寫入：
  - Pi（OpenClaw 中樞）會寫
  - Windows/WSL 節點也會寫

❓待確認：
- CouchDB endpoint/存取方式（Tailscale? LAN? 反代?）
- Vault 的「真實 single source of truth」現在是 NAS CouchDB，還是 iCloud vault？（或兩者混合）

---

## 2) OpenClaw 架構（運算/代理層）

### 2.0 角色分工（你目前的策略）
- **Pi（主中樞）**：
  - 你目前把除 finlab 以外的工作大多丟給 Pi
  - 近期主要工作：維護/整理 Obsidian 筆記、產出研究手冊/報告
  - 也負責 orchestrate（必要時叫 Claude/Codex 來寫 code）

✅你目前的思路：
- finlab 相關要做「寫 code」時，OpenClaw（agent）只當 PM/驗證員
- 真正產碼由 Claude/Codex 去寫
- 目標是：**不要讓 OpenClaw 讀太多 code 細節，避免 token 被 code/上下文吃爆**

❓待確認：
- 你所說的「OpenClaw 不要知道 code 的細部內容」是指：
  1) 不要把整個 repo 檔案內容餵進對話（節省 token）
  2) 還是要在系統層面做資料隔離（例如 finlab repo 只允許子代理/特定 session 讀）


### 2.1 Windows / WSL 節點
你目前在 Windows 下養兩個 WSL，讓 OpenClaw 在上面運作。

#### 2.1.1 WSL：`finlab`
- 目的：
  - hosting `finlab_v2` web service
  - 作量化交易、台股相關預測
- OpenClaw 在此的定位：
  - 你希望 OpenClaw 偏 PM / 驗證
  - 寫 code 交給 Claude/Codex（或 coding agent）

❓待确认：
- finlab_v2 service 的對外位置/port（目前你內部習慣怎麼連？）
- 主要計算/回測會跑在 WSL 還是另外有 worker？

#### 2.1.2 WSL：`voicebot`（規劃中）
- 目的：
  - 主力維護 Obsidian
  - 讓你能「跟這台 Windows 機器聊天」來整理 Obsidian
- 計畫部署：
  - 本地模型：Qwen 16B（❓是哪個 variant：Instruct? AWQ? GGUF?）
  - 語音轉文字：Whisper

❓待确认：
- 你想要 voicebot 對外提供什麼介面：
  - Telegram bot？
  - Web UI？
  - 純本地麥克風/喇叭的桌面對話？
  - 或 iPhone 語音 → server？

---

## 3) 你在擔心的點：這樣的配置是不是最佳解？
我把你的顧慮拆成兩個可討論的設計問題：

### 3.1 Token 成本 vs 工程效率
- 你希望 OpenClaw（主對話）不要吞太多 code context
- 但又希望它能驗證/控品質

可選策略（之後丟給 Gemini 討論）：
1) **摘要式驗證**：coding agent 產 PR/patch + 摘要 + test report，主對話只看摘要
2) **分層上下文**：主對話只看 spec/設計與測試結果；需要看 code 時只拉「局部檔案片段」
3) **嚴格隔離**：finlab repo 只允許在特定 session/subagent 讀取

### 3.2 多節點寫入 Obsidian 的一致性
- 你想讓 Pi/finlab/voicebot 都能寫入 Obsidian
- 但要避免：重複筆記、衝突、不同格式

可選策略：
1) 統一寫入入口（例如都寫到 Inbox/Voice-Inbox，再由整理流程 merge）
2) 每個節點固定寫入自己的 namespace（folder + frontmatter 標記來源）

---

## 4) 已確認資訊（2026-02-23）
### 4.1 Obsidian 同步策略（iCloud + CouchDB 並行）
- **兩者並行**
- 只有 **Mac 與 iPhone** 會真的去連 **CouchDB（LiveSync）**
- **Mac 端 vault 也會存在 iCloud**
- **Windows 端**：直接讀 iCloud 上（由 Mac 建立/維護）的 vault（不直接連 CouchDB）

### 4.2 Windows 可用性 / 外網需求
- Windows 打算長開
- 需要外網時手機也能連回（代表需要：安全的遠端通道與固定可連性）

### 4.3 finlab_v2 服務
- 部署位置：WSL（Windows）
- 啟動方式：直接用 Python 跑
- 對外 port：`8050`

### 4.4 voicebot 介面
- 互動介面：Telegram
- 實際上三台機器都用 Telegram 分別溝通（形成你的人機/機機控制面）

### 4.5 主對話的 token 策略
- 你選 (A)：主要是為了避免把整個 repo/大量 code 丟進主對話造成 token 爆炸
- 不是要做嚴格資料隔離（可視需要在工具層做局部讀取）

---

## 5) 下一步（我建議）
我會把這份文件補成一份「可以直接丟給 Gemini 討論」的版本，包含：
- 架構圖（文字版：資料流 / 控制流）
- 每個節點：責任、輸入/輸出、與 Obsidian 的寫入規則
- 外網連回 Windows 的安全設計（建議：Tailscale / 反代 / Telegram 控制面）
- finlab_v2（8050）如何安全曝光（僅 tailnet / reverse proxy / auth）
- 以及一段「給 Gemini 的提問清單」（要怎麼優化 token、角色分工、與可靠性）

## 6) 遠端連線與控制面（已確認）
### 6.1 Windows 端如何取得 Obsidian Vault
- Windows 端使用 **iCloud for Windows** 同步 vault 到 Windows 本機資料夾

### 6.2 外網手機如何連回（你的偏好）
- 你外網主要透過 **Telegram** 與 OpenClaw 溝通/下指令（作為控制面）
- 換句話說：你不一定需要「手機直接連回 Windows 的服務 port」；只要 OpenClaw 在 Windows/WSL 上能收 Telegram 訊息並執行即可

> 仍可選的進階補強（非必須）：若未來要直接從手機開 finlab web / SSH / code-server，再補上 Tailscale 或反代。
