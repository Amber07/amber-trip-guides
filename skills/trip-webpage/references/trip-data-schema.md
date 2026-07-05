# Trip Data Schema

Create one UTF-8 JSON file with this shape:

```json
{
  "page": {
    "title": "塔州东海岸 6 日游",
    "htmlTitle": "塔斯马尼亚 2026.10.2-10.7 行程攻略",
    "description": "页面 meta description",
    "eyebrow": "Tasmania East Coast · 2026.10.02-10.07",
    "heroTitle": "塔州东海岸 6 日游",
    "heroCopy": "一段 50-120 字的路线概述",
    "heroImage": "assets/hero.jpg",
    "notice": "重要提醒，可为空",
    "footer": "塔斯马尼亚东海岸旅行攻略 · 2026.10.02-10.07",
    "mapKicker": "Route Map",
    "mapTitle": "路线地图标题",
    "mapLead": "地图说明",
    "itineraryKicker": "Daily Plan",
    "itineraryTitle": "每日行程安排",
    "itineraryLead": "每日行程说明",
    "foodKicker": "Food",
    "foodTitle": "沿线餐饮与补给",
    "foodLead": "餐饮补给说明",
    "prepKicker": "Before Departure",
    "prepTitle": "需要提前预定和准备的东西",
    "prepLead": "准备清单说明",
    "defaultSelectedSpotId": "main_spot_id",
    "defaultFromId": "start_spot_id",
    "defaultToId": "end_spot_id",
    "timeZone": "Australia/Hobart",
    "sunTimeSource": "https://sunrise-sunset.org/api"
  },
  "heroStats": [
    { "value": "6 日", "label": "10/2-10/7 游玩" }
  ],
  "spots": [
    {
      "id": "wineglass",
      "name": "Wineglass Bay Lookout",
      "zh": "酒杯湾观景台",
      "type": "spot",
      "day": 2,
      "time": "10/3 09:00-11:00",
      "lat": -42.1232,
      "lng": 148.2973,
      "stay": "1.5-2 小时",
      "image": "https://...",
      "images": [
        "assets/wineglass_1.jpg",
        {
          "src": "assets/wineglass_2.jpg",
          "caption": "Wineglass Bay Lookout｜酒杯湾观景台",
          "photoSource": "https://...",
          "photoCredit": "作者 · 授权"
        }
      ],
      "imageSourceType": "document|web|wikipedia|local|fallback",
      "photoSource": "https://...",
      "photoCredit": "作者 · 授权",
      "wikipediaTitle": "Wineglass Bay",
      "wikipediaUrl": "https://en.wikipedia.org/wiki/Wineglass_Bay",
      "features": ["Freycinet", "经典观景台", "轻徒步"],
      "intro": "景点简介",
      "play": "怎么玩",
      "note": "注意事项",
      "ratings": { "nature": 10, "culture": 3, "weather": 8, "stamina": 6 }
    }
  ],
  "hotels": [
    {
      "id": "stay_hobart",
      "name": "Hobart Stay",
      "zh": "霍巴特住宿",
      "type": "hotel",
      "day": 5,
      "lat": -42.8821,
      "lng": 147.3272
    }
  ],
  "route": ["spot_id_1", "spot_id_2"],
  "routeSegments": [
    { "mode": "drive", "ids": ["spot_id_1", "spot_id_2"] }
  ],
  "spotInsights": {
    "wineglass": {
      "unique": "景观特色",
      "history": "背景 / 历史"
    }
  },
  "days": [
    {
      "day": 1,
      "date": "2026-10-02",
      "title": "Launceston → Bay of Fires → Bicheno",
      "base": "Bicheno",
      "lat": -41.873,
      "lng": 148.302,
      "sunLabel": "Bicheno",
      "sunrise": "05:42",
      "sunset": "18:12",
      "alerts": ["提前下离线地图"],
      "transport": "当天交通说明",
      "timeline": [
        ["08:30", "从 Launceston 出发"],
        ["12:00-14:00", "Binalong Bay｜比纳龙湾午餐和海滩散步", "binalong"]
      ]
    }
  ],
  "foods": [
    {
      "area": "Coles Bay",
      "type": "徒步后午餐",
      "title": "Freycinet 午餐",
      "text": "餐饮建议",
      "budget": "AUD 20-45"
    }
  ],
  "prep": [
    {
      "title": "重点预订",
      "items": ["Maria Island Ferry", "Bicheno Penguin Tour"]
    }
  ]
}
```

Required top-level keys: `page`, `heroStats`, `spots`, `hotels`, `route`, `routeSegments`, `spotInsights`, `days`, `foods`, `prep`.

Validation expectations:

- `page.defaultSelectedSpotId`, `page.defaultFromId`, and `page.defaultToId` must exist in `spots` or `hotels`; if omitted, the renderer will choose safe defaults.
- Set `page.timeZone` to an IANA timezone such as `Australia/Perth`, `Australia/Hobart`, `Pacific/Auckland`, or `Europe/Paris` when sunrise/sunset may need automatic lookup.
- Each `days[]` item must have `date`, `lat`, and `lng` for sunrise/sunset enrichment. Optional `sunLabel` controls the prefix in rendered fields, for example `Rottnest 06:03`.
- If the itinerary document does not include sunrise/sunset times, run `scripts/enrich_sun_times.py trip-data.json --tzid <timezone>` before rendering. The script fills only missing values unless `--overwrite` is passed.
- `page.heroImage` accepts images and videos. Image paths render as the default full-bleed hero image; `.mp4`, `.webm`, and `.mov` paths render as muted autoplay looping hero video. Keep the path local under `assets/` by final render when possible.
- For foreign attractions and hotels, `name` is the English official/common name and `zh` is the Chinese name. The template displays them as `name｜zh`, for example `Wineglass Bay Lookout｜酒杯湾观景台`.
- Timeline rows that reference foreign spots should use the same `English｜中文` display style, for example `["09:00-11:00", "Wineglass Bay Lookout｜酒杯湾观景台", "wineglass"]`.
- For domestic Chinese attractions, use Chinese in `name`; omit `zh` unless a bilingual display is desired.
- Ratings are integers from 1 to 10.
- Coordinates are decimal degrees.
- Timeline item arrays must have 2 or 3 values.
- A timeline row should contain only one scenic spot reference. Split multi-spot strings into multiple rows when those spots each deserve map/detail interaction.
- `routeSegments[].mode` can be `drive`, `ferry`, `walk`, or `flight`.
- `spot.image` should point to a local `assets/...` file by final render and remains the primary/fallback image. During drafting it may temporarily be an extracted document image path or a remote URL, but run `localize_trip_images.py` before publishing.
- `spot.images` is optional and enables the detail-panel carousel. Use it when a spot has multiple useful images; strings are accepted, and object entries may include `src`, `caption`, `photoSource`, and `photoCredit`. Put the primary image first and keep `spot.image` equal to that first `src` for compatibility.
- Use `imageSourceType: "document"` when the image came from the provided itinerary document. Use `"web"` or `"wikipedia"` when it was found online and downloaded locally.
