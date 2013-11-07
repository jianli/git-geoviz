"""
Converts git log output to timestamped geographic coordinates.

Pipe input from:

git log --reverse --no-merges --format='%H|%ai|%ae'
"""

import datetime
import dateutil.parser
import json
import pytz
import sys


TIMEZONES = {
    'US/Central': [38.971667, -95.235278],
    'US/Eastern': [40.67, -73.94],
    'US/Hawaii': [21.311389, -157.796389],
    'US/Pacific': [37.708333, -122.280278],
    'Europe/Warsaw': [52.233333, 21.016667],
    'Europe/London': [51.507222, -0.1275],
    'Australia/Sydney': [-33.859972, 151.211111],
    'Asia/Tokyo': [35.689506, 139.6917],
    'Asia/Singapore': [1.3, 103.8],
    'America/Argentina/Buenos_Aires': [-34.603333, -58.381667],
}


def matches_timezone(localized_date, timezone):
    return pytz.timezone(timezone).localize(
        localized_date.replace(tzinfo=None)) == localized_date


def get_timezone(localized_date):
    for tz in TIMEZONES:
        if matches_timezone(date, tz):
            return tz
    return None


def total_seconds(localized_date):
    return (
        localized_date -
        datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.utc)
    ).total_seconds()


data = []
for line in sys.stdin.read().strip().split('\n'):
    sha1, date, user = line.split('|')
    date = dateutil.parser.parse(date)
    timezone = get_timezone(date)
    if not timezone:
        continue
    data.append([total_seconds(date), TIMEZONES[timezone]])

sys.stdout.write(json.dumps(data))
