#!/usr/bin/env bash
# Удаление из ИСТОРИИ git файлов с открытыми паролями и текстом инструкции.
#
#   ./tools/purge_history.sh          # показать план
#   ./tools/purge_history.sh --yes    # выполнить (перезапишет ветку main!)
#
# Удаляются: архив workspace-*.zip, arena_manual/users.json,
#            Таблица_логинов_и_паролей.xlsx, PDF/PPTX в открытом виде,
#            arena_web/, arena_manual/build_html_app.py.
# ВАЖНО: делайте это ДО включения branch protection (force-push будет отклонён).
# После перезаписи всем, у кого была старая копия репозитория, нужно клонировать
# его заново, а рабочую ветку Arena (arena/...) — пересоздать.
set -euo pipefail

cd "$(dirname "$0")/.."
BRANCH="${BRANCH:-main}"

PATHS=(
  'workspace-*.zip'
  'arena_manual/users.json'
  'arena_manual/build_html_app.py'
  'arena_web'
  'Таблица_логинов_и_паролей.xlsx'
  'Инструкция_по_работе_с_AI_Arena.pdf'
  'Instrukcja_pracy_z_AI_Arena_PL.pdf'
  'Презентация_AI_Arena_Agent_Mode.pptx'
  'Презентация_AI_Arena_Agent_Mode_protected.pdf'
)

echo "Ветка: $BRANCH"
echo "Будут удалены из ВСЕЙ истории:"
printf '  - %s\n' "${PATHS[@]}"
echo
echo "Текущие коммиты:"
git log --oneline -5 "$BRANCH" || true

if [ "${1:-}" != "--yes" ]; then
  cat <<'EOT'

Это был план. Для выполнения:
    ./tools/purge_history.sh --yes

Перед запуском: сделайте резервную копию (git clone --mirror) и убедитесь, что
branch protection выключен.
EOT
  exit 0
fi

read -r -p "Точно перезаписать историю ветки $BRANCH? (введите ДА): " ok
[ "$ok" = "ДА" ] || { echo "отменено"; exit 1; }

echo "Резервная копия в ../backup-mirror.git …"
git clone --mirror . ../backup-mirror.git >/dev/null 2>&1 || true

if command -v git-filter-repo >/dev/null 2>&1; then
  ARGS=(); for p in "${PATHS[@]}"; do ARGS+=(--path "$p"); done
  git filter-repo --force --invert-paths "${ARGS[@]}"
else
  echo "git-filter-repo не найден — использую git filter-branch (медленнее)…"
  FILTER=''
  for p in "${PATHS[@]}"; do
    case "$p" in
      *'*') FILTER+="git rm -r --cached --ignore-unmatch $p >/dev/null 2>&1 || true; " ;;
      *)    FILTER+="git rm -r --cached --ignore-unmatch \"$p\" >/dev/null 2>&1 || true; " ;;
    esac
  done
  FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch --force --index-filter "$FILTER" \
    --prune-empty -- --all
  rm -rf .git/refs/original
fi

git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force origin "$BRANCH"

echo "Готово. Проверьте, что в истории нет паролей:"
echo "  git log --all --oneline && git grep -i 'turbo2' \$(git rev-list --all) -- | head"
