#!/bin/bash
# Fastest way to publish changes to the Bravery Tracker page.
# Usage:
#   ./publish.sh                 -> commits with a default message
#   ./publish.sh "your message"  -> commits with a custom message
set -e
cd "$(dirname "$0")"

if git diff --quiet && git diff --cached --quiet; then
  echo "No changes to publish."
  exit 0
fi

MSG="${1:-Update Bravery Trail page}"
git add -A
git commit -m "$MSG"
git push
echo "Published. Live in ~30-60s at https://nclloyd.github.io/tidbyt-bravery/"
