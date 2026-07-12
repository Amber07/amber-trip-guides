#!/usr/bin/env python3
"""下载 trip-data.json 中的外部媒体，并把媒体路径改成本地 assets。"""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "image"


SUPPORTED_MEDIA_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".webm", ".mov", ".m4v"}


def extension_from_response(url: str, content_type: str | None) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in SUPPORTED_MEDIA_SUFFIXES:
        return suffix
    if content_type:
        guessed = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if guessed in SUPPORTED_MEDIA_SUFFIXES:
            return guessed
    return ".jpg"


def download(url: str, target_stem: str, assets_dir: Path) -> str:
    request = Request(url, headers={"User-Agent": "trip-webpage/1.0"})
    with urlopen(request, timeout=20) as response:
        content_type = response.headers.get("Content-Type")
        suffix = extension_from_response(url, content_type)
        target = assets_dir / f"{slug(target_stem)}{suffix}"
        counter = 2
        while target.exists():
            target = assets_dir / f"{slug(target_stem)}_{counter}{suffix}"
            counter += 1
        target.write_bytes(response.read())
    return f"assets/{target.name}"


def download_cached(url: str, target_stem: str, assets_dir: Path, cache: dict[str, str]) -> str:
    if url not in cache:
        cache[url] = download(url, target_stem, assets_dir)
    return cache[url]


def localize_value(owner: dict, key: str, name: str, assets_dir: Path, failures: list[str], cache: dict[str, str]) -> None:
    url = owner.get(key)
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        return
    try:
        owner[key] = download_cached(url, name, assets_dir, cache)
        owner.setdefault("photoSource", url)
        owner.setdefault("photoCredit", "网络图片，已本地保存")
    except (OSError, URLError, TimeoutError) as exc:
        failures.append(f"{name}: {url} 下载失败：{exc}")


def localize_spot_images(spot: dict, assets_dir: Path, failures: list[str], cache: dict[str, str]) -> None:
    images = spot.get("images")
    if not isinstance(images, list):
        return

    name = str(spot.get("id") or spot.get("name") or "spot")
    for index, item in enumerate(images, start=1):
        label = f"{name}_{index}"
        if isinstance(item, str):
            if not item.startswith(("http://", "https://")):
                continue
            try:
                images[index - 1] = download_cached(item, label, assets_dir, cache)
            except (OSError, URLError, TimeoutError) as exc:
                failures.append(f"{label}: {item} 下载失败：{exc}")
            continue
        if isinstance(item, dict):
            url = item.get("src")
            if isinstance(url, str) and url.startswith(("http://", "https://")):
                try:
                    item["src"] = download_cached(url, label, assets_dir, cache)
                    item.setdefault("photoSource", url)
                    item.setdefault("photoCredit", spot.get("photoCredit") or "网络图片，已本地保存")
                except (OSError, URLError, TimeoutError) as exc:
                    failures.append(f"{label}: {url} 下载失败：{exc}")
            poster = item.get("poster")
            if isinstance(poster, str) and poster.startswith(("http://", "https://")):
                try:
                    item["poster"] = download_cached(poster, f"{label}_poster", assets_dir, cache)
                except (OSError, URLError, TimeoutError) as exc:
                    failures.append(f"{label} poster: {poster} 下载失败：{exc}")


def localize_stay_images(data: dict, assets_dir: Path, failures: list[str], cache: dict[str, str]) -> None:
    for section in data.get("staySections", []):
        if not isinstance(section, dict):
            continue
        section_id = section.get("id") or section.get("title") or "stay"
        for index, card in enumerate(section.get("cards", []), start=1):
            if not isinstance(card, dict):
                continue
            url = card.get("image")
            if not isinstance(url, str) or not url.startswith(("http://", "https://")):
                continue
            name = f"{section_id}_{card.get('name') or index}"
            try:
                card["image"] = download_cached(url, name, assets_dir, cache)
                card.setdefault("imageSource", url)
                card.setdefault("imageCaption", "图片：网络，已本地保存")
            except (OSError, URLError, TimeoutError) as exc:
                failures.append(f"{name}: {url} 下载失败：{exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Download remote trip images into local assets.")
    parser.add_argument("data", help="trip-data.json")
    parser.add_argument("--assets-dir", required=True, help="目标 assets 目录")
    parser.add_argument("--output", "-o", help="输出更新后的 JSON；不提供则覆盖原文件")
    args = parser.parse_args()

    data_path = Path(args.data)
    assets_dir = Path(args.assets_dir)
    assets_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(data_path.read_text(encoding="utf-8"))

    failures: list[str] = []
    cache: dict[str, str] = {}
    page = data.get("page", {})
    if isinstance(page, dict) and isinstance(page.get("heroImage"), str) and page["heroImage"].startswith(("http://", "https://")):
        try:
            page["heroImage"] = download_cached(page["heroImage"], "hero", assets_dir, cache)
        except (OSError, URLError, TimeoutError) as exc:
            failures.append(f"hero: {page['heroImage']} 下载失败：{exc}")
    if isinstance(page, dict) and isinstance(page.get("heroPoster"), str) and page["heroPoster"].startswith(("http://", "https://")):
        try:
            page["heroPoster"] = download_cached(page["heroPoster"], "hero_poster", assets_dir, cache)
        except (OSError, URLError, TimeoutError) as exc:
            failures.append(f"hero poster: {page['heroPoster']} 下载失败：{exc}")

    for spot in data.get("spots", []):
        if isinstance(spot, dict):
            localize_value(spot, "image", spot.get("id") or spot.get("name") or "spot", assets_dir, failures, cache)
            localize_spot_images(spot, assets_dir, failures, cache)
    localize_stay_images(data, assets_dir, failures, cache)

    output_path = Path(args.output) if args.output else data_path
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    for failure in failures:
        print(failure, file=sys.stderr)
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
