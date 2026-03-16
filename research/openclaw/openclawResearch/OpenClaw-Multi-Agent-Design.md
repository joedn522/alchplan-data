# OpenClaw 多 Agent 設計（不依賴 nodes，信任 Tailscale 內網）

> 目標：
> - 對內（Tailscale 網路內）：所有 OpenClaw instance 視彼此為「可信節點」，用簡單的 HTTP / 檔案通道合作，不再被 gateway token 綁死。
> - 對外（手機 / 公網）：仍透過 Telegram / Gateway auth 保持安全。

---

## 1. 角色與網路邊界

### 1.1 角色（每一支都是獨立 OpenClaw）

- **Mac mini / Pi**
  - 主要職責：
    - 總策展：整合 Obsidian / Daily / Research。
    - 高階決策：幫我想「要問誰」、「這個任務應該丟給哪支 Agent」。
  - 有自己的 Gateway + Telegram bot。

- **WSLC（Voice Agent）**
  - 主要職責：
    - 處理語音相關：電話 → 語音 → 文字 → 研究對話。
    - 直接讀寫 Obsidian `/Research` 與 `openclaw/openclawResearch`。

- **Finbot WSL（Quant / Work Agent）**
  - 主要職責：
    - 台股量化、工作自動化、API 研究。

> 三者都是獨立的 OpenClaw 實例，各自有：
> - 自己的 Gateway（不同 port / token）
> - 自己的 Telegram Bot（或共用一個 bot，不同指令路由）

### 1.2 網路邊界

- **內網邊界**：
  - 所有主機（Mac mini / WSLC / Finbot）都在同一個 Tailscale 網路。 
  - 內網互相溝通只看：
    - `tailscale-ip:port`
  - 對內假設：
    - 只要封包來自 Tailscale 網段，就被視為「自己人」。（安全前提：Tailscale 本身的 node 控制權在我手上）

- **外網邊界**：
  - 手機 / 公網使用者 → 只能透過 Telegram / WhatsApp / Bridged Gateway 進入。
  - 對外仍保留 Gateway Token / Channel 的 auth 機制。

---

## 2. 對內：多 Agent 如何互相「問問題」？

### 2.1 不再使用 Gateway nodes / gateway token 做內部串接

- Nodes 模式：
  - Mac mini Gateway 視其他機器為「工作節點」，需要它們用 `OPENCLAW_GATEWAY_TOKEN` 連進來。
  - 現實問題：auth 行為易壞，一壞就整條線死。

- 改良模式：
  - **每支 Agent 都跑自己的 Gateway，但對內溝通不透過 Gateway 協定**。
  - 對內溝通使用：
    - HTTP API
    - 檔案（Obsidian Vault）
    - 任意你定義的協議，而不是 `openclaw nodes`。

### 2.2 具體模式：HTTP API + Obsidian

- 每支 Agent 對內暴露一組簡單的 HTTP 介面（只在 Tailscale 網路可見）：

  例如 WSLC（Voice Agent）:

  ```text
  POST http://wslc:5050/voice/query
  Body: {
    "from": "pi",          // 呼叫來源，可用來做紀錄
    "intent": "research",  // 大致用途
    "text": "幫我整理今天錄音的重點，寫回 Research/xxx.md"
  }
  ```

- 回傳：

  ```json
  {
    "status": "ok",
    "reply": "已根據錄音建立摘要並寫入 Research/2026-02-20-voice-log.md",
    "meta": {
      "note_path": "Research/2026-02-20-voice-log.md"
    }
  }
  ```

- Mac mini / Pi 如果要請 WSLC 幫忙：
  - 不是用 `openclaw nodes run`，
  - 而是用標準 HTTP client 發一個 POST，文字交給 WSLC 處理。

> 這樣的好處：
> - 不需要知道 WSLC 的 Gateway Token。
> - 內部認證只要你願意，可以完全基於「Tailscale IP + 自訂 API key」。

### 2.3 以 Tailscale 作為信任網

- 規則：
  - 只接受來自 Tailscale 網段的 HTTP 請求。
  - 可選：再加一個簡單的 `X-API-Key`（所有內部 Agent 共用同一把 key）。

- 語意：
  - 「只要你能打到我（在這個封閉 Tailscale 網路裡），我就當你是自己人。」
  - 不再把 Gateway Token 當成內部協作的唯一憑證。

---

## 3. 對外：仍透過各自的 Gateway / Telegram 控制

- 每支 Agent 對外的入口還是：
  - Telegram Bot
  - 或 Web UI / Control UI

- 對外訪客不在 Tailscale 裡：
  - 還是走 Gateway auth / Channel auth。

- 使用方式：
  - 「我自己」要找哪一支 Agent，就開對應的 Telegram 聊天。
  - 每支 Agent 可以有：
    - 單獨的 Bot（如：Pi、Finbot、VoiceAgent）
    - 或共用 Bot，用前綴指令（/pi /finbot /voice）做路由。

---

## 4. 實際操作體驗（對你的角度）

- 我（人）層級：
  - 開車時：
    - 用 Telegram 語音對「VoiceAgent Bot」講話。
  - 坐在電腦前：
    - 在 Mac mini 上用 Pi + Obsidian 看所有 Agent 寫回來的研究 note。
  - 想看 Quant：
    - 找 Finbot 的聊天視窗。

- Agent 互動層級：
  - Pi 需要 VoiceAgent 做事：
    - 發 HTTP POST 到 WSLC 的 `/voice/query`。
  - Pi 需要 Finbot 做事：
    - 發 HTTP POST 到 Finbot 的 `/quant/query`。

- 所有這些對內的 HTTP 呼叫：
  - 都建立在「Tailscale 內網 + 自訂 API key」之上，
  - 完全不碰 `gateway.auth.token` 或 `openclaw nodes` 的那套。

---

## 5. 小結

- 是，這個做法符合你描述的「對內彼此信任、對外嚴格 auth」：
  - 對內：以 Tailscale 為信任網，Agent 間透過 HTTP / Obsidian 合作，不再被 Gateway Token 卡住。
  - 對外：手機 / 公網使用者仍然需要透過 Telegram / Gateway auth 進入，各自的 Gateway Token 只保護「自己這一支」。

- 接下來可以做的實作路線：
  1. 在 WSLC 上設計 `voice/query` API（內部 HTTP 介面）。
  2. 在 Finbot 上設計 `quant/query` API。
  3. 在 Mac mini / Pi 這邊，寫一組小工具（或 skill）來呼叫這些 HTTP API。

這份設計就是多 Agent 的「不靠 nodes、信任 Tailscale 內網」版藍圖，未來可以再細化每支 Agent 的 API 規格與安全策略。