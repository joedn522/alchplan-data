# RingBot 深度研究報告：Pi × Windows 語音架構（實作版）

本文件是給「未來的你」看的實作手冊，描述：
- Pi 留在 **Mac mini** 當唯一大腦
- **Windows + 5080** 負責語音（STT/TTS）
- 兩者透過 HTTP + JSON 溝通
- 保留未來在 Windows 端掛第二顆 LLM 的彈性

---

## 0. 架構一眼看懂

**目前目標版本（精簡模式）：**

> 電話 → Windows/Voice Bridge (STT) → Pi (文字 → 回覆文字) → Windows/Voice Bridge (TTS) → 電話

- Windows：
  - 收音、轉文字（Whisper / faster-whisper）
  - 收 Pi 回覆、轉語音播出
- Pi（Mac mini）：
  - 接收文字請求
  - 使用現有 LLM 能力 + Obsidian + 自動化邏輯產生回覆

**未來升級版（雙大腦模式，先預留 hook）：**

> 電話 → Windows/Bridge → (判斷：簡單 → Windows 本地 LLM；複雜 → Pi)

現在先實作「精簡模式」，但在架構與程式裡預留 `USE_LOCAL_LLM` hook，未來你想在 Windows 跑第二顆 LLM 時可以無痛接上。

---

## 1. Pi 與 Voice Bridge 的通訊協定

### 1.1 協定設計

- Windows → Pi：HTTP `POST /voice_bridge/request`
- Body：JSON

```jsonc
{
  "text": "使用者說的話（已由 STT 轉文字）",
  "source": "windows-voice-bridge",
  "meta": {
    "raw_audio_path": "/tmp/xxx.wav" // 可選
  }
}
```

- Pi → Windows：回傳 JSON

```jsonc
{
  "reply": "Pi 準備給使用者聽的那句話",
  "meta": {
    "intent": "note/research/chat/...", 
    "obsidian_write": {
      "path": "openclaw/daily/2026-02-20.md",
      "append": "- 使用者在車上說：XXX"
    }
  }
}
```

> 後續你要實作 Obsidian 寫入，可以直接讀 `meta.obsidian_write`。

---

## 2. Windows WSL2：Voice Bridge 部署

### 2.1 基本環境（WSL2 裝 Python + Whisper）

```bash
# 更新系統
sudo apt update && sudo apt upgrade -y

# 安裝基本工具 & Python
sudo apt install -y python3 python3-venv python3-pip ffmpeg git curl

# 建 Voice Bridge 專用資料夾
mkdir -p ~/voice-bridge && cd ~/voice-bridge

# 建立 virtualenv
python3 -m venv .venv
source .venv/bin/activate

# 安裝必要套件
pip install faster-whisper torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install fastapi uvicorn[standard] requests
# TTS 相關套件等你決定要用哪一套再裝
```

### 2.2 建立 Voice Bridge 服務程式

> 檔案：`~/voice-bridge/voice_bridge.py`

```python
import tempfile
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
import uvicorn
import os

# ====== 可調整配置 ======
PI_ENDPOINT = os.environ.get(
    "PI_ENDPOINT",
    "http://<MAC_MINI_IP>:18789/voice_bridge/request"  # 之後會在 Mac 開這個 handler
)

MODEL_SIZE = os.environ.get("WHISPER_MODEL", "large-v3")
DEVICE = "cuda"  # 5080 用 GPU
USE_LOCAL_LLM = os.environ.get("USE_LOCAL_LLM", "false").lower() == "true"
# =======================

print(f"Loading Whisper model {MODEL_SIZE} on {DEVICE} ...")
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type="float16")

app = FastAPI(title="Voice Bridge for Pi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def maybe_handle_locally(text: str) -> str | None:
    """預留 hook：未來在 Windows 跑本地 LLM 時可以在這裡先嘗試直接回答。

    現階段直接回傳 None，所有請求都送給 Pi。
    """
    if not USE_LOCAL_LLM:
        return None
    # TODO: 未來你想接 Ollama / DeepSeek，就在這裡呼叫本地 LLM
    return None


@app.post("/stt-and-forward")
async def stt_and_forward(file: UploadFile = File(...)):
    """主入口：
    1) 收到電話錄音 (Twilio / LiveKit webhook 轉來的音訊檔)
    2) 用 faster-whisper 轉文字
    3)（未來）若 USE_LOCAL_LLM：可先在 Windows 嘗試處理
    4) 否則把文字丟給 Pi 的 HTTP endpoint
    5) 回傳 Pi 的 reply，給上一層處理 TTS
    """
    # 將上傳的音訊存到暫存檔
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        audio_path = tmp.name
        content = await file.read()
        tmp.write(content)

    # 1) STT：語音 → 文字
    segments, info = model.transcribe(audio_path, beam_size=5)
    text = "".join(segment.text for segment in segments).strip()

    # 2) （預留）先問問本地 LLM 要不要自己處理
    local_reply = maybe_handle_locally(text)
    if local_reply is not None:
        return {
            "status": "ok",
            "mode": "local-llm",
            "transcript": text,
            "pi_reply": local_reply,
            "pi_meta": {"handled_by": "windows-local-llm"},
        }

    # 3) 傳給 Pi
    payload = {
        "text": text,
        "source": "windows-voice-bridge",
        "meta": {
            "raw_audio_path": audio_path,
        }
    }

    try:
        resp = requests.post(PI_ENDPOINT, json=payload, timeout=60)
        resp.raise_for_status()
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to contact Pi: {e}",
            "partial_transcript": text,
        }

    pi_data = resp.json()
    reply_text = pi_data.get("reply", "")
    return {
        "status": "ok",
        "mode": "pi",
        "transcript": text,
        "pi_reply": reply_text,
        "pi_meta": pi_data.get("meta", {}),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

### 2.3 啟動 Voice Bridge

```bash
cd ~/voice-bridge
source .venv/bin/activate
export PI_ENDPOINT="http://<MAC_MINI_IP>:18789/voice_bridge/request"
# 若未來要啟用本地 LLM： export USE_LOCAL_LLM=true
python voice_bridge.py
# 服務會跑在 http://0.0.0.0:8001
```

> 之後 Twilio / LiveKit 端的語音 webhook 就可以丟音訊檔到這個 `/stt-and-forward`。

---

## 3. Mac mini：Pi Voice Handler（Pi 端 HTTP 入口）

Mac mini 這邊需要有一個 HTTP handler 來接 Voice Bridge 的請求，然後轉交給 Pi 本體（也就是現在這個 assistant）。

這裡給一個「最小可用」版本，你之後可以把裡面呼叫 LLM 的部分換成真正的 OpenClaw/Pi 呼叫。

### 3.1 建立環境

```bash
mkdir -p ~/pi-voice-handler && cd ~/pi-voice-handler
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn requests
```

### 3.2 Handler 實作

> 檔案：`~/pi-voice-handler/handler.py`

```python
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# TODO: 在這裡接入真正的 Pi / OpenClaw 呼叫
# 例如：用 requests 打 OpenClaw Gateway 的 /chat API

class VoiceRequest(BaseModel):
    text: str
    source: str | None = None
    meta: dict | None = None

app = FastAPI(title="Pi Voice Handler")

@app.post("/voice_bridge/request")
async def handle_voice(req: VoiceRequest):
    user_text = req.text

    # === 這裡改成實際丟給 Pi 本體 ===
    # 暫時先用一個示範回覆：
    reply = f"Pi 收到你的語音內容：{user_text}。之後這裡會換成真正的 LLM 回覆與 Obsidian 寫入。"

    return {
        "reply": reply,
        "meta": {
            "handled_by": "pi-voice-handler",
            "note": "之後可以在這裡加上 obsidian write 的具體資訊"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=18789)
```

### 3.3 啟動 Handler

```bash
cd ~/pi-voice-handler
source .venv/bin/activate
python handler.py
# Pi Voice Handler 跑在 http://<Mac-mini-IP>:18789
```

啟動之後，記得回到 Windows 端，把 `PI_ENDPOINT` 指向這個 URL。

---

## 4. Obsidian 同步與命名（重點提醒）

這部分沿用之前的設計，但簡短重申要點：

1. **Vault 命名**：建議所有機器都使用 `asherdb` 當 Vault 資料夾名稱（避免腳本路徑分裂）。
2. **LiveSync 初次設定**：
   - 在 Windows 端建立空的 `asherdb` 資料夾。
   - 用 Obsidian 開啟，安裝 `Self-hosted LiveSync`。
   - 設定 CouchDB 連線後，**務必選「Fetch from Remote」**，讓 Windows 從 NAS 拉資料，而不是推空資料上去。
3. **自動同步**：確認第一次 Fetch 完成後，再開啟自動同步。

---

## 5. 未來：讓 Windows 變第二大腦

你未來如果想讓 Windows 端也跑 LLM：

1. 在 WSL2 安裝 Ollama / DeepSeek：
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama run deepseek-v3
   ```
2. 在 `voice_bridge.py` 裡實作 `maybe_handle_locally(text)`：
   - 用簡單規則判斷：
     - 若只是閒聊或不需要跨系統操作 → 呼叫本地 LLM，直接回覆
     - 若需要查 Obsidian / 呼叫 Gog / 控制 NAS → 把請求轉交 Pi
3. 設環境變數：
   ```bash
   export USE_LOCAL_LLM=true
   ```

這樣整體架構不需要翻修，只是多了一條「Windows 自己先想一想」的支線。

---

## 6. 下一步建議

1. 按照本文件在 **Windows WSL2** 部署 `voice-bridge`。
2. 在 **Mac mini** 上部署 `pi-voice-handler`，確認用 curl 測試互通：
   ```bash
   curl -X POST http://<Mac-mini-IP>:18789/voice_bridge/request \
     -H 'Content-Type: application/json' \
     -d '{"text":"測試","source":"manual"}'
   ```
3. 再用 curl 或簡單工具從 Windows 打 `/stt-and-forward` 測試流程（先用一個小 wav 檔）。

等你實際跑一輪，我們可以再針對「Twilio / LiveKit 入口」寫成第二階段文件。</n