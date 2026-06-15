#!/usr/bin/env bash
# Simulate a child-repo upgrade: clone template, apply cherry-pick areas, validate bootstrap.
# See docs/UPGRADING_FROM_TEMPLATE.md for the human/agent merge playbook.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

echo "==> Simulating template upgrade in $WORKDIR"

git clone --quiet "file://$ROOT" "$WORKDIR/child"
cd "$WORKDIR/child"

AREAS=(
  scripts/check-file-encoding.sh
  scripts/validate-bootstrap.sh
  scripts/validate-template-index.sh
  .github/workflows/dependency-review.yml
)

for path in "${AREAS[@]}"; do
  if [ ! -e "$path" ]; then
    echo "MISSING in clone: $path"
    exit 1
  fi
done

bash scripts/validate-bootstrap.sh --quick
bash scripts/validate-template-index.sh

echo "==> Non-interactive init smoke (web stack, no prune)"
bash scripts/init-project.sh \
  --non-interactive \
  --stack web \
  --project-name "Upgrade Sim" \
  --purpose "Cherry-pick validation" \
  --no-prune

bash scripts/validate-bootstrap.sh --quick

echo "Upgrade simulation passed"
