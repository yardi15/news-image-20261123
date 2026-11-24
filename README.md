# The World in One Day: 23 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261123-red)](https://make.fun/bounty/news-image-20261123)
[![Python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A newspaper front page that sums up the world news of Monday 23 November 2026 in a single 1024×1024 image. Built for the make.fun bounty [news-image-20261123](https://make.fun/bounty/news-image-20261123).

## The day

- **Nvidia brings back Jensen Huang** as CEO, 11 days after he quit; shares jump 31.5%, their best day since 2003.
- **Iran claims it shot down a US drone** east of the Strait of Hormuz and defies the US naval blockade; Washington sanctions 20-plus exchange houses.
- **The EU proposes its 22nd sanctions package** on Russia: 60 banks off SWIFT, 70-plus shadow-fleet ships listed.
- **India pledges $1.62bn to Nepal**; the Dymer toll rises to 11; the UN and US condemn the Khartoum drone strikes.

38 stories across 8 regions and 13 fields, every card carrying a status label (CONFIRMED / OFFICIAL / REPORTED / CLAIM / PENDING) with a legend, a numbered-pin world map, a UTC timeline, a day-in-numbers strip, and a DATE CHECK box for stories from other days.

## What's on the page

- **Masthead** — the date, the story/region/field counts, and the press time in UTC.
- **Three leads** — Nvidia, Iran/Hormuz, and the EU sanctions package, each with its own illustration, a 2–4 word banner, and a numeric callout.
- **Ten briefs** — one distinct illustration per story, from the India–Nepal package to the Wellington Test draw.
- **Also on** — 25 more stories, one line each, with region colour, source, and status.
- **The world** — a dot-grid map with 13 numbered, region-coloured pins.
- **Monday in six moments** — the day's timeline in UTC.
- **Date check** — events from 20–22 November, plus things that have not happened yet, deliberately left out so nothing from another day is sold as Monday's news.

## How it works

`main.py` draws the whole page from scratch with the Python standard library only — a small bitmap font, a hand-rolled PNG encoder, and one distinct vector illustration per story. No network, no clock, no randomness.

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Verify

The program runs twice and writes byte-identical output:

```sh
MAKEFUN_OUTPUT_DIR=out1 python3 main.py
MAKEFUN_OUTPUT_DIR=out2 python3 main.py
sha256sum out1/entry.png out2/entry.png
```

`entry.png` is a PNG, 1024×1024, under 1 MiB.

## Sources

Reuters, AP, AFP, BBC, CNN, European Commission, US Treasury, UN. Wires read to 00:30 UTC.

## License

MIT — see [LICENSE](LICENSE).
