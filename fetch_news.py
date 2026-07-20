import json, re, sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

TOPICS = [
    "Ranveer Singh", "FIFA 2026", "Bollywood", "Cricket India",
    "World News", "Health and Pregnancy", "Food and Recipes",
    "Karnataka News", "Technology", "Bengaluru"
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def fetch_topic(topic):
    url = "https://news.google.com/rss/search?q=" + urllib.request.quote(topic) + "&hl=en-IN&gl=IN&ceid=IN:en"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = resp.read()
    root = ET.fromstring(data)
    channel = root.find("channel")
    items = []
    for item in channel.findall("item")[:8]:
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        pubdate = item.findtext("pubDate") or ""
        source_el = item.find("source")
        source = source_el.text if source_el is not None else ""
        if source and title.endswith(" - " + source):
            title = title[: -(len(source) + 3)]
        items.append({"title": title, "link": link, "pubDate": pubdate, "source": source})
    return items

def main():
    result = {"updated": datetime.now(timezone.utc).isoformat(), "topics": {}}
    for t in TOPICS:
        try:
            result["topics"][t] = fetch_topic(t)
            print(f"OK: {t} -> {len(result['topics'][t])} items", file=sys.stderr)
        except Exception as e:
            result["topics"][t] = []
            print(f"FAIL: {t} -> {e}", file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
