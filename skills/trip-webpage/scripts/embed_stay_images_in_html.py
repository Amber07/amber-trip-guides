#!/usr/bin/env python3
"""Embed local lodging-card images in an existing trip HTML page."""

from __future__ import annotations

import argparse
import base64
import mimetypes
import re
from pathlib import Path


IMAGE_FIELD_RE = re.compile(r'("image"\s*:\s*")([^"]+)(")')


def make_data_uri(image_path: Path) -> str:
    mime = mimetypes.guess_type(image_path.name)[0]
    if mime is None:
        suffix = image_path.suffix.lower()
        if suffix == ".webp":
            mime = "image/webp"
        elif suffix in {".jpg", ".jpeg"}:
            mime = "image/jpeg"
        elif suffix == ".png":
            mime = "image/png"
        else:
            raise ValueError(f"无法判断图片 MIME 类型: {image_path}")

    payload = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def embed_stay_images(html_path: Path) -> tuple[str, int, list[str]]:
    html = html_path.read_text(encoding="utf-8")
    page_dir = html_path.parent
    missing: list[str] = []
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        prefix, value, suffix = match.groups()
        if value.startswith("data:image/") or not value.startswith("assets/stay-"):
            return match.group(0)

        image_path = page_dir / value
        if not image_path.exists():
            missing.append(value)
            return match.group(0)

        count += 1
        return f"{prefix}{make_data_uri(image_path)}{suffix}"

    return IMAGE_FIELD_RE.sub(replace, html), count, missing


def main() -> None:
    parser = argparse.ArgumentParser(
        description="把已有行程 HTML 中的住宿卡 assets/stay-* 图片内嵌为 data URI，适合语雀单文件上传。"
    )
    parser.add_argument("html", type=Path, help="要处理的 trip index.html")
    parser.add_argument("--dry-run", action="store_true", help="只统计，不写回文件")
    args = parser.parse_args()

    html_path = args.html
    if not html_path.exists():
        raise SystemExit(f"文件不存在: {html_path}")

    new_html, count, missing = embed_stay_images(html_path)
    if missing:
        for item in missing:
            print(f"缺少图片: {item}")
        raise SystemExit(1)

    if args.dry_run:
        print(f"将内嵌 {count} 张住宿图片")
        return

    html_path.write_text(new_html, encoding="utf-8")
    print(f"已内嵌 {count} 张住宿图片: {html_path}")


if __name__ == "__main__":
    main()
