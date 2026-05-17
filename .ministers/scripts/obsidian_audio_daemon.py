r"""
Obsidian Audio Daemon — 監聽 Alchplan vault 新錄音 → Whisper 轉錄 → append 回原 note

設計原則：
- 音檔放在哪個資料夾 = topic context（LeetCode/ = leetcode，daily/ = 日記）
- 掃描哪個 .md 裡有 ![[audio.m4a]] → 找到 parent note → append 逐字稿
- 找不到 parent note → 在同一個資料夾建一個同名 .md

用法：
  python obsidian_audio_daemon.py           # 持續 daemon（每 30 秒掃）
  python obsidian_audio_daemon.py --once    # 掃一次就結束
  python obsidian_audio_daemon.py --interval 60  # 每 60 秒掃
"""

import os
import re
import sys
import json
import time
import logging
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# === Config ===
ALCHPLAN_VAULT = r"C:\Users\ashershih\iCloudDrive\iCloud~md~obsidian\Alchplan"
ALCHPLAN_DATA  = r"C:\Users\ashershih\Documents\alchplan-data"
STATE_FILE     = os.path.join(ALCHPLAN_DATA, ".ministers", "state", "obsidian.json")
TRANSCRIBED_MARKER = "<!-- obsidian-audio-transcribed -->"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [ObsidianDaemon] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("obsidian_daemon")

_model = None

def get_model():
    global _model
    if _model is None:
        import whisper
        log.info("Loading Whisper large-v3 on CUDA...")
        _model = whisper.load_model("large-v3", device="cuda")
        log.info("Model loaded.")
    return _model


# === State ===

def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"processed_files": [], "total_transcribed": 0, "last_scan_date": None}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


# === Discovery ===

def get_processed_set():
    state = load_state()
    return set(state.get("processed_files", []))

def find_new_audio_files():
    """Walk Alchplan vault for .m4a files not yet processed."""
    processed = get_processed_set()
    new_files = []
    vault = Path(ALCHPLAN_VAULT)
    for path in vault.rglob("*.m4a"):
        if any(part.startswith(".") for part in path.parts):
            continue
        rel = str(path.relative_to(vault))
        if rel not in processed:
            new_files.append(path)
    return new_files


def find_parent_note(audio_path: Path) -> Path | None:
    """
    Search all .md files in vault for ![[audio_filename]] embed.
    Returns the path of the first match.
    """
    filename = audio_path.name
    vault = Path(ALCHPLAN_VAULT)
    pattern = re.compile(r"!\[\[" + re.escape(filename) + r"\]\]")
    for md in vault.rglob("*.md"):
        if any(part.startswith(".") for part in md.parts):
            continue
        try:
            content = md.read_text(encoding="utf-8")
            if pattern.search(content):
                return md
        except:
            pass
    return None


def get_context(audio_path: Path, parent_note: Path | None) -> str:
    """
    Derive human-readable context from folder position + note title.
    e.g. audio_path = .../LeetCode/Two Sum/recording.m4a
         → context = "LeetCode / Two Sum"
    """
    vault = Path(ALCHPLAN_VAULT)
    rel = audio_path.relative_to(vault)
    parts = list(rel.parts[:-1])  # exclude filename itself

    if not parts:
        topic = "inbox"
    else:
        topic = " / ".join(parts)

    if parent_note:
        note_stem = parent_note.stem
        # If note name not already in topic, append
        if note_stem not in topic:
            topic = f"{topic} / {note_stem}"

    return topic


# === Transcription + Write-back ===

def transcribe(model, audio_path: Path) -> str:
    result = model.transcribe(str(audio_path), language="zh", task="transcribe", verbose=False)
    return result.get("text", "").strip()


def is_hallucination(text: str) -> bool:
    """Heuristic: very short or contains known Whisper hallucination patterns."""
    if len(text) < 5:
        return True
    hallucinations = ["请不吝点赞", "字幕志愿者", "法定人數不足", "響鐘響鐘"]
    return any(h in text for h in hallucinations)


def append_transcription_to_note(note_path: Path, audio_filename: str, transcript: str, context: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    block = (
        f"\n\n---\n"
        f"### 🎙️ 語音轉錄（{now}）\n"
        f"*{context}*\n\n"
        f"{transcript}\n\n"
        f"{TRANSCRIBED_MARKER}\n"
    )
    with open(note_path, "a", encoding="utf-8") as f:
        f.write(block)
    log.info(f"  Appended to: {note_path.name}")


def create_standalone_note(audio_path: Path, transcript: str, context: str) -> Path:
    """No parent note — create a sibling .md file."""
    note_path = audio_path.with_suffix(".md")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = (
        f"# {audio_path.stem}\n\n"
        f"*錄音時間：{now}*  \n"
        f"*Context：{context}*\n\n"
        f"---\n\n"
        f"{transcript}\n\n"
        f"{TRANSCRIBED_MARKER}\n"
    )
    note_path.write_text(content, encoding="utf-8")
    log.info(f"  Created note: {note_path.name}")
    return note_path


# === Git Push ===

def git_push(files_touched):
    if not files_touched:
        return
    try:
        os.chdir(ALCHPLAN_VAULT)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        msg = f"obsidian-daemon: 轉錄 {len(files_touched)} 則語音"
        subprocess.run(["git", "commit", "-m", msg], check=True, capture_output=True)
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], capture_output=True)
        result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
        if result.returncode == 0:
            log.info(f"Git push OK — {len(files_touched)} notes updated")
        else:
            log.warning(f"Git push skipped (vault may not be a git repo): {result.stderr[:100]}")
    except Exception as e:
        log.warning(f"Git step skipped: {e}")


# === Main Scan ===

def scan_and_process():
    new_files = find_new_audio_files()
    if not new_files:
        return 0

    log.info(f"Found {len(new_files)} new audio file(s)")
    model = get_model()
    state = load_state()
    processed = []
    files_touched = []

    for i, audio_path in enumerate(new_files):
        vault = Path(ALCHPLAN_VAULT)
        rel = str(audio_path.relative_to(vault))
        log.info(f"[{i+1}/{len(new_files)}] {rel}")

        try:
            transcript = transcribe(model, audio_path)
            if not transcript or is_hallucination(transcript):
                log.warning(f"  ⚠️ Empty or hallucination — skipped")
                state.setdefault("failed_files", []).append(rel)
                processed.append(rel)
                continue

            parent_note = find_parent_note(audio_path)
            context = get_context(audio_path, parent_note)

            if parent_note:
                append_transcription_to_note(parent_note, audio_path.name, transcript, context)
                files_touched.append(str(parent_note))
            else:
                note = create_standalone_note(audio_path, transcript, context)
                files_touched.append(str(note))

            processed.append(rel)
            log.info(f"  ✅ [{context}]")

        except Exception as e:
            log.error(f"  ❌ {e}")
            state.setdefault("failed_files", []).append(rel)

    state["processed_files"] = list(set(state.get("processed_files", []) + processed))
    state["total_transcribed"] = state.get("total_transcribed", 0) + len(processed)
    state["last_scan_date"] = datetime.now().strftime("%Y-%m-%d")
    save_state(state)

    git_push(files_touched)
    return len(processed)


def main():
    parser = argparse.ArgumentParser(description="Obsidian Audio Daemon")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--interval", type=int, default=30)
    args = parser.parse_args()

    log.info(f"Obsidian Audio Daemon 啟動")
    log.info(f"  Vault: {ALCHPLAN_VAULT}")
    log.info(f"  Mode: {'single scan' if args.once else f'watch every {args.interval}s'}")

    if args.once:
        n = scan_and_process()
        log.info(f"Done. Processed {n} file(s).")
        return

    while True:
        try:
            n = scan_and_process()
            if n > 0:
                log.info(f"Cycle done — {n} new file(s) transcribed")
        except Exception as e:
            log.error(f"Scan error: {e}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
