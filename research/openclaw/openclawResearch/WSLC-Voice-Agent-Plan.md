# WSLC 語音代理計劃（暫時獨立於 Mac mini）

> 目標：在 WSLC 上建立一個「可以接電話、自己理解 Obsidian 研究內容、用語音跟我對話」的獨立語音 LLM Agent，未來再和 Mac mini / Pi 串接。

---

## 0. 現況與策略

- Mac mini Gateway ⇄ Nodes 的 auth 在目前 2026.2.x 版本下有不穩定行為，WSLC 一直卡在 `1008 token mismatch`。
- 為了不要讓「語音研究系統」被 Gateway bug 卡死，改採：
  - **WSLC = 獨立語音 Agent 節點**
  - Mac mini / Pi 先當「設計師與總召」，之後再透過 API / 檔案同步串起來。

---

## 1. WSLC 應用架構總覽

1. **電話進線層（Telephony & Media）**
   - 使用 Twilio 作為 PSTN ↔ VoIP 橋接。
   - 在 WSLC 上跑一個語音媒體服務（建議：LiveKit 或簡化版的 WebSocket + WebRTC Gateway）。
   - 任務：
     - 接收來電 → 建立語音流 → 丟給 WSLC 本機的 STT。
     - 把 WSLC 產生的語音 TTS 回放給電話端。

2. **語音 ⇄ 文字 ⇄ LLM（Core Agent）**
   - STT：`faster-whisper`（利用 5080）
     - 對接 LiveKit/Twilio 推過來的音訊
     - 輸出乾淨文字（含 basic segmentation）。
   - LLM：本地 LLM（Ollama + DeepSeek / Llama3）或在 WSLC 上跑一顆獨立 OpenClaw gateway + agent。
   - TTS：
     - 短期可以走 ElevenLabs API 或 Groq Orpheus；
     - 長期建議測試本地 TTS（例如 Sherpa-ONNX TTS）放在 5080 上跑。

3. **知識層：WSLC 直接讀寫 Obsidian**
   - 在 WSLC 掛載 Obsidian Vault：
     - 透過同一套 Self-hosted LiveSync (CouchDB)，或
     - 透過 SMB / NFS 從 NAS 或 Mac mini 掛載 `asherdb`。
   - 任務：
     - 直接讀 `/Research`、`/openclaw/openclawResearch` 中的研究筆記。
     - 把電話對話 → 研究摘要 → 待辦，寫回 Obsidian（例如 `openclaw/daily` 與相關 research note）。

---

## 2. 需求對照（對應你的 1–5 點）

### 2.1 接電話（你的 1）

- **具體實作**：
  - Twilio 號碼 → Twilio Voice Webhook → 轉到 WSLC 上的語音服務端點（例如 `https://wslc.example/voice/incoming`）。
  - WSLC 的語音服務：
    - 接收來電事件（開始 / 結束 / 轉接）。
    - 建立音訊流傳給 STT 模組。

### 2.2 打電話 → 語音 → 本機 LLM / 本機 OpenClaw（你的 2）

- 第一階段：
  - 打電話 → STT → 把文字餵給「WSLC 本地 LLM 互動 loop」。
  - LLM 角色：
    - 讀研究 note，理解 context。
    - 用中文回覆你現在的想法、建議、問題解答。
  - 回覆流程：LLM 出文字 → TTS → 回放到電話。

- 第二階段（可選）：
  - 在 WSLC 上跑一顆獨立 OpenClaw（小型 Gateway+Agent）：
    - 優點：可以用 skills/cron，語音只是一種入口。
    - 缺點：相當於第二套 OpenClaw universe，未來要和 Mac mini 合併需要設計手動同步或 API bridge。

### 2.3 WSLC import Obsidian（你的 3）

- **建議路線**：
  - 使用現有的 Self-hosted LiveSync（你 NAS 上的 CouchDB），讓 WSLC 加入同步：
    - Vault path：`~/asherdb`（WSLC 端）
    - LiveSync 指向同一 CouchDB DB。
  - 如此一來：
    - 你在 Mac mini 改的 Research note → LiveSync → WSLC 立即看得到。
    - 你在電話裡講的研究更新 → WSLC LLM 整理 → 寫回 Obsidian → LiveSync 回 Mac mini。

### 2.4 先獨立跟 WSLC 聊天與改 Obsidian（你的 4）

- 在 auth 修好前，Pi 先不介入 WSLC 的 runtime：
  - 你透過 **電話** 或 **簡單的 Web UI / WebSocket client** 跟 WSLC 直接對話。
  - WSLC 直接讀 `/Research` 內的筆記，幫你改寫、補充、整理。
  - 所有變更都經由 Obsidian Vault 同步回 Mac mini，Pi 只在筆記層面看到結果。

### 2.5 LLM 透過電話輸出（你的 5）

- 對話 loop 設計：
  1. 你講話 → STT → 文字
  2. LLM（WSLC）基於當前研究 note + 歷史對話決定要說什麼
  3. 把回覆文字送給 TTS → 實時回放給你
  4. 同步將這段「語音對話」寫回 Obsidian：
     - 例如寫入 `Research/如何在車上-走路-回到家的電腦前與 Pi 做研究/Voice-Logs/2026-02-19.md`

---

## 3. 建議用的「聊天 / 語音堆疊」組合

### 3.1 Telephony & Media

- **Twilio**：PSTN 號碼 + Webhook
- **LiveKit**（推薦）或更簡化的自建 WebRTC server：
  - 優點：
    - 專門為實時語音/視訊設計
    - 可以在 WSLC 本機跑，流量只在你家/公司網路裡

### 3.2 LLM

- 初期：Ollama + DeepSeek / Llama3
  - 好處：
    - 可以完全離線跑在 5080 上
    - 避免額外 API 成本

- 未來：如 auth 修好後，可改成 WSLC 上跑一顆 OpenClaw Agent，讓 Pi 也能透過 HTTP/Nodes 和它溝通。

### 3.3 Obsidian

- WSLC 使用和 Mac mini 相同的 Vault / LiveSync 設定：
  - Vault 根目錄：`~/asherdb`
  - 重點資料夾：
    - `/Research`：你的研究專題（例如 Voice/Research 流程）
    - `/openclaw/openclawResearch`：OpenClaw + Agents 的設計文件
    - `/openclaw/daily`：每日 tips / 操作筆記

---

## 4. 後續與 Mac mini / Pi 串接計劃

在 WSLC 語音 Agent 跑穩之後，再處理 auth / pairing 問題，比較不痛苦：

1. **第一階段（現在）：**
   - WSLC 完全獨立運作語音 Agent
   - 只透過 Obsidian Vault 與 Mac mini / Pi 同步資訊

2. **第二階段（之後）：**
   - 修復 Mac mini Gateway ⇄ Nodes auth（等待 OpenClaw 新版或更穩定的修復指南）
   - 把 WSLC 也掛為 Mac mini 的 node，Pi 就可以透過 `nodes.run` 直接下指令給 WSLC

3. **第三階段（最終）：**
   - Pi 可以：
     - 派 WSLC 去做長時間語音研究任務（例如 60 分鐘通話摘要 + research note 整理）
     - 自動在 Obsidian 裡建立與語音對話對應的研究分頁

---

## 5. 給 Antigravity 的 Setup 任務摘要

> 給 Antigravity / 内部工具看的簡化版需求：

- 在 **WSLC** 上部署：
  1. Twilio +（建議）LiveKit 的語音接入服務（可接受電話打入，將語音流轉給本地 Python 程式）。
  2. Python 語音橋接服務：
     - `faster-whisper`(GPU=RTX 5080) 做 STT。
     - 一個本地 LLM（DeepSeek / Llama3 via Ollama）。
     - TTS（ElevenLabs API 或本地 sherpa-onnx-tts）。
  3. Obsidian Vault 掛載與同步：
     - Vault：`~/asherdb`
     - 確保 `/Research` 與 `/openclaw/openclawResearch` 與 Mac mini 同步。

- 用戶流程：
  - 使用者打電話 → WSLC 接聽 → 語音轉文字 → LLM 回應 → 語音回放 → 同步寫入 Obsidian 研究筆記。

這份文件之後可以作為 Antigravity 的 setup spec，讓他幫你把 WSLC 語音 Agent 先搭起來，等 Mac mini 的 auth/nodes 問題穩定後，再補上「Pi ⇄ WSLC」的正式串接。