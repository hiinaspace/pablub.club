#!/usr/bin/env bash
# slots/maxslots for all custom servers
set -eo pipefail
while true; do
  curl -s ms.pavlov-vr.com/v1/servers -H 'version: 0.70.4' |\
  jq '.servers[] | ["pavlov.public-servers.\(.hash).slots \(.slots) \(now)", "pavlov.public-servers.\(.hash).max-slots \(.maxSlots) \(now)"][]' -r
  sleep 60
done | nc localhost 2003 -q0
