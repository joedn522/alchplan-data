# Qwen 2.5 遷移與驗證計畫 v2.0 (Windows Host 版)

由於目前決定將 Ollama 引擎運行於 Windows 宿主機，以實現多環境共享 5080 效能，本計畫旨在確保連線打通並平穩遷移。

---

## 🛠️ 第一階段：物理連線驗證 (The Bridge)
**目標：確保 WSL 真的能「看到」 Windows 上的 Ollama。**

1. **宿主機狀態檢查**：
   - 確保 Windows Ollama 已啟動（右下角有小羊駝）。
   - 確保 Windows 已下載模型：`ollama pull qwen2.5-coder:32b`。
2. **網路連線測試**：
   - 我會反覆測試 `curl http://172.23.32.1:11434/api/tags`。
   - **如果失敗**：我會引導你確認 Windows 端 `OLLAMA_HOST` 是否真的生效（需重啟電腦或 Ollama 程式）。

---

## 🚀 第二階段：配置遷移 (The Migration)
**目標：正式修改 WSLC 內部的神經連結。**

1. **更新 `openclaw.json`**：
   - 將 `baseUrl` 指向 `http://172.23.32.1:11434`。
   - 將 `primary` 模型設定為 `ollama/qwen2.5-coder:32b`。
2. **重啟 Gateway**：
   - 執行 `openclaw gateway restart` 確保新配置生效。

---

## 🔍 第三階段：冒煙測試 (Smoke Test)
**目標：確認 Qwen 是否正常說話且能讀取筆記。**

1. **身份確認**：
   - `/model` 切換後，問它：「請自我介紹，並告訴我你目前運行在哪張顯卡上？」
   - **檢驗點**：它應該要能說出自己是 Qwen，且如果你筆記有寫 5080，它應能關聯到。
2. **Obsidian 存取壓力測試**：
   - 要求它：「讀取 `openclaw/Qwen-Boot-Plan.md` 並給我三個具體的修改建議。」
   - **檢驗點**：這能同時測試「讀取工具」與「邏輯推理」是否在 Qwen 上運作正常。

---

## ⚠️ 失敗回退機制 (Fallback)
- 如果 Qwen 回應超過 20 秒，或出現 `Connection Refused`。
- **動作**：我會自動執行指令切換回 `gemini-3-flash`，並將錯誤日誌存入 Obsidian 供你查閱。

*計畫擬定者：你的筆記本精靈 (Antigravity)*
