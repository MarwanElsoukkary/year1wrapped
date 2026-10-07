#!/usr/bin/env python3
"""
Downloads the 30-second Spotify previews for the songs on the site, so they
can play automatically while she scrolls.

Run it on your Mac inside the unzipped site folder:
    python3 get_previews.py

It saves files named prev_<spotify id>.mp3 next to index.html.
Upload those along with everything else.
"""
import json
import re
import urllib.request

TRACKS = {
    "5KADKKJqxxF2d0a9Ir2lK3": "Be That Easy",
    "13VXVxePp4NUiXwtmQ0viz": "Said Sum (Remix)",
    "2aTf0R0TQCJJKcb0ipszD2": "SOMEBODY LOVES ME PT. 2",
    "7mjrovxCbFPlnkJ1aDhtu9": "Hagaraan Ala Al Shesha",
    "7zO8pvhMf6s1DzMMiV7CaU": "NARI NARI NARI",
    "6GZ1fXt4LMbYxqsh4KkzoU": "Forgive Me",
    "0QyJXG36Q3Kta662XS8GhY": "Too Fast",
    "6EpZVG2zXeXGUitW8979U8": "DELRESTO (ECHOES)",
    "4MJpGGIDRwHuWoZCddIOgM": "ILYSMIH",
    "4KDNRh9Oor80z3XIxdWlui": "Bubbly",
    "7bXbTuAqOq7OzPb27NS0ZV": "WOOPAAA",
    "5HCTbcF18u5DcYNwEWWf3n": "Ayonha",
    "2LTRSoho4n35jXJBYZrpwp": "All Of My Friends",
    "0oZaQXBtEQPtVX1wtsMSsA": "Fuck Ya Butt",
    "1uALqmxOYLMGJGOzwSypXF": "YAYA",
    "1RTtg5LOy7r5rtwBIA5DBx": "NINI",
    "3xIzkKqp7oe37NEVrcPjGS": "TROLLZ",
    "4x7j9ed3FRH6CHj27kiTQ3": "Wackelkontakt",
    "1fA0xIPAY6TKNwsjQrOQ11": "All Your Time",
    "7L4G39PVgMfaeHRyi1ML7y": "Day Dreaming",
    "2d0UrqT7OYP0gcntGV2rsp": "Konnichiwa",
    "6BdgtqiV3oXNqBikezwdvC": "Over",
    "1DyUe6OZxW5c7jN1MhUvyH": "Controlla Freestyle",
    "0RZnx3YbepVt8MrrjU0Zyg": "678",
    "1VWiDyYTrqQhhmnWANWkFa": "SaWaDiKa",
    "2KePS2HZdSVq8awIxIlWgn": "Kings & Queens",
}
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        return r.read()


ok, missing = [], []
for tid, name in TRACKS.items():
    try:
        html = get(f"https://open.spotify.com/embed/track/{tid}").decode("utf-8", "ignore")
        m = re.search(r'"audioPreview"\s*:\s*\{\s*"url"\s*:\s*"([^"]+)"', html)
        url = m.group(1).encode().decode("unicode_escape") if m else None
        if not url:
            m = re.search(r'https://p\.scdn\.co/mp3-preview/[A-Za-z0-9]+[^"\\]*', html)
            url = m.group(0) if m else None
        if not url:
            missing.append(name)
            print(f"  no preview: {name}")
            continue
        data = get(url)
        with open(f"prev_{tid}.mp3", "wb") as f:
            f.write(data)
        ok.append(name)
        print(f"  saved: {name}")
    except Exception as e:
        missing.append(name)
        print(f"  failed: {name} ({e})")

print(f"\nSaved {len(ok)} previews. Missing {len(missing)}: {', '.join(missing) or 'none'}")
print("Upload all the prev_*.mp3 files to your repo next to index.html.")
