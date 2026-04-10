# Google News Entity Tracker

Tracks Google News RSS feeds for mentions of ~35 Indian listed companies and logs matches to `match_log.jsonl`.

Runs every 3 hours via GitHub Actions — completely free.

## Setup

1. Create a new GitHub repo and push these files
2. Enable Actions (Settings → Actions → Allow all)
3. That's it — first run triggers automatically per the schedule

## Files

| File | Purpose |
|---|---|
| `tracker.py` | Main script — fetches RSS, matches entities, appends log |
| `match_log.jsonl` | Output — one JSON record per match, appended each run |
| `.seen_guids.json` | Dedup cache — tracks article GUIDs already processed |
| `.github/workflows/tracker.yml` | Cron schedule (every 3 hours) |

## Log format

Each line in `match_log.jsonl` looks like:

```json
{
  "ts": "2026-04-10T06:00:00+00:00",
  "entities": ["Infosys", "TCS"],
  "title": "IT majors see Q4 uptick as deal wins accelerate",
  "link": "https://...",
  "published": "Thu, 10 Apr 2026 05:30:00 GMT",
  "source_feed": "https://news.google.com/rss/..."
}
```

## Customising

- **Entities**: Edit the `ENTITIES` list in `tracker.py`
- **Feeds**: Add/remove URLs in `RSS_FEEDS`
- **Frequency**: Edit the cron expression in the workflow YAML (`0 */3 * * *` = every 3 hours)
- **Retention**: `.seen_guids.json` is cached between runs so articles are never logged twice
