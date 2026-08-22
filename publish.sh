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

CACHEBUST=$(date +%s)
echo "Published. Live in ~30-60s (GitHub's CDN caches for 10 min, so use this link to skip the wait):"
echo "https://nclloyd.github.io/tidbyt-bravery/?v=$CACHEBUST"
