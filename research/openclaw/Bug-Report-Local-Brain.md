# OpenClaw 本地大腦 Bug 整理報告 (2026-02-22)

這份報告整理了目前 WSLC 環境中，本地大腦 (RTX 5080 / Qwen 2.5 Coder 32B) 與 OpenClaw 系統遇到的核心問題與 Bug。

---

## 🔴 1. 核心配對失敗 (Auth/Pairing Issue)
**狀態：阻斷級**
- **現象**：日誌中持續出現 `pairing required` (code 1008) 錯誤。
- **原因**：Windows 主機 (`172.23.32.1`) 嘗試連接 WSL Gateway 時驗證失敗。
- **影響**：導致 Mac mini 或 Windows 端無法正確將 WSLC 作為 Node 進行操控，目前 WSLC 處於孤島狀態。

## 🟠 2. Ollama 連通性問題 (Connectivity)
**狀態：警告**
- **現象**：WSL 內部無法透過 `127.0.0.1:11434` 存取 Ollama。
- **原因**：WSL2 的 `127.0.0.1` 指向容器本身，而非 Windows 宿主機。
- **建議**：應將 `openclaw.json` 中的 Ollama `baseUrl` 改為宿主機 IP (`172.23.32.1`) 或使用 `$(hostname).local`。

## 🟠 3. 上下文窗口限制 (Context Window Cap)
**狀態：警告**
- **現象**：系統偵測到 Qwen 32B 的 context window 僅為 20k，低於設定的 32k (`warn<32000`)。
- **影響**：處理長筆記或複雜任務時，可能會發生截斷。

## 🟡 4. 安全性配置風險 (Security Audit)
**狀態：需優化**
- **現象**：Security Audit 報告指出 32B 模型屬於「小模型」，但在未開啟沙箱 (`sandbox=off`) 的情況下啟用了聯網工具。
- **風險**：可能導致模型誤執行危險的 Web 指令。

## 🔵 5. 語音服務 (Whisper) 配置
**狀態：待驗證**
- **路徑**：`/home/wsl/whisper-bin/whisper_service.py`
- **說明**：目前設定使用自定義 Python 腳本調用 5080 進行 STT。需要確保該 venv 環境與 GPU 調用正常。

---

## 🛠️ 建議行動方案 (Next Steps)
1. **修正配對**：手動在 Windows 端執行 `openclaw pairing` 流程，或暫時放寬 Gateway 的 auth 限制。
2. **更新配置**：修改 `~/.openclaw/openclaw.json` 中的 Ollama 地址。
3. **環境測試**：執行 `ollama list` 並確認 5080 的 VRAM 分配情況。
