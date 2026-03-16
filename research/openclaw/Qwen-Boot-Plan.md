# Qwen 2.5 Coder 32B 啟動與驗證策略 (Qwen-Boot-Plan)

為了確保從 Gemini 切換到本地 Qwen 大腦能成功，我們將採取「三階段驗證法」，並強化日誌監控。

---

## 📅 第一階段：環境預檢與日誌強化 (Pre-flight)

1. **連通性最終確認**：
   - 執行 `curl -I http://172.23.32.1:11434` 確保沒有防火牆攔截。
2. **開啟追蹤模式**：
   - 我會建議你在切換前，先開啟一個獨立視窗執行 `openclaw logs --follow`，或者我會頻繁讀取 `/tmp/openclaw/openclaw-YYYY-MM-DD.log` 來監控。
3. **記憶體快照**：
   - 確認 RTX 5080 的剩餘 VRAM (目前 2.5GB 已佔用，還有約 13.5GB 可用)。32B 模型如果是 4-bit 量化約需 18-20GB，可能需要確認 Windows 端是否有其他佔用，或是模型是否已正確載入。

---

## 🚀 第二階段：模型切換與「握手測試」 (Handshake)

1. **切換主腦**：
   - 在 Telegram 輸入 `/model ollama/qwen2.5-coder:32b`。
2. **三點基礎驗證**：
   - **(A) 指令響應性**：問一個簡單問題（如：你是誰？），確認 Ollama 回應速度。
   - **(B) 中文處理能力**：確認其繁體中文輸出的流暢度。
   - **(C) Obsidian 權限驗證**：要求 Qwen 列出 `/Research` 資料夾下的前三個檔案，驗證 `read` 工具在 Qwen 下的調用是否正常。

---

## 🔍 第三階段：核心任務驗證 (Capability Test)

1. **筆記理解測試**：
   - 要求 Qwen 讀取並總結 `openclaw/OpenClaw-Intelligence-Hub.md`。
   - **檢驗點**：它是否能正確提取「核心使用情境」？
2. **跨筆記連結測試**：
   - 問它：「根據我的筆記，WSLC 語音代理計劃目前遇到了什麼問題？」
   - **檢驗點**：它是否能主動搜尋 `WSLC-Voice-Agent-Plan.md` 並給出正確答案？
3. **回退機制 (Fallback)**：
   - 若 Qwen 在 30 秒內無回應或報錯，系統應自動回退至 Gemini，我會立刻接手分析失敗原因。

---

## 🛠️ 失敗預判與對策

- **Timeout**：若載入太慢，我會建議調整 Ollama 的 `keep_alive` 時間。
- **Tool Call 格式錯誤**：Qwen 有時會給出格式稍偏的 JSON，我會檢查日誌，必要時調整 `System Prompt` 強化其對 OpenClaw 工具格式的服從度。

*計畫擬定者：筆記本精靈 Antigravity*
