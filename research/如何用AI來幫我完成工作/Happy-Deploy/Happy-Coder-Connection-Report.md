# Happy Coder（slopus/happy）連線結構與網路路徑報告（針對 WSL2 / 手機連線問題）

> 目的：釐清 Happy Coder「到底怎麼連線」、哪些是 outbound、哪些需要 inbound，並解釋為什麼在 WSL2 會出現「掃 QR 成功但送訊息失敗」。

Repo: https://github.com/slopus/happy
（本報告根據 repo 內程式碼閱讀：`packages/happy-cli` / `packages/happy-server`）

---

## 1) 專案元件結構（monorepo）
Repo 根目錄下 `packages/`：
- `happy-cli`：你在電腦/WSL 跑的 CLI（`npm i -g happy-coder` 那個）
- `happy-app`：手機 App / Web UI（Expo）
- `happy-server`：同步/relay 的後端（E2E encrypted blobs + WebSocket）
- `happy-agent`：遠端 agent control CLI（更偏 server/控制面）
- `happy-wire`：加密/傳輸協定相關（底層）

---

## 2) 兩種「連線」其實是兩條不同的路
你現在直覺上把它想成「手機直連 WSL」——這在 Happy 的設計裡**不一定是主路徑**。
Happy 主要依賴一個後端 server 做「裝置間同步與指令轉送」，手機與電腦都各自連到 server（而不是彼此直連）。

### 2.1 Authentication（掃 QR）在做什麼？
程式碼：`packages/happy-cli/src/ui/auth.ts`
- CLI 產生 ephemeral keypair（TweetNaCl box）
- CLI 先 `POST {serverUrl}/v1/auth/request` 建立授權請求
- 然後顯示 QR：
  - mobile auth：`happy://terminal?<base64url(publicKey)>`
- 手機掃 QR 後會用 server 做授權流程
- CLI 端會一直輪詢 `POST {serverUrl}/v1/auth/request` 看授權狀態，成功後拿到 token/secret 寫到 `~/.happy/*`

**重點：**
- 這整段流程看起來是「CLI → server 的 outbound HTTPS」
- 手機也多半是「手機 → server」
- 所以你會看到：即使 WSL inbound 很爛，**掃 QR 依然可能成功**（因為主要是 outbound）

### 2.2 Daemon / Remote control（手機送訊息接管）在走什麼路？
Happy CLI 有個常駐 daemon，負責讓手機能遠端接管。

程式碼與設計文件：
- `packages/happy-cli/src/daemon/run.ts`
- `packages/happy-cli/src/api/apiMachine.ts`
- `packages/happy-cli/src/daemon/controlServer.ts`（本機控制面 HTTP server）
- `packages/happy-cli/src/daemon/CLAUDE.md`（repo 內自帶架構說明）

#### 2.2.1 Daemon 對外連線：**WSL → server 的 outbound WebSocket**
程式碼：`packages/happy-cli/src/api/apiMachine.ts`
- 會用 `socket.io-client` 連線到：
  - `serverUrl` 由 `HAPPY_SERVER_URL` 決定（預設值見下）
  - 轉成 ws/wss：`configuration.serverUrl.replace(/^http/, 'ws')`
  - path 固定：`/v1/updates`
  - transports 強制：`['websocket']`
- 這條連線是 machine-scoped（daemon 身分）

**這是 100% outbound**。只要 WSL 能上網，這條通常就通。

#### 2.2.2 手機下指令：**手機 → server →（透過 WebSocket RPC）→ daemon**
在 `ApiMachineClient` 裡，daemon 會註冊 RPC handler：
- `spawn-happy-session`
- `stop-session`
- `stop-daemon`

server 會透過 socket event `rpc-request` 把指令送到 daemon。

**所以理論上：如果完全走這條（手機/daemon 都連 server），WSL 的 inbound NAT 並不一定是問題。**

---

## 3) 那為什麼你會「手機送訊息壞掉」？（WSL2 NAT 仍可能是兇手）
雖然主控制面是「各自連 server」，但在實作上仍可能出現需要本機 inbound/localhost callback 的部分，尤其是：

### 3.1 OAuth callback / 本機 callback server（localhost）
以 Claude OAuth helper 為例：`packages/happy-cli/src/commands/connect/authenticateClaude.ts`
- 會在 `127.0.0.1` 開一個 HTTP server 接 OAuth redirect
- 預設 port `54545`（但也會找可用 port）

這種 callback server：
- 對「同一台機器上的瀏覽器」是 OK
- 但如果流程在手機端開 browser、或跨裝置跳轉，且 redirect 指向 `localhost`，就會出現「看得到但送不回去」的現象

不過：你描述的是 Happy app 送訊息給 CLI，不一定是 OAuth；但這類 localhost callback 是常見坑。

### 3.2 WSL2 造成「QR 裡的 host:port 指到 WSL IP」
你掃 QR 成功之後，如果 app 內部某段要打回你正在跑 happy 的那台機器（例如 LAN 模式、或某種 direct channel），而 QR/設定裡帶的是 WSL 的 `172.x.x.x`，手機在 Wi‑Fi LAN 上通常打不到。

這時你就會看到：
- 掃 QR（不需打回 WSL）可以
- 送訊息（需要打回某個 host/port 或 WebSocket）失敗

### 3.3 防火牆 / AP isolation
就算不是 WSL IP，Wi‑Fi AP isolation 也會讓「同網段裝置互打」失敗。

---

## 4) 重要設定：Happy CLI 的預設 server URL 不是 slopus 的那個字串
程式碼：`packages/happy-cli/src/configuration.ts`
- `serverUrl = process.env.HAPPY_SERVER_URL || 'https://api.cluster-fluster.com'`
- `webappUrl = process.env.HAPPY_WEBAPP_URL || 'https://app.happy.engineering'`

也就是說，你如果沒有設 `HAPPY_SERVER_URL`，CLI 會連到 `https://api.cluster-fluster.com`（而不是 README 上提到的 `happy-api.slopus.com` 那段文字）。

> 這不一定是 bug（可能是新域名/搬遷），但在除錯時要知道你實際連的是哪個 host。

---

## 5) 我建議你做的「最小實驗」（用來證明是不是 WSL inbound NAT）

### 實驗 A：確認 Happy daemon 是否只用 outbound WebSocket
1. 在 WSL 跑 `happy daemon start`（或你平常的啟動方式）
2. 同時在 WSL 看它有沒有 listen 非 localhost 的 port：
   - `ss -ltnp` 或 `netstat -tulpn`
3. 如果所有 listen 都是 `127.0.0.1`，那手機就不該是直連，應該是經由 server

### 實驗 B：抓「手機送訊息壞掉」時 CLI log
`happy` 的 log 位置通常在 `~/.happy/logs`（依 `configuration.happyHomeDir`）
把錯誤那段貼出來，通常能看到是：
- 連 server 的 ws 掛了？（outbound 問題）
- 還是 app 嘗試連某個本地位址/port？（inbound 問題）

---

## 6) 結論（回答你的核心問題）
- **如果 Happy 完全走標準設計：手機與 WSL/電腦各自連到 Happy Server（WebSocket），那 WSL 的 NAT inbound 不應該是主要問題**。
- **但你遇到「掃 QR OK、送訊息壞」很像有一段需要『打回你本機的 host/port』或拿到錯誤的 host（WSL 172.x）**，這就會被 WSL NAT / 防火牆 / Wi‑Fi 隔離打爆。

下一步要更精準定位，需要你提供：
1) 你 WSL 跑 `happy` 時的 `~/.happy/logs` 相關錯誤片段
2) 手機送訊息那刻 App 顯示的錯誤（若有）
3) 你目前是否有設 `HAPPY_SERVER_URL`（以及值）

---

## 附錄：關鍵程式碼位置（方便之後再查）
- Mobile auth QR：`packages/happy-cli/src/ui/auth.ts`
- CLI server URL 預設：`packages/happy-cli/src/configuration.ts`
- Daemon 架構文件：`packages/happy-cli/src/daemon/CLAUDE.md`
- Daemon 對 server WebSocket：`packages/happy-cli/src/api/apiMachine.ts`
- Daemon 本機控制 server（127.0.0.1）：`packages/happy-cli/src/daemon/controlServer.ts`
- Claude OAuth callback server：`packages/happy-cli/src/commands/connect/authenticateClaude.ts`
