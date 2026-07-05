#!/usr/bin/env python3
"""用经纬度、日期和时区补全 trip-data.json 中缺失的日出日落时间。"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API = "https://api.sunrise-sunset.org/json"
SOURCE_LABEL = "Sunrise-Sunset.org"
SOURCE_URL = "https://sunrise-sunset.org/api"
MISSING = {"", "-", "—", "待补充", "未知", "tbd", "todo", "n/a", "na"}


def is_missing(value: object) -> bool:
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    return value.strip().lower() in MISSING


def day_label(day: dict) -> str:
    if day.get("sunLabel"):
        return str(day["sunLabel"]).strip()
    title = str(day.get("title", "")).strip()
    if "→" in title:
        title = title.split("→")[-1].strip()
    if "/" in title:
        title = title.split("/")[0].strip()
    return title or str(day.get("base", "")).split("，")[0].strip() or "当地"


def fetch_sun_times(lat: float, lng: float, date: str, tzid: str) -> dict:
    params = {
        "lat": lat,
        "lng": lng,
        "date": date,
        "formatted": 0,
        "tzid": tzid,
    }
    request = Request(f"{API}?{urlencode(params)}", headers={"User-Agent": "trip-webpage/1.0"})
    with urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("status") != "OK":
        raise RuntimeError(f"Sunrise-Sunset API 返回 {payload.get('status')}")
    return payload["results"]


def hhmm(value: str) -> str:
    return datetime.fromisoformat(value).strftime("%H:%M")


def enrich(data: dict, tzid: str, overwrite: bool = False) -> int:
    filled = 0
    for day in data.get("days", []):
        if not isinstance(day, dict):
            continue
        need_sunrise = overwrite or is_missing(day.get("sunrise"))
        need_sunset = overwrite or is_missing(day.get("sunset"))
        if not need_sunrise and not need_sunset:
            continue
        if day.get("lat") is None or day.get("lng") is None or not day.get("date"):
            print(f"跳过 Day {day.get('day', '?')}：缺少 date/lat/lng", file=sys.stderr)
            continue
        results = fetch_sun_times(float(day["lat"]), float(day["lng"]), str(day["date"]), tzid)
        label = day_label(day)
        if need_sunrise:
            day["sunrise"] = f"{label} {hhmm(results['sunrise'])}"
            filled += 1
        if need_sunset:
            day["sunset"] = f"{label} {hhmm(results['sunset'])}"
            filled += 1

    if filled:
        page = data.setdefault("page", {})
        page.setdefault("timeZone", tzid)
        page["sunTimeSource"] = SOURCE_URL
        footer = str(page.get("footer", page.get("title", ""))).strip()
        attribution = f"日出日落：{SOURCE_LABEL}"
        if footer and attribution not in footer:
            page["footer"] = f"{footer} · {attribution}"
    return filled


def main() -> int:
    parser = argparse.ArgumentParser(description="Fill missing sunrise/sunset fields in trip-data.json.")
    parser.add_argument("data", help="trip-data.json")
    parser.add_argument("--tzid", help="IANA 时区，例如 Australia/Perth、Australia/Hobart")
    parser.add_argument("--output", "-o", help="输出更新后的 JSON；不提供则覆盖原文件")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已有日出日落时间")
    args = parser.parse_args()

    data_path = Path(args.data)
    data = json.loads(data_path.read_text(encoding="utf-8"))
    tzid = args.tzid or data.get("page", {}).get("timeZone") or data.get("page", {}).get("tzid")
    if not tzid:
        raise SystemExit("缺少时区：请在 page.timeZone 中设置，或传 --tzid，例如 Australia/Perth")

    try:
        filled = enrich(data, tzid, args.overwrite)
    except (OSError, URLError, TimeoutError) as exc:
        raise SystemExit(f"联网查询日出日落失败：{exc}") from exc

    output_path = Path(args.output) if args.output else data_path
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已补全 {filled} 个日出/日落字段。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
