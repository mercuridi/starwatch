from datetime import datetime, timedelta

today = datetime.now().date()
date_week_from_now = today + timedelta(days=7)


one_week_today = {
    "start": date_week_from_now,
    "end": date_week_from_now + timedelta(days=1)
}
this_week = {
    "start": today,
    "end": date_week_from_now
}

print(f"today: {today}")
print(f"date_week_from_now: {date_week_from_now}")

print(f"one week: {one_week_today}")
print(f"this week: {this_week}")
