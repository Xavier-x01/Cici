#!/usr/bin/env bash
# Cici preflight / health check — run: bash scripts/doctor.sh
# Prints one paragraph: PASS or the top issue to fix first.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

ISSUES=()

# ── 1. Git ────────────────────────────────────────────────────────────────────
BRANCH=$(git branch --show-current 2>/dev/null || echo "detached")
if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
  GIT_STATUS="clean"
else
  GIT_STATUS="dirty (WIP)"
fi
if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  ISSUES+=("Branch is '$BRANCH' — use a feature branch for active work.")
fi

# ── 2. Config & secrets ───────────────────────────────────────────────────────
if [[ ! -d "config" ]]; then
  ISSUES+=("config/ directory not found.")
fi
if git ls-files | grep -qE '^\.env$'; then
  ISSUES+=(".env is tracked by git — remove it and rotate any exposed keys.")
fi
# Scan tracked files for common token patterns (hex 32+, Bearer tokens)
SECRET_HIT=$(git ls-files | xargs grep -rlE \
  '(SUPABASE_SERVICE_ROLE_KEY|MCP_ACCESS_KEY|sk-[A-Za-z0-9]{20,}|Bearer [A-Za-z0-9+/=]{20,}|[0-9a-f]{64})' \
  --include="*.env" --include="*.json" --include="*.sh" --include="*.ts" \
  2>/dev/null | grep -v ".git" || true)
if [[ -n "$SECRET_HIT" ]]; then
  ISSUES+=("Possible secret in tracked file(s): $SECRET_HIT — verify and rotate if real.")
fi

# ── 3. Proposals queue ────────────────────────────────────────────────────────
OPEN_PROPOSALS=0
if [[ -d "proposals/queue" ]]; then
  OPEN_PROPOSALS=$(find proposals/queue -maxdepth 1 -name "*.json" | wc -l | tr -d ' ')
fi

# ── 4. Build output ───────────────────────────────────────────────────────────
echo ""
echo "══════════════════════ Cici Doctor ══════════════════════"
echo "  Branch   : $BRANCH ($GIT_STATUS)"
echo "  Proposals : $OPEN_PROPOSALS open in proposals/queue/"
echo "═════════════════════════════════════════════════════════"

if [[ ${#ISSUES[@]} -eq 0 ]]; then
  echo ""
  echo "  PASS — repo looks healthy. No blocking issues found."
  echo ""
else
  echo ""
  echo "  FIX FIRST: ${ISSUES[0]}"
  if [[ ${#ISSUES[@]} -gt 1 ]]; then
    echo ""
    echo "  Additional issues (${#ISSUES[@]} total):"
    for i in "${!ISSUES[@]}"; do
      [[ $i -eq 0 ]] && continue
      echo "    [$i] ${ISSUES[$i]}"
    done
  fi
  echo ""
  exit 1
fi
