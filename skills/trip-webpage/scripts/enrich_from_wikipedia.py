#!/usr/bin/env python3
"""用 Wikipedia 搜索补全景点简介和缺失图片 URL。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API = "https://en.wikipedia.org/w/api.php"


def fetch_summary(query: str) -> dict | None:
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": "1",
        "prop": "extracts|pageimages|info",
        "exintro": "1",
        "explaintext": "1",
        "piprop": "original|thumbnail",
        "pithumbsize": "1200",
        "inprop": "url",
        "format": "json",
        "formatversion": "2",
    }
    url = f"{API}?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": "trip-webpage/1.0"})
    with urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    pages = payload.get("query", {}).get("pages", [])
    if not pages:
        return None
    return pages[0]


def compact_intro(text: str, limit: int = 180) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def needs_text(value: object) -> bool:
    return not isinstance(value, str) or not value.strip() or value.strip() in {"待补充", "TODO", "景点简介"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Enrich missing spot intro/images from Wikipedia.")
    parser.add_argument("data", help="trip-data.json")
    parser.add_argument("--output", "-o", help="输出更新后的 JSON；不提供则覆盖原文件")
    args = parser.parse_args()

    data_path = Path(args.data)
    data = json.loads(data_path.read_text(encoding="utf-8"))
    for spot in data.get("spots", []):
        if not isinstance(spot, dict):
            continue
        intro_missing = needs_text(spot.get("intro"))
        image_missing = needs_text(spot.get("image"))
        if not intro_missing and not image_missing:
            continue
        query = spot.get("wikipediaTitle") or spot.get("name") or spot.get("zh")
        if not query:
            continue
        page = fetch_summary(str(query))
        if not page:
            continue
        if intro_missing and page.get("extract"):
            spot["intro"] = compact_intro(page["extract"])
            spot.setdefault("wikipediaUrl", page.get("fullurl"))
        image = page.get("original", {}).get("source") or page.get("thumbnail", {}).get("source")
        if image_missing and image:
            spot["image"] = image
            spot.setdefault("photoSource", page.get("fullurl") or image)
            spot.setdefault("photoCredit", "Wikipedia / Wikimedia Commons")

    output_path = Path(args.output) if args.output else data_path
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
