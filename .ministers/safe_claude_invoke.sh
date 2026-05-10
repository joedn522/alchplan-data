#!/usr/bin/env bash
# safe_claude_invoke.sh — 強制 unset ANTHROPIC_API_KEY 防止偷扣 API
# 用法: ./safe_claude_invoke.sh "<prompt>" [--max-turns N]

set -euo pipefail

# 雙保險：強制走 Max 訂閱，不走 API
unset ANTHROPIC_API_KEY 2>/dev/null || true
unset ANTHROPIC_API_BASE 2>/dev/null || true

MAX_TURNS="${2:-15}"

if [ -z "${1:-}" ]; then
    echo "Usage: $0 '<prompt>' [max-turns]"
    exit 1
fi

exec claude -p "$1" --max-turns "$MAX_TURNS"
