#!/bin/bash
# Renders whatever mission_queue.json currently says (current + completed)
# and pushes it directly to the Tidbyt — no queue advancement, no git
# operations. Use "Bravery Pull"/"Bravery Publish" first if you need to
# sync mission_queue.json itself with GitHub before running this.
set -e
cd "$(dirname "$0")"

PIXLET=/Users/niclloyd/Desktop/Claude/.local/pixlet/pixlet
source /Users/niclloyd/Desktop/Claude/.local/pixlet/device.env

CURRENT=$(jq -r '.current' mission_queue.json)
COMPLETED=$(jq -r '.completed' mission_queue.json)
echo "Rendering: \"$CURRENT\" (done=$COMPLETED)"

"$PIXLET" render mission.star -o mission.webp challenge="$CURRENT" done="$COMPLETED"
"$PIXLET" push -t "$TIDBYT_API_TOKEN" -i mission "$TIDBYT_DEVICE_ID" mission.webp
rm -f mission.webp

echo "Synced to Tidbyt."
