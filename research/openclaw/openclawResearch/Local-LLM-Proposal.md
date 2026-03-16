# 本地 LLM 部署提案 (WSL2 + 128GB RAM + RTX 5080)

## 1. 專案概述
本提案旨在利用使用者強大的運算環境（128GB RAM, RTX 5080），在本地部署大型語言模型 (LLM)，以強化 **OpenClaw** 自動化生態系與 **Obsidian** 人生紀錄系統。

## 2. 核心使用情境

### A. 隱私優先的個人 RAG (Obsidian 大腦)
- **概念**：使用本地 LLM 索引並查詢整個 `asherdb` 庫。
- **實作**：透過 `Smart Connections` 插件或自定義 OpenClaw 技能，將 `Ollama` 或 `LM Studio` 連接到 Obsidian。
- **優點**：在獲得 AI 檢索能力的同時，確保私人日記、專案筆記與敏感紀錄絕不外洩。
- **推薦模型**：`Llama-3-70B-Instruct` (量化版) 或 `Qwen-2.5-32B`。

### B. 智慧語音後處理 (Whisper 處理器)
- **概念**：自動化結構處理與摘要由 Whisper 轉錄的音檔。
- **實作**：監控 `Voice-Inbox/` 資料夾中的新 `.md` 檔案，觸發本地 LLM 提取待辦事項 (TODO) 與摘要。
- **優點**：無需雲端成本或延遲，即可將原始想法轉化為可執行的任務。

### C. 安全編碼與台股量化分析
- **概念**：用於 Python 回測腳本與財經情緒分析的本地 AI 助手。
- **實作**：在 WSL2 中透過 `Continue.dev` 使用 `DeepSeek-Coder-V2`。
- **優點**：防止專有交易策略與程式邏輯外流至外部 API。

### D. OpenClaw 「隱私衛士」層
- **概念**：作為 OpenClaw 預處理器的本地模型。
- **實作**：OpenClaw 將敏感數據（金鑰、路徑）先發送到本地 LLM 進行去敏感化處理或本地執行。
- **優點**：結合了 Gemini/Claude 的推理能力與本地節點的安全安全性。

## 3. 硬體優化策略
- **VRAM (GPU)**：優先用於 14B-20B 參數以下模型的高速推理。
- **RAM (CPU Offloading)**：利用 128GB 的超大容量，透過 `llama.cpp` 的部分 GPU 卸載 (Offloading) 技術運行 70B 以上的重型模型。

## 4. 後續步驟
- [ ] 在 WSL2 上安裝 Ollama。
- [ ] 測試 Llama-3-70B 在 GPU 卸載模式下的效能表現。
- [ ] 透過新的 `local-llm` 技能將本地端點與 OpenClaw 整合。

---
*Pi (OpenClaw) 產於 2026-02-22*
