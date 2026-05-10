#!/usr/bin/env python3
"""
AlchPlan 部長公司 — 統一入口
用法:
  python3 run.py voice                    # 跑 Voice 部長
  python3 run.py pm                       # 跑 PM 部長
  python3 run.py knowledge                # 跑 Knowledge 部長
  python3 run.py all                      # 依序跑全部（Voice → PM → Knowledge）
  python3 run.py voice --print-prompt-only # 只印 prompt 不執行
  python3 run.py voice --debug            # debug 模式
  python3 run.py voice --skip-cadence     # 跳過 cadence check
  python3 run.py voice --max-turns 25     # 覆蓋 max-turns
"""

import os
import sys
import json
import subprocess
import argparse
import fcntl
from datetime import datetime, timedelta
from pathlib import Path

# === Config ===
BASE_DIR = Path(__file__).parent.parent  # alchplan-data root
MINISTERS_DIR = BASE_DIR / '.ministers'
SOPS_DIR = MINISTERS_DIR / 'sops'
STATE_DIR = MINISTERS_DIR / 'state'
CHARTER_PATH = MINISTERS_DIR / 'alchplan_charter.md'
SAFE_INVOKE = MINISTERS_DIR / 'safe_claude_invoke.sh'

MINISTER_ORDER = ['voice', 'pm', 'knowledge']  # knowledge 必須最後
DEFAULT_MAX_TURNS = 15

MINISTER_CONFIG = {
    'voice': {
        'sop': 'minister_voice.md',
        'state': 'voice.json',
        'min_cadence_hours': 0,
        'max_turns': 20,
    },
    'pm': {
        'sop': 'minister_pm.md',
        'state': 'pm.json',
        'min_cadence_hours': 0,
        'max_turns': 15,
    },
    'knowledge': {
        'sop': 'minister_knowledge.md',
        'state': 'knowledge.json',
        'min_cadence_hours': 0,
        'max_turns': 15,
    },
}


def get_circle_id():
    """產生今天的 Circle ID"""
    today = datetime.now().strftime('%Y%m%d')
    circles_dir = MINISTERS_DIR / 'circles'
    existing = [f.name for f in circles_dir.glob(f'circle_{today}_C*.md')]
    next_num = len(existing) + 1
    return f'{today}_C{next_num:03d}'


def check_env():
    """安全檢查：確保不會偷扣 API"""
    if os.environ.get('ANTHROPIC_API_KEY'):
        print('❌ ANTHROPIC_API_KEY is set! Refusing to run.')
        print('   This would charge your API account instead of using Max subscription.')
        print('   Run: unset ANTHROPIC_API_KEY')
        sys.exit(1)


def check_cadence(minister_name, skip=False):
    """檢查部長是否到了該跑的時間"""
    if skip:
        return True
    config = MINISTER_CONFIG[minister_name]
    state_path = STATE_DIR / config['state']
    if not state_path.exists():
        return True  # 從沒跑過

    state = json.loads(state_path.read_text())
    last_id = state.get('last_circle_id')
    if not last_id:
        return True

    # 簡單檢查：同一天只跑一次（除非 skip-cadence）
    today = datetime.now().strftime('%Y%m%d')
    if last_id.startswith(today):
        print(f'⏭  {minister_name} 今天已跑過 ({last_id})，跳過')
        return False
    return True


def build_prompt(minister_name, circle_id):
    """組裝 prompt：章程 + SOP + state + circle_id"""
    config = MINISTER_CONFIG[minister_name]

    parts = []

    # 1. 章程
    parts.append('# === 章程（最高指導原則） ===\n')
    parts.append(CHARTER_PATH.read_text(encoding='utf-8'))
    parts.append('\n\n')

    # 2. SOP
    sop_path = SOPS_DIR / config['sop']
    parts.append('# === 你的 SOP ===\n')
    parts.append(sop_path.read_text(encoding='utf-8'))
    parts.append('\n\n')

    # 3. State
    state_path = STATE_DIR / config['state']
    parts.append('# === 你的 State（上次狀態） ===\n')
    parts.append('```json\n')
    parts.append(state_path.read_text(encoding='utf-8'))
    parts.append('\n```\n\n')

    # 4. Inbox preview (for PM and Knowledge)
    inbox_path = BASE_DIR / 'system' / 'pm_tasks.json'
    if inbox_path.exists():
        parts.append('# === PM Inbox 現況 ===\n')
        parts.append('```json\n')
        parts.append(inbox_path.read_text(encoding='utf-8'))
        parts.append('\n```\n\n')

    # 5. 執行指令
    parts.append(f'# === 執行指令 ===\n')
    parts.append(f'Circle ID: {circle_id}\n')
    parts.append(f'部長: {minister_name}\n')
    parts.append(f'時間: {datetime.now().isoformat()}\n')
    parts.append(f'工作目錄: {BASE_DIR}\n\n')
    parts.append('請按照 SOP 的步驟順序執行。\n')
    parts.append('所有檔案路徑都相對於工作目錄。\n')
    parts.append(f'Newsletter 輸出到: .ministers/newsletters/{minister_name}_{circle_id}.md\n')
    parts.append('完成後用 git commit + push 持久化。\n')

    return ''.join(parts)


def run_pre_scripts(minister_name, circle_id):
    """Voice 部長的前置腳本：先跑 Whisper 轉錄再啟動 claude -p"""
    if minister_name != 'voice':
        return None  # 其他部長不需要前置腳本

    print('📼 Voice 前置：執行 Whisper 轉錄腳本...')
    script = MINISTERS_DIR / 'scripts' / 'voice_transcribe.py'
    try:
        result = subprocess.run(
            ['powershell.exe', '-Command', f'python "{script}"'],
            capture_output=True, text=True,
            timeout=1800,  # 30 min for Whisper
        )
        stderr_lines = result.stderr.strip()
        if stderr_lines:
            print(f'   {stderr_lines}')

        stdout = result.stdout.strip()
        if stdout:
            import json as _json
            try:
                data = _json.loads(stdout)
                n = len(data.get('transcribed', []))
                f = len(data.get('failed', []))
                print(f'   ✅ 轉錄完成：{n} 成功, {f} 失敗')
                return stdout  # JSON string to inject into prompt
            except:
                print(f'   ⚠️ 腳本輸出非 JSON: {stdout[:200]}')
                return stdout
        else:
            print('   ℹ️ 無新錄音')
            return '{"new_found": 0, "transcribed": [], "failed": []}'

    except subprocess.TimeoutExpired:
        print('   ⏰ 轉錄腳本超時（30分鐘）')
        return '{"error": "timeout"}'
    except Exception as e:
        print(f'   ❌ 轉錄腳本失敗: {e}')
        return f'{{"error": "{e}"}}'


def run_minister(minister_name, circle_id, args):
    """執行一個部長"""
    config = MINISTER_CONFIG[minister_name]
    max_turns = args.max_turns or config.get('max_turns', DEFAULT_MAX_TURNS)

    print(f'\n{"="*60}')
    print(f'🏛  {minister_name.upper()} 部長啟動 — Circle {circle_id}')
    print(f'{"="*60}\n')

    # Run pre-scripts (Voice minister: Whisper transcription)
    pre_result = run_pre_scripts(minister_name, circle_id)

    # Build prompt
    prompt = build_prompt(minister_name, circle_id)

    # Inject pre-script result into prompt for Voice minister
    if pre_result and minister_name == 'voice':
        prompt += f'\n# === 轉錄腳本已執行完畢，結果如下 ===\n'
        prompt += f'```json\n{pre_result}\n```\n\n'
        prompt += '轉錄腳本已幫你完成 Step 1。請從 Step 2 (git 持久化) 開始執行。\n'

    if args.print_prompt_only:
        print(prompt)
        return True

    # File lock to prevent duplicate runs
    lock_path = STATE_DIR / f'.{minister_name}.lock'
    lock_file = open(lock_path, 'w')
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print(f'⚠️  {minister_name} 已在執行中（lock file exists），跳過')
        return False

    try:
        # Run claude -p via safe wrapper
        cmd = ['bash', str(SAFE_INVOKE), prompt, str(max_turns)]

        if args.debug:
            print(f'[DEBUG] Command: {" ".join(cmd[:2])} "<prompt>" {max_turns}')
            print(f'[DEBUG] Prompt length: {len(prompt)} chars')

        result = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=600,  # 10 min timeout per minister
        )

        print(result.stdout)
        if result.stderr:
            print(f'[STDERR] {result.stderr}', file=sys.stderr)

        if result.returncode != 0:
            print(f'❌ {minister_name} 執行失敗 (exit code {result.returncode})')
            return False

        print(f'✅ {minister_name} 完成')
        return True

    except subprocess.TimeoutExpired:
        print(f'⏰ {minister_name} 超時（10分鐘），強制結束')
        return False
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()
        lock_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description='AlchPlan 部長公司 — 統一入口')
    parser.add_argument('minister', choices=['voice', 'pm', 'knowledge', 'all'],
                        help='要執行的部長（或 all 依序全跑）')
    parser.add_argument('--print-prompt-only', action='store_true',
                        help='只印 prompt 不執行')
    parser.add_argument('--debug', action='store_true',
                        help='Debug 模式')
    parser.add_argument('--skip-cadence', action='store_true',
                        help='跳過 cadence 檢查')
    parser.add_argument('--max-turns', type=int, default=None,
                        help='覆蓋 max-turns')

    args = parser.parse_args()

    # Safety check
    check_env()

    # Circle ID
    circle_id = get_circle_id()
    print(f'📋 Circle ID: {circle_id}')
    print(f'📁 Working dir: {BASE_DIR}')

    # Determine which ministers to run
    if args.minister == 'all':
        ministers = MINISTER_ORDER
    else:
        ministers = [args.minister]

    # Run
    results = {}
    for name in ministers:
        if not check_cadence(name, skip=args.skip_cadence):
            results[name] = 'skipped'
            continue

        success = run_minister(name, circle_id, args)
        results[name] = 'success' if success else 'failed'

    # Summary
    print(f'\n{"="*60}')
    print(f'📊 Circle {circle_id} 執行結果')
    print(f'{"="*60}')
    for name, status in results.items():
        icon = {'success': '✅', 'failed': '❌', 'skipped': '⏭'}[status]
        print(f'  {icon} {name}: {status}')


if __name__ == '__main__':
    main()
