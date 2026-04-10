import feedparser
import json
import os
import re
from datetime import datetime, timezone

# ── Entity list ───────────────────────────────────────────────────────────────
ENTITIES = ENTITIES = [
    "AGI Greenpac",
    "Allied BD",
    "Artemis Medicare",
    "Balu Forge",
    "BharatRohan Airborne Innovations",
    "Bigbloc Construction",
    "Caplin Point",
    "Dynamatic",
    "Easy Trip Planners",
    "eMudhra",
    "Fujiyama Power Systems",
    "Glottis",
    "Gopal Snacks",
    "Graphite India",
    "HT Media",
    "India Pesticides",
    "Jindal Steel",
    "JNK India",
    "Lumino Industries",
    "Markaz",
    "Minda Corporation",
    "Paradeep Phosphates",
    "Power Mech-Projects",
    "Quality Power",
    "Rushil Decor",
    "Sanstar",
    "SBL Energy",
    "Shree Pushkar",
    "SJS Enterprises",
    "SOM Group",
    "TCI Express",
    "Telge Projects",
    "Texmaco",
    "TVS Supply Chain Solutions",
    "Websol",
]

# ── Google News RSS feeds to monitor ─────────────────────────────────────────
RSS_FEEDS = [
    "https://news.google.com/rss/search?q=Indian+stock+market&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=BSE+NSE+India&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=India+business+earnings&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=India+corporate+news&hl=en-IN&gl=IN&ceid=IN:en",
]

LOG_FILE = "match_log.jsonl"
SEEN_FILE = ".seen_guids.json"


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen(seen: set):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def find_matches(text: str) -> list[str]:
    text_lower = text.lower()
    return [e for e in ENTITIES if e.lower() in text_lower]


def run():
    seen = load_seen()
    new_seen = set()
    matches_found = 0

    with open(LOG_FILE, "a") as log:
        for feed_url in RSS_FEEDS:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                guid = entry.get("id") or entry.get("link", "")
                if guid in seen:
                    continue
                new_seen.add(guid)

                title = entry.get("title", "")
                summary = entry.get("summary", "")
                combined = f"{title} {summary}"

                matched = find_matches(combined)
                if matched:
                    record = {
                        "ts": datetime.now(timezone.utc).isoformat(),
                        "entities": matched,
                        "title": title,
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "source_feed": feed_url,
                    }
                    log.write(json.dumps(record) + "\n")
                    matches_found += 1
                    print(f"[MATCH] {matched} → {title[:80]}")

    seen.update(new_seen)
    save_seen(seen)

    print(f"\nDone. {matches_found} new matches logged to {LOG_FILE}.")
    print(f"Total seen GUIDs: {len(seen)}")


if __name__ == "__main__":
    run()
