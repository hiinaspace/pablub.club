#!/usr/bin/env bash
# slots/maxslots for all custom servers
set -eo pipefail
while true; do
  curl -s --cacert vankrupt-com-chain.pem -XPOST https://pavlov-ms.vankrupt.com/servers/v1/list -H 'version: 0.80.81' -H 'User-Agent: pablub.club' -H 'Content-Type: text/plain;charset=UTF-8' -d '{}' |\
  jq '.servers[] | ["pavlov.public-servers.\(.hash).slots \(.slots) \(now)", "pavlov.public-servers.\(.hash).max-slots \(.maxSlots) \(now)"][]' -r
  sleep 60
done | nc localhost 2003 -q0
