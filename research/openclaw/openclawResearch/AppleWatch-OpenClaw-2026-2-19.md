# Apple Watch × OpenClaw (2026.2.19 版) 使用筆記

> 版本：OpenClaw v2026.2.19
> 功能重點：新增 Apple Watch companion MVP，支援「Watch inbox UI」「通知轉送」「Gateway 指令入口」。

---

## 1. 新增了什麼？（Release Note 摘要）

來源：`openclaw/openclaw` GitHub release v2026.2.19

- **iOS/Watch**
  - 加了一個 Apple Watch companion MVP：
    - Watch inbox UI（可以在手錶上看到簡易訊息 / 任務）
    - Watch notification relay handling（手錶通知轉給 Gateway / Agent）
    - Gateway command surfaces for watch status/send flows（在手錶上觸發一些「送狀態 / 簡訊息」的指令入口）
- **iOS/Gateway + APNs** 
  - Gateway 在呼叫 iOS/Watch node 前，會先透過 APNs 喚醒裝置，減少「背景睡死、invoke 失敗」的機率。

直觀理解：
- 手錶不是直接跑 OpenClaw，而是透過 **iOS App + Watch App + Gateway + APNs** 形成一個「手錶視窗」。
- 手錶可以：
  - 收到來自 OpenClaw 的簡短訊息 / 通知。
  - 觸發一些簡單的指令（例如：回覆固定模板、送一個狀態、快速丟一段短文字）。

---

## 2. 要怎麼用在我的 setup 上？（概念層）

### 2.1 前提條件

1. **Mac mini 上 Gateway 跑著**（你已經有）。
2. **iPhone 上有新版 OpenClaw App**（支援 2026.2.19 + Watch companion）。
3. **Apple Watch 和 iPhone 配對正常**，可以顯示 iOS 推播通知。

### 2.2 初次設定流程（高層步驟）

1. **更新 iPhone 上的 OpenClaw App** 到支援 Watch 的版本。
2. **在 iPhone 上啟用「Apple Watch companion」**（App 內應該會有設定或首次啟動 wizard）：
   - 授權通知（APNs）
   - 授權在 Watch 上顯示對應的 OpenClaw Inbox
3. **確保 Mac mini 的 Gateway 知道有這個 iOS/Watch node**：
   - 這通常是透過 iPhone App 和 Gateway 之間的 pairing：
     - iPhone App 連上 `ws://<Mac-mini-ip>:18789`（或 Tailscale IP）
     - 完成 pairing 後，Gateway 那邊會有一個「iOS/Watch node」記錄
4. **在 OpenClaw 設定「哪些事件要 relay 到 Watch」**：
   - 例如：
     - 新的高優先級提醒
     - 某個 cron 任務的短摘要
     - 你手動触發的「發送到手錶」指令

> 目前這些 Watch 相關的 UI / 設定細節沒有完整公開文件，只知道功能有到「收消息 + 簡單指令」。

---

## 3. 可以用來做什麼？（結合我的工作流）

### 3.1 手錶變成「OpenClaw 小小通知中心」

- 例如：
  - 台股量化 cron 推送 → 簡短版本同步到 Watch inbox。
  - 每日 OpenClaw skill survey 結果：在手錶上只顯示「今日有 10 個新 skill 可看」，可以點一下讓 Pi 之後在 Mac 上展開細節。

### 3.2 手錶快速丟「指令」給 Pi

- 用法想像：
  - 在手錶上選擇一個簡單動作：
    - 「記錄當下心情」
    - 「打卡：正在通勤」
    - 「幫我標記這段時間為 deep work」
  - 背後實際是：
    - Watch → iPhone → Gateway → Pi → 寫入 Obsidian（例如 Daily note / Activity log）

### 3.3 與語音 Agent 的未來連動

- 現階段：Watch 主要是內容展示 + 簡易指令。
- 之後如果 WSLC 語音 Agent 完成，可以想像：
  - 手錶上顯示「WSLC 正在處理的語音任務狀態」
  - 快速推送「最近一次語音研究的重點摘要」到 Watch

---

## 4. 實作 TODO（給 Antigravity / 未來我看的）

1. **確認 iPhone / Watch 上的 OpenClaw App 版本**
   - 是否已支援 `2026.2.19` 的 Watch companion。

2. **設計要 push 到 Watch 的事件清單**
   - 台股量化 Tips（cron）
   - OpenClaw Daily Skill Survey 的「今日有幾個候選 skill」
   - 某些高優先級提醒（例如：行事曆 10 分鐘前 / 特殊任務完成）

3. **Pair iPhone App ↔ Mac mini Gateway**
   - 讓 Gateway 上出現 iOS/Watch node，準備後續通知 relay。

4. **在 Obsidian 中規劃 Watch 對應的 Inbox 區塊**
   - 例如：`openclaw/Watch-Inbox/`：
     - 記錄 Watch 收到/觸發的事件（方便事後回顧）。

---

## 5. 小結

- Apple Watch 目前不是「直接跑 OpenClaw」，而是透過：
  - **iPhone App + Watch App + Gateway + APNs** 把 Watch 變成一個「小視窗」。
- 對我來說比較實用的方向：
  - 把重要的 OpenClaw 訊息 / cron 簡報推到手錶。
  - 在手錶上提供少量可控的快速動作（狀態回報 / 簡易指令），由 Pi 接手在 Mac mini 上做真正的工作。