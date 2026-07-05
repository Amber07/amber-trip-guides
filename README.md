# 旅行攻略网页

这个工作区用于存放多个独立的旅行攻略网页。

## 目录结构

```text
.
├── index.html                         # 攻略索引页
├── vercel.json                        # Vercel 路由配置
├── tasmania-20261002-1007/
│   ├── index.html                     # 塔斯马尼亚攻略正文
│   └── assets/                        # 该攻略自己的图片资源
└── perth-20260925-1001/
    ├── index.html                     # 珀斯 / 西澳北线攻略正文
    └── assets/                        # 珀斯攻略自己的图片资源
```

## 新增一个攻略

1. 在根目录下新建一个攻略目录，例如 `perth-20260925-1001/`。
2. 把攻略页面保存为该目录下的 `index.html`。
3. 把这个攻略用到的本地图片放到该目录自己的 `assets/` 下。
4. 在根目录 `index.html` 里新增一张攻略卡片。
5. 如果需要短链接，在 `vercel.json` 里新增 rewrite。

每个攻略目录独立维护自己的资源；根目录只放索引页、路由配置、说明文档，以及各个攻略目录。

## 自动生成攻略网页

`skills/trip-webpage/` 是从“塔州东海岸 6 日游”沉淀出来的 Codex skill。提供 PDF、Word、Markdown、Excel、CSV 或文本行程后，先抽取文档内容和文档图片，再整理为 `trip-data.json`，补齐 Wikipedia 景点介绍，把网络图片下载到本地，最后用塔州同款模板生成独立的攻略网页。

核心命令：

```bash
python3 skills/trip-webpage/scripts/extract_trip_text.py 行程文件.pdf --output /tmp/trip-source.txt --media-dir 新攻略目录/assets --media-path-prefix assets
python3 skills/trip-webpage/scripts/enrich_from_wikipedia.py trip-data.json
python3 skills/trip-webpage/scripts/enrich_sun_times.py trip-data.json --tzid Australia/Perth
python3 skills/trip-webpage/scripts/localize_trip_images.py trip-data.json --assets-dir 新攻略目录/assets
python3 skills/trip-webpage/scripts/render_trip_webpage.py trip-data.json --output 新攻略目录/index.html
```

已有攻略网页也可以用这个 skill 更新：先审计当前页面缺少哪些模板能力，再按模板补齐当前 HTML。

```bash
python3 skills/trip-webpage/scripts/audit_trip_webpage.py 已有攻略目录/index.html
```
