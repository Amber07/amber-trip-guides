#!/usr/bin/env python3
"""检查已生成攻略网页是否缺少 trip-webpage 模板能力。"""

from __future__ import annotations

import argparse
from pathlib import Path


FEATURES = {
    "hero_media_layer": [
        "hero-media",
        ".hero::after",
        "heroMediaSlot",
        "renderHeroMedia",
        "const heroMedia",
    ],
    "image_lightbox": [
        "imageLightbox",
        "openImageLightbox",
        "closeImageLightbox",
        "cursor: zoom-in",
    ],
    "lightbox_carousel": [
        "lightbox-nav",
        "lightboxDots",
        "renderLightboxImage",
        "shiftLightboxImage",
        "setLightboxImage",
    ],
    "image_carousel": [
        "panelImageWrap",
        "getSpotImages",
        "shiftSpotImage",
        "setSpotImage",
        "carousel-dot",
    ],
    "mixed_media_carousel": [
        "panel-video",
        "lightboxVideo",
        "isVideoItem",
        "coverImageFor",
        "show-video",
    ],
    "bilingual_display_name": [
        "function displayName",
        "${item.name}｜${item.zh}",
    ],
    "spot_detail_panel": [
        "spot-panel",
        "panelImage",
        "panelBody",
        "function selectSpot",
    ],
    "rating_panel": [
        "ratingPanel",
        "function renderRating",
        "renderRatingBars",
    ],
    "mobile_bottom_nav": [
        "@media (max-width: 760px)",
        "inset: auto 10px",
        "env(safe-area-inset-bottom",
    ],
    "day_jump": [
        "dayJump",
        "function renderDayJump",
        "jumpToDay",
    ],
    "stay_shortlist": [
        "stay-section",
        "stay-card",
        "stayJump",
        "initStayJump",
    ],
}


def audit(html: str) -> list[tuple[str, list[str]]]:
    missing: list[tuple[str, list[str]]] = []
    for feature, markers in FEATURES.items():
        absent = [marker for marker in markers if marker not in html]
        if absent:
            missing.append((feature, absent))
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit an existing trip webpage for missing template features.")
    parser.add_argument("html", help="已有攻略网页 HTML 路径")
    args = parser.parse_args()
    path = Path(args.html)
    html = path.read_text(encoding="utf-8")
    missing = audit(html)
    if not missing:
        print("OK: 当前网页包含已知 trip-webpage 模板能力。")
        return 0
    print("MISSING: 当前网页可能缺少以下模板能力：")
    for feature, markers in missing:
        print(f"- {feature}: 缺少 {', '.join(markers)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
