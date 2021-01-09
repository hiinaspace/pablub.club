#!/usr/bin/env python
from yattag import Doc
import re
import requests
import geoip2.database
from geoip2.errors import AddressNotFoundError

geodb = geoip2.database.Reader('GeoLite2-Country_20200616/GeoLite2-Country.mmdb')

pablub_headers = {
    "Version": "0.80.75",
    "User-Agent": "pablub.club",
    "Content-Type": "text/plain;charset=UTF-8",

}
# requires posting an empty object
# and dave's SSL certs are broken somehow, too lazy to debug
r = requests.post("https://pavlov-ms.vankrupt.com/servers/v1/list", headers=pablub_headers, json={}, verify='./vankrupt-com-chain.pem')

workshop_id_re = re.compile(r"^UGC(\d+)$")

def ip_country(ip):
    try:
        return geodb.country(ip).country.name
    except AddressNotFoundError:
        return "Unknown"

doc, tag, text, line = Doc().ttl()
doc.asis("<!DOCTYPE html>")
with tag('html'):
    with tag('head'):
        doc.asis("<meta charset=utf8>")
        line('title', "pablub custom serbers")
        doc.stag('link', href="style.css", rel="stylesheet")
        doc.asis('<link href="tabulator-master/dist/css/tabulator.min.css" rel="stylesheet">')
        doc.asis('<link href="tabulator-master/dist/css/tabulator_midnight.css" rel="stylesheet">')
        doc.asis('<script type="text/javascript" src="tabulator-master/dist/js/tabulator.min.js" async id=tabulator-script></script>')
        line('script', '', ('async', ''), src='pablub.js')
    with tag('body'):
        with tag('h1'):
            text("pablub custom serbers ")
            with tag('a', href="https://stats.pablub.club/d/5vWE7ISZk/all-pablub-custom-servers"):
                doc.stag("img", src="/totalplayers/")

        if not r:
            line('p', "couldn't fetch server information, fix it dave")
        else:
            serbs = r.json()
            with tag('table', id="serbers"):
                with tag('thead'):
                    with tag('tr'):
                        line('th', 'Name')
                        line('th', 'Gamemode')
                        line('th', 'Map')
                        line('th', 'Current Players')
                        line('th', 'Max Players')
                        line('th', 'Location')

                for serb in sorted(serbs['servers'], reverse=True, key=lambda x: int(x['slots'])):
                    with tag('tr'):
                        line('td', serb['name'])
                        line('td', serb['gameMode'])
                        wid = workshop_id_re.match(serb["mapId"])
                        with tag('td'):
                            if wid:
                                with tag('a', href=f"https://steamcommunity.com/sharedfiles/filedetails/?id={wid.group(1)}", target="_blank"):
                                    text(serb['mapLabel'])
                            else:
                                text(serb['mapLabel'])
                        with tag('td'):
                            with tag('a', href="https://stats.pablub.club/d/G-CkMD4Wk/pablub?orgId=1&var-hash=%s" % (serb['hash'])):
                                #doc.stag('img', src="/graph/%s" % (serb['hash']))
                                text(serb['slots'])
                            #doc.asis(" ")
                        line('td', serb['maxSlots'])
                        line('td', ip_country(serb['ip']) or "Unknown")


        with tag('footer'):
            import datetime
            text(f"last updated at {datetime.datetime.now()}")

print(doc.getvalue())
