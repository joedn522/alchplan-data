r"""
Voice 部長專用轉錄腳本
Batch transcribe Just Press Record → alchplan-data/bujo/voice-inbox/
輸出 JSON 結果到 stdout 供 Voice 部長讀取。

用法（必須用 Windows Python 跑，因為 Whisper + CUDA）:
  powershell.exe -Command "python C:\Users\ashershih\Documents\alchplan-data\.ministers\scripts\voice_transcribe.py"
"""
import os
import sys
import json
import whisper
from datetime import datetime

ICLOUD_DIR = r"C:\Users\ashershih\iCloudDrive\iCloud~com~openplanetsoftware~just-press-record"
VOICE_INBOX = r"C:\Users\ashershih\Documents\alchplan-data\bujo\voice-inbox"
STATE_FILE = r"C:\Users\ashershih\Documents\alchplan-data\.ministers\state\voice.json"
START_DATE = "2026-03-12"


def get_existing_originals():
    existing = set()
    for fname in os.listdir(VOICE_INBOX):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(VOICE_INBOX, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('original_file:'):
                        existing.add(line.strip().split(':', 1)[1].strip())
                    if line.startswith('---') and len(existing) > 0:
                        break
        except:
            pass
    return existing


def collect_new_files(existing_originals):
    new_files = []
    for folder_name in sorted(os.listdir(ICLOUD_DIR), reverse=True):
        if not folder_name.startswith('2026-'):
            continue
        if folder_name < START_DATE:
            continue
        folder_path = os.path.join(ICLOUD_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue
        for fname in sorted(os.listdir(folder_path), reverse=True):
            if not fname.lower().endswith(('.m4a', '.wav', '.mp3')):
                continue
            if fname in existing_originals:
                continue
            new_files.append((folder_name, fname, os.path.join(folder_path, fname)))
    return new_files


def transcribe_and_save(model, date_str, original_file, audio_path):
    result = model.transcribe(audio_path, language="zh", task="transcribe", verbose=False)
    text = result.get("text", "").strip()
    if not text:
        return None, 0

    title = text[:40].replace('\n', ' ').strip()
    if len(text) > 40:
        title += '...'

    time_part = original_file.replace('.m4a', '').replace('.wav', '').replace('.mp3', '')
    time_clean = time_part.replace('-', '')

    md_filename = f"{date_str} - {title} ({time_clean}).md"
    for ch in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
        md_filename = md_filename.replace(ch, '')

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""---
date: {date_str}
source: Just Press Record
original_file: {original_file}
type: voice-transcript
---

# 🎙️ 語音轉錄: {title}

> 轉錄日期: {now}

## 轉錄內容
{text}

---
#voice-inbox #justpressrecord
"""
    out_path = os.path.join(VOICE_INBOX, md_filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return f"{date_str}/{original_file}", len(text)


def main():
    # Collect
    existing = get_existing_originals()
    new_files = collect_new_files(existing)

    result = {
        "scan_date": datetime.now().strftime("%Y-%m-%d"),
        "new_found": len(new_files),
        "transcribed": [],
        "failed": [],
        "total_chars": 0,
    }

    if not new_files:
        # Output JSON to stdout
        print(json.dumps(result, ensure_ascii=False))
        return

    # Load model
    print("Loading Whisper...", file=sys.stderr)
    model = whisper.load_model("large-v3", device="cuda")
    print("Model loaded.", file=sys.stderr)

    for i, (date_str, original_file, audio_path) in enumerate(new_files):
        print(f"[{i+1}/{len(new_files)}] {date_str}/{original_file}", file=sys.stderr)
        try:
            file_id, chars = transcribe_and_save(model, date_str, original_file, audio_path)
            if file_id:
                result["transcribed"].append(file_id)
                result["total_chars"] += chars
            else:
                result["failed"].append({"file": f"{date_str}/{original_file}", "error": "empty transcription"})
        except Exception as e:
            result["failed"].append({"file": f"{date_str}/{original_file}", "error": str(e)})

    # Update state file
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except:
        state = {"processed_files": [], "total_transcribed": 0}

    state["last_scan_date"] = result["scan_date"]
    state["processed_files"].extend(result["transcribed"])
    state["total_transcribed"] = state.get("total_transcribed", 0) + len(result["transcribed"])
    state["failed_files"] = [f["file"] for f in result["failed"]]
    state["errors_this_cycle"] = [f["error"] for f in result["failed"]]

    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Output JSON result to stdout (for Voice minister to read)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
