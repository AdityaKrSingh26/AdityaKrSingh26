"""Scrape the public GitHub contributions calendar (no token needed) and write data/contributions.json."""
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "AdityaKrSingh26"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"

COUNT_RE = re.compile(r"^(No|\d[\d,]*)\s+contributions?\s+on", re.IGNORECASE)


def fetch_days():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    tooltips = {
        tip["for"]: tip.get_text(strip=True)
        for tip in soup.select("tool-tip[for]")
    }

    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        cell_id = cell.get("id", "")
        day, week = (int(x) for x in cell_id.rsplit("-", 2)[-2:])
        level = int(cell.get("data-level", 0))

        tooltip_text = tooltips.get(cell_id, "")
        match = COUNT_RE.match(tooltip_text)
        count = 0 if not match or match.group(1).lower() == "no" else int(match.group(1).replace(",", ""))

        days.append({"date": cell["data-date"], "week": week, "day": day, "level": level, "count": count})

    days.sort(key=lambda d: d["date"])
    return days


def compute_stats(days):
    total = sum(d["count"] for d in days)

    current_streak = 0
    for d in reversed(days):
        if d["count"] == 0:
            break
        current_streak += 1

    longest_streak = 0
    running = 0
    for d in days:
        if d["count"] > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0

    best_day = max(days, key=lambda d: d["count"], default=None)

    monthly = {}
    for d in days:
        month = d["date"][:7]
        monthly[month] = monthly.get(month, 0) + d["count"]

    return {
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": {"date": best_day["date"], "count": best_day["count"]} if best_day else None,
        "monthly": monthly,
    }


def main():
    days = fetch_days()
    data = {"username": USERNAME, "days": days, "stats": compute_stats(days)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))
    print(f"wrote {len(days)} days, {data['stats']['total']} contributions -> {OUT}")


if __name__ == "__main__":
    main()
