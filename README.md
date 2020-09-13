# [pablub.club](https://pablub.club)

Server list and graphite stats collector for Pavlov VR dedicated servers.

`player-metrics.sh` scrapes all server's current player counts into graphite's
TCP line protocol, assuming graphite is running on localhost on the default
port. It depends on curl and jq. I recommend similarly supervising it with
systemd.

`storage-schemas.conf` and `storage-aggregation.conf` are what I use for
graphite. The max aggregation is important or the player counts will look
innacurate.

`pablub.py` is a python script to generate an html server list. `pip install -r
requirements.txt` to grab all the dependencies (I also recommend running in a
`python3 -m venv venv` virtualenv). `update.sh` will run the script every
minute. You can wrap `update.sh` in a systemd unit for easy supervision, or
just run it in tmux if you're lazy.

The generated HTML page depends on graphite-web's png renderer to generate
sparklines for each server's player count, which I proxy with the
`nginx.config` as an example (which also proxies grafana to
stats.pablub.club). It does kind of slam the graphite-web WSGI server though
for every page load. Might need additional caching in nginx.
