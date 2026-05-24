r"""
Voice Daemon — 監聽 iCloud Just Press Record → Whisper 轉錄 → 寫入 voice-inbox → git push
這不是部長，是一個獨立 daemon。有新錄音就立刻處理。

用法（Windows Python，因為 Whisper + CUDA）:
  python voice_daemon.py              # 前台跑
  python voice_daemon.py --once       # 掃一次就結束（適合 cron）
  python voice_daemon.py --interval 60  # 每 60 秒掃一次（預設 30）

這個腳本設計為由 Windows Task Scheduler 或手動啟動。
"""
import os
import sys
import re
import json
import time
import subprocess
import argparse
import logging
from datetime import datetime
from pathlib import Path

# === Config ===
ICLOUD_DIR = r"C:\Users\ashershih\iCloudDrive\iCloud~com~openplanetsoftware~just-press-record"
ALCHPLAN_DATA = r"C:\Users\ashershih\Documents\alchplan\alchplan-data"
VOICE_INBOX = os.path.join(ALCHPLAN_DATA, "bujo", "voice-inbox")
STATE_FILE = os.path.join(ALCHPLAN_DATA, ".ministers", "state", "voice.json")
START_DATE = "2026-03-12"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [VoiceDaemon] %(message)s',
    datefmt='%H:%M:%S',
)
log = logging.getLogger('voice_daemon')

# Whisper model (lazy load)
_model = None

def get_model():
    global _model
    if _model is None:
        import whisper
        log.info("Loading Whisper large-v3 on CUDA...")
        _model = whisper.load_model("large-v3", device="cuda")
        log.info("Model loaded.")
    return _model


def load_state():
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            "last_scan_date": None,
            "processed_files": [],
            "failed_files": [],
            "total_transcribed": 0,
        }


def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_existing_originals():
    existing = set()
    for fname in os.listdir(VOICE_INBOX):
        if not fname.endswith('.md'):
            continue
        # Primary: check frontmatter original_file (daemon-generated files)
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
        # Fallback: extract time code from filename pattern "(HHMMSS).md"
        # Covers legacy transcripts that have no frontmatter
        m = re.search(r'\((\d{6})\)\.md$', fname)
        if m:
            t = m.group(1)
            existing.add(f"{t[:2]}-{t[2:4]}-{t[4:]}.m4a")
    return existing


def find_new_files(existing_originals):
    new_files = []
    if not os.path.exists(ICLOUD_DIR):
        log.warning(f"iCloud dir not found: {ICLOUD_DIR}")
        return new_files

    for folder_name in sorted(os.listdir(ICLOUD_DIR), reverse=True):
        if not folder_name.startswith('2026-') and not folder_name.startswith('2025-'):
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


def transcribe_one(model, date_str, original_file, audio_path):
    result = model.transcribe(audio_path, language="zh", task="transcribe", verbose=False)
    text = result.get("text", "").strip()
    if not text:
        return None

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

    return md_filename


def git_push(files_added):
    """git add + commit + push"""
    if not files_added:
        return

    try:
        os.chdir(ALCHPLAN_DATA)
        subprocess.run(['git', 'add', 'bujo/voice-inbox/', '.ministers/state/voice.json'],
                       check=True, capture_output=True)
        msg = f"voice-daemon: 轉錄 {len(files_added)} 則新錄音"
        subprocess.run(['git', 'commit', '-m', msg],
                       check=True, capture_output=True)
        # pull --rebase first to avoid conflicts
        subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'],
                       capture_output=True)
        result = subprocess.run(['git', 'push', 'origin', 'main'],
                                capture_output=True, text=True)
        if result.returncode == 0:
            log.info(f"Git push OK — {len(files_added)} files")
        else:
            log.error(f"Git push failed: {result.stderr}")
    except subprocess.CalledProcessError as e:
        log.error(f"Git error: {e}")


def scan_and_process():
    """掃一次，處理所有新錄音"""
    existing = get_existing_originals()
    new_files = find_new_files(existing)

    if not new_files:
        return 0

    log.info(f"Found {len(new_files)} new recordings")
    model = get_model()

    state = load_state()
    processed = []

    for i, (date_str, original_file, audio_path) in enumerate(new_files):
        log.info(f"[{i+1}/{len(new_files)}] {date_str}/{original_file}")
        try:
            md_name = transcribe_one(model, date_str, original_file, audio_path)
            if md_name:
                processed.append(f"{date_str}/{original_file}")
                log.info(f"  ✅ {md_name}")
            else:
                log.warning(f"  ⚠️ Empty transcription, skipped")
                state.setdefault("failed_files", []).append(f"{date_str}/{original_file}")
        except Exception as e:
            log.error(f"  ❌ {e}")
            state.setdefault("failed_files", []).append(f"{date_str}/{original_file}")

    # Update state
    state["last_scan_date"] = datetime.now().strftime("%Y-%m-%d")
    state["processed_files"] = state.get("processed_files", []) + processed
    state["total_transcribed"] = state.get("total_transcribed", 0) + len(processed)
    save_state(state)

    # Git push
    git_push(processed)

    return len(processed)


def main():
    parser = argparse.ArgumentParser(description='Voice Daemon — 監聽錄音 → 轉錄 → push')
    parser.add_argument('--once', action='store_true', help='掃一次就結束')
    parser.add_argument('--interval', type=int, default=30, help='掃描間隔（秒），預設 30')
    args = parser.parse_args()

    log.info(f"Voice Daemon 啟動")
    log.info(f"  iCloud: {ICLOUD_DIR}")
    log.info(f"  Output: {VOICE_INBOX}")
    log.info(f"  Mode: {'single scan' if args.once else f'watch (every {args.interval}s)'}")

    if args.once:
        n = scan_and_process()
        log.info(f"Done. Processed {n} files.")
        return

    # Daemon loop
    while True:
        try:
            n = scan_and_process()
            if n > 0:
                log.info(f"Cycle done — {n} new files processed")
        except Exception as e:
            log.error(f"Scan error: {e}")

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
