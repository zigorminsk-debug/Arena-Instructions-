#!/usr/bin/env bash
# Защита ветки main: запрет удаления и force-push, обязательный Pull Request.
#
#   ./tools/protect_branch.sh
#
# Если появится «Resource not accessible by integration» — у вашего токена нет
# прав Administration. Два пути:
#   1) кнопка «Protect this branch» на странице репозитория;
#   2) Settings → Rules → Rulesets → New branch ruleset (Target: main,
#      включить Restrict deletions, Block force pushes, Require a pull request).
set -euo pipefail

REPO="${REPO:-zigorminsk-debug/Arena-Instructions-}"

echo "Репозиторий: $REPO"
echo "Пробую создать ruleset через API…"

set +e
OUT=$(gh api -X POST "repos/$REPO/rulesets" \
  -f name="main-protection" -f target=branch -f enforcement=active \
  -f 'conditions[ref_name][include][]=refs/heads/main' \
  -f 'rules[][type]=deletion' -f 'rules[][type]=non_fast_forward' \
  -f 'rules[][type]=pull_request' \
  -f 'rules[0][parameters][required_approving_review_count]=0' 2>&1)
RC=$?
set -e

if [ $RC -eq 0 ]; then
  echo "OK: ruleset создан."
  echo "$OUT" | head -5
  echo
  echo "Проверить:  gh api repos/$REPO/rulesets | head"
else
  echo "Не удалось через API:"
  echo "$OUT" | head -3
  cat <<'EOT'

Сделайте вручную (2 минуты):
  1. Откройте https://github.com/REPO/settings/rules
  2. New branch ruleset → Name: main-protection
  3. Target branches → Add target → Include by pattern → main
  4. Rules: Restrict deletions ✔, Block force pushes ✔,
            Require a pull request before merging ✔ (Approvals: 0)
  5. Enforcement status: Active → Create
EOT
fi

echo
echo "Заодно проверьте: Settings → Pages (source: main / root) и Settings → Issues"
echo "(анонимные issue в публичном репозитории могут создавать посторонние)."
