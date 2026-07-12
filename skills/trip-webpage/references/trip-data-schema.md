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
    "heroPoster": "assets/hero-poster.jpg",
    "heroAlt": "头图替代文本",
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
    "stayKicker": "Stay Shortlist",
    "stayTitle": "沿线住宿备选",
    "stayLead": "住宿备选说明",
    "embedStayImages": false,
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
        },
        {
          "src": "assets/wineglass_clip.mp4",
          "type": "video",
          "poster": "assets/wineglass_1.jpg",
          "caption": "Wineglass Bay Lookout｜酒杯湾视频"
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
  "staySections": [
    {
      "id": "sydney-stay",
      "label": "SYD",
      "dateLabel": "10·07—08",
      "title": "悉尼 / Mascot",
      "lead": "10 月 7 日入住、10 月 8 日离店，重点看晚到入住、机场接送、次日行李寄存与去 T1 的便利度。",
      "notices": [
        {
          "title": "公共交通备注",
          "text": "Mascot 附近住宿可坐 420 公交往返悉尼机场，作为机场班车以外的兜底方案；出发前再确认实时班次和候车点。"
        }
      ],
      "cards": [
        {
          "rank": "#1 · 机场班车优先",
          "name": "Silkari Urban CKS Sydney Airport Hotel",
          "score": "Booking 7.4 · 4,253 条点评",
          "price": "¥818",
          "priceNote": "当前含税总价 · 2 位成人 / 1 间房",
          "tags": [
            { "text": "机场班车收费", "style": "main" },
            "含早餐",
            "免费取消"
          ],
          "details": [
            { "label": "房型 / 床型", "value": "15㎡标准特大号床间；1 张超大号双人床，独立浴室" },
            { "label": "取消 / 付款", "value": "10 月 6 日前免费取消；到店前向住宿付款" },
            { "label": "早餐 / 洗衣", "value": "含早餐；住宿内有洗衣设施" },
            { "label": "停车", "value": "私人停车场；AUD 20 / 天" },
            { "label": "入住 / 离店", "value": "14:00 后入住；10:00 前离店" },
            { "label": "机场班车", "value": "接机服务：AUD 13 / 人，约每 40 分钟。\n送机服务：AUD 13 / 人，04:50 起约每 40 分钟。" }
          ],
          "note": "晚到时提前确认接机末班；若延误，直接改用出租车 / 网约车。",
          "warning": true,
          "recommended": true,
          "selected": false,
          "image": "assets/stay-sydney-silkari.jpg",
          "imageAlt": "Silkari Urban CKS Sydney Airport Hotel 房源首图",
          "imageCaption": "图片：Booking",
          "imageSource": "https://cf.bstatic.com/...",
          "url": "https://www.booking.com/...",
          "actionLabel": "前往 Booking 查看"
        }
      ]
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

Optional top-level key: `staySections`. When omitted or empty, the renderer removes the 住宿备选 section and its nav item.

Validation expectations:

- `page.defaultSelectedSpotId`, `page.defaultFromId`, and `page.defaultToId` must exist in `spots` or `hotels`; if omitted, the renderer will choose safe defaults.
- Set `page.timeZone` to an IANA timezone such as `Australia/Perth`, `Australia/Hobart`, `Pacific/Auckland`, or `Europe/Paris` when sunrise/sunset may need automatic lookup.
- Each `days[]` item must have `date`, `lat`, and `lng` for sunrise/sunset enrichment. Optional `sunLabel` controls the prefix in rendered fields, for example `Rottnest 06:03`.
- If the itinerary document does not include sunrise/sunset times, run `scripts/enrich_sun_times.py trip-data.json --tzid <timezone>` before rendering. The script fills only missing values unless `--overwrite` is passed.
- `page.heroImage` accepts images and videos. Image paths render as the default full-bleed hero image; `.mp4`, `.webm`, `.mov`, and `.m4v` paths render as muted autoplay looping hero video. Optional `page.heroPoster` is used as the video poster frame, and optional `page.heroAlt` becomes the image alt text. Keep media paths local under `assets/` by final render when possible.
- For foreign attractions and hotels, `name` is the English official/common name and `zh` is the Chinese name. The template displays them as `name｜zh`, for example `Wineglass Bay Lookout｜酒杯湾观景台`.
- Timeline rows that reference foreign spots should use the same `English｜中文` display style, for example `["09:00-11:00", "Wineglass Bay Lookout｜酒杯湾观景台", "wineglass"]`.
- For domestic Chinese attractions, use Chinese in `name`; omit `zh` unless a bilingual display is desired.
- Ratings are integers from 1 to 10.
- Coordinates are decimal degrees.
- Timeline item arrays must have 2 or 3 values.
- A timeline row should contain only one scenic spot reference. Split multi-spot strings into multiple rows when those spots each deserve map/detail interaction.
- `routeSegments[].mode` can be `drive`, `ferry`, `walk`, or `flight`.
- `spot.image` should point to a local `assets/...` image by final render and remains the primary/fallback cover image. During drafting it may temporarily be an extracted document image path or a remote URL, but run `localize_trip_images.py` before publishing.
- `spot.images` is optional and enables the detail-panel media carousel. Use it when a spot has multiple useful images or videos; strings are accepted for images, and object entries may include `src`, `type`, `poster`, `caption`, `photoSource`, and `photoCredit`. Set `type: "video"` for video entries, or use `.mp4`, `.webm`, or `.mov` paths for automatic detection. Put a still image first when possible and keep `spot.image` equal to the first cover image for compatibility.
- Use `imageSourceType: "document"` when the image came from the provided itinerary document. Use `"web"` or `"wikipedia"` when it was found online and downloaded locally.
- `staySections[]` renders the dedicated lodging shortlist section. Use one section per lodging city/area and one card per candidate property.
- Keep accommodation card `details` labels consistent when possible: `房型 / 床型`, `取消 / 付款`, `早餐 / 洗衣`, `停车`, `入住 / 离店`, `机场班车`.
- For airport shuttle summaries, use the format `无班车。` or split pickup/dropoff inside the `机场班车` detail value: `接机服务：价格 + 时间` and `送机服务：价格 + 时间`; prices should include the currency such as `AUD`.
- Put public-transport fallbacks such as airport buses in `staySections[].notices`, not inside each room card unless only one property is affected.
- `staySections[].cards[].tags` accepts strings or objects like `{ "text": "当前已选", "style": "confirmed" }`; supported styles are `main` and `confirmed`.
- `staySections[].cards[].image` may point to a local `assets/...` image. Set `page.embedStayImages: true` or run `render_trip_webpage.py --embed-stay-images` when the final HTML must carry accommodation images as data URIs for single-file upload environments.
- For an already-rendered HTML page that will be uploaded to Yuque as a single file, run `scripts/embed_stay_images_in_html.py <trip-folder>/index.html` so lodging images are embedded directly in `staySections[].cards[].image`; do not leave them as `assets/stay-*` paths.
- To get lodging images, use user-provided local images first. Otherwise, when a Booking/Airbnb/hotel detail page or wishlist is available, open the property page, take the visible lead/gallery photo for that exact property, save it into the trip folder’s `assets/` directory with a descriptive `stay-...` filename, and set `image`, `imageAlt`, `imageCaption`, and optional `imageSource`.
- Avoid generic destination photos for lodging cards; the image should represent the actual property or room listing.
