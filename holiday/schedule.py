#!/usr/bin/env python3
"""Decides what the holiday app should show today (US Eastern time).

Prints JSON: {"action": "push"|"remove", "holiday": ..., "days": ..., "date": ...}
Usage: schedule.py [--date YYYY-MM-DD]   (--date is for testing)

Stateless and idempotent: the workflow can run this as often as it likes and
always converge on the right state, which matters because GitHub's scheduler
fires this repo's cron jobs hours late.
"""
import json
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

# Holidays that have artwork in holiday.star. Others on the calendar below are
# recognized but treated as "nothing to show" until their sprite is added.
SUPPORTED = {"thanksgiving", "christmas", "christmas_countdown"}


def nth_weekday(year, month, weekday, n):
    """nth occurrence (1-based) of weekday (Mon=0) in a month."""
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def easter(year):
    """Anonymous Gregorian algorithm."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return date(year, month, day + 1)


def holidays(year):
    return {
        date(year, 1, 1): "new_year",
        date(year, 2, 14): "valentines",
        date(year, 3, 17): "st_patricks",
        easter(year): "easter",
        nth_weekday(year, 5, 6, 2): "mothers_day",
        nth_weekday(year, 6, 6, 3): "fathers_day",
        date(year, 7, 4): "july_4th",
        date(year, 10, 31): "halloween",
        nth_weekday(year, 11, 3, 4): "thanksgiving",
        date(year, 12, 25): "christmas",
    }


def decide(today):
    holiday, days = holidays(today.year).get(today), ""

    # Christmas countdown runs from the day after Thanksgiving through Dec 24
    countdown_start = nth_weekday(today.year, 11, 3, 4) + timedelta(days=1)
    christmas = date(today.year, 12, 25)
    if holiday is None and countdown_start <= today < christmas:
        holiday, days = "christmas_countdown", str((christmas - today).days)

    action = "push" if holiday in SUPPORTED else "remove"
    return {"action": action, "holiday": holiday or "", "days": days, "date": today.isoformat()}


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--date":
        today = date.fromisoformat(sys.argv[2])
    else:
        today = datetime.now(ZoneInfo("America/New_York")).date()
    print(json.dumps(decide(today)))
