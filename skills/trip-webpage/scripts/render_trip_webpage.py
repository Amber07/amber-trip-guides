#!/usr/bin/env python3
"""把 trip-data.json 注入塔州同款 HTML 模板。"""

from __future__ import annotations

import argparse
import json
import re
from html import escape
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "assets" / "trip-template.html"


def js(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=6)


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        raise ValueError(f"找不到模板片段：{start} ... {end}")
    return pattern.sub(start + replacement + end, text, count=1)


def replace_const(text: str, name: str, value: Any) -> str:
    pattern = re.compile(rf"    const {re.escape(name)} = .*?;\n", re.S)
    if not pattern.search(text):
        raise ValueError(f"找不到 const {name}")
    return pattern.sub(f"    const {name} = {js(value)};\n", text, count=1)


def replace_text_tag(text: str, selector: str, value: str) -> str:
    return text.replace(selector, escape(value), 1)


def is_video_media(src: str) -> bool:
    suffix = Path(urlparse(src).path).suffix.lower()
    return suffix in {".mp4", ".webm", ".mov", ".m4v"}


def video_type(src: str) -> str:
    suffix = Path(urlparse(src).path).suffix.lower()
    if suffix == ".webm":
        return "video/webm"
    if suffix == ".mov":
        return "video/quicktime"
    if suffix == ".m4v":
        return "video/x-m4v"
    return "video/mp4"


def hero_media_html(src: str) -> str:
    safe_src = escape(src, quote=True)
    if is_video_media(src):
        return (
            '    <div class="hero-media" aria-hidden="true">\n'
            f'      <video autoplay muted loop playsinline preload="metadata"><source src="{safe_src}" type="{video_type(src)}"></video>\n'
            "    </div>"
        )
    return (
        '    <div class="hero-media" aria-hidden="true">\n'
        f'      <img src="{safe_src}" alt="">\n'
        "    </div>"
    )


def patch_page_copy(html: str, data: dict[str, Any]) -> str:
    page = data["page"]
    html = re.sub(r"<title>.*?</title>", f"<title>{escape(page.get('htmlTitle') or page['title'])}</title>", html, count=1)
    html = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="{escape(page.get("description", ""))}">',
        html,
        count=1,
    )
    if page.get("heroImage"):
        html = replace_const(
            html,
            "heroMedia",
            {
                "src": str(page["heroImage"]),
                "poster": str(page.get("heroPoster", "")),
                "alt": str(page.get("heroAlt") or page.get("heroTitle") or page["title"]),
            },
        )

    replacements = {
        '<p class="eyebrow">Tasmania East Coast · 2026.10.02-10.07</p>': f'<p class="eyebrow">{escape(page.get("eyebrow", ""))}</p>',
        "<h1>塔州东海岸 6 日游</h1>": f'<h1>{escape(page.get("heroTitle") or page["title"])}</h1>',
        '<p class="hero-copy">从 Launceston 一路向东南，沿海串起火焰湾、Freycinet 酒杯湾、Maria Island 野生袋熊、塔斯曼半岛海崖巡航，最后在 Hobart 城市与山景中收尾。</p>': f'<p class="hero-copy">{escape(page.get("heroCopy", ""))}</p>',
        '<p class="kicker">Route Map</p>': f'<p class="kicker">{escape(page.get("mapKicker", "Route Map"))}</p>',
        "<h2>塔州东海岸路线地图</h2>": f'<h2>{escape(page.get("mapTitle", "路线地图"))}</h2>',
        '<p class="lead">沿着行程查看景点、住宿区域与机场位置。点击地图图标可查看景点亮点、玩法和注意事项；自驾段为实线，Maria Island 渡轮段为虚线。</p>': f'<p class="lead">{escape(page.get("mapLead", ""))}</p>',
        '<p class="kicker">Daily Plan</p>': f'<p class="kicker">{escape(page.get("itineraryKicker", "Daily Plan"))}</p>',
        "<h2>每日行程安排</h2>": f'<h2>{escape(page.get("itineraryTitle", "每日行程安排"))}</h2>',
        '<p class="lead">每天按时间线整理主要景点、住宿、交通和日出日落信息。点击景点名即可联动查看地图位置、景点详情和多维评分。</p>': f'<p class="lead">{escape(page.get("itineraryLead", ""))}</p>',
        '<p class="kicker">Food</p>': f'<p class="kicker">{escape(page.get("foodKicker", "Food"))}</p>',
        "<h2>沿线餐饮与补给</h2>": f'<h2>{escape(page.get("foodTitle", "沿线餐饮与补给"))}</h2>',
        '<p class="lead">按当天路线整理适合吃饭和补给的区域，优先保证顺路、轻松和不耽误后续行程。</p>': f'<p class="lead">{escape(page.get("foodLead", ""))}</p>',
        '<p class="kicker">Before Departure</p>': f'<p class="kicker">{escape(page.get("prepKicker", "Before Departure"))}</p>',
        "<h2>需要提前预定和准备的东西</h2>": f'<h2>{escape(page.get("prepTitle", "需要提前预定和准备的东西"))}</h2>',
        '<p class="lead">把出发前需要预订、确认和打包的事项集中到一处，方便临行前逐项核对。</p>': f'<p class="lead">{escape(page.get("prepLead", ""))}</p>',
        "<footer>塔斯马尼亚东海岸旅行攻略 · 2026.10.02-10.07</footer>": f'<footer>{escape(page.get("footer", page["title"]))}</footer>',
    }
    for old, new in replacements.items():
        html = html.replace(old, new, 1)

    notice = page.get("notice", "")
    notice_html = f'<div class="notice">{escape(notice)}</div>' if notice else ""
    html = re.sub(r'\s*<div class="notice">重要时间提醒：.*?</div>', "\n      " + notice_html, html, count=1, flags=re.S)

    stats_html = "\n".join(
        f'        <div class="hero-stat"><strong>{escape(str(item.get("value", "")))}</strong><span>{escape(str(item.get("label", "")))}</span></div>'
        for item in data.get("heroStats", [])
    )
    html = re.sub(
        r'      <div class="hero-stats">\n.*?      </div>\n      <div class="notice"',
        f'      <div class="hero-stats">\n{stats_html}\n      </div>\n      <div class="notice"',
        html,
        count=1,
        flags=re.S,
    )
    return html


def validate(data: dict[str, Any]) -> None:
    required = ["page", "heroStats", "spots", "hotels", "route", "routeSegments", "spotInsights", "days", "foods", "prep"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError("缺少顶层字段：" + ", ".join(missing))
    ids = {item["id"] for item in data["spots"] + data["hotels"]}
    for day in data["days"]:
        for item in day.get("timeline", []):
            if len(item) == 3 and item[2] not in ids:
                raise ValueError(f"timeline 引用了不存在的地点 id：{item[2]}")


def patch_defaults(html: str, data: dict[str, Any]) -> str:
    page = data["page"]
    spots = data["spots"]
    places = data["spots"] + data["hotels"]
    selected = page.get("defaultSelectedSpotId") or (spots[0]["id"] if spots else "")
    from_id = page.get("defaultFromId") or (places[0]["id"] if places else "")
    to_id = page.get("defaultToId") or (places[min(1, len(places) - 1)]["id"] if places else "")
    html = re.sub(r'    let selectedId = ".*?";', f'    let selectedId = "{selected}";', html, count=1)
    html = re.sub(r'document\.getElementById\("fromSelect"\)\.value = ".*?";', f'document.getElementById("fromSelect").value = "{from_id}";', html, count=1)
    html = re.sub(r'document\.getElementById\("toSelect"\)\.value = ".*?";', f'document.getElementById("toSelect").value = "{to_id}";', html, count=1)
    return html


def render(data_path: Path, output_path: Path, template_path: Path) -> None:
    data = json.loads(data_path.read_text(encoding="utf-8"))
    validate(data)
    html = template_path.read_text(encoding="utf-8")
    html = patch_page_copy(html, data)
    for name in ["spots", "hotels", "route", "routeSegments", "spotInsights", "days", "foods", "prep"]:
        html = replace_const(html, name, data[name])
    html = patch_defaults(html, data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render trip webpage from trip-data.json.")
    parser.add_argument("data", help="trip-data.json")
    parser.add_argument("--output", "-o", required=True, help="输出 HTML 路径")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE), help="HTML 模板路径")
    args = parser.parse_args()
    render(Path(args.data), Path(args.output), Path(args.template))
    print(Path(args.output).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
