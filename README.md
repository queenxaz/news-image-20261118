[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/queenxaz/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/queenxaz/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

# THE WORLD TODAY — Wednesday 18 November 2026

Entry for the make.fun competition
[news-image-20261118](https://make.fun/bounty/news-image-20261118)
("Sum up 18 November's world news in one image", $250, 50 places paid,
closes 2026-11-20T00:00:00Z).

## The image

A dense newspaper front page, drawn programmatically at build time and
embedded in `main.py` so the entrypoint is deterministic and stdlib-only:

- Masthead **THE WORLD TODAY** with the date **WEDNESDAY 18 NOVEMBER 2026**.
- Lead story: **Ukraine strikes Kerch Bridge — road span collapses**
  (second day of strikes; part of the road span fell into the strait).
- 20 numbered stories in total, covering the day's biggest news across
  regions and beats: the US strike on an Iranian missile site on Qeshm
  Island and Iranian drones fired at Bahrain and Kuwait; Ebola in DR Congo
  more than doubling to 11,000 cases and 5,400 dead; the US losing
  measles-free status after 26 years; the Trump–Xi–Putin trilateral summit
  in Shenzhen; Democrats winning the Alaska Senate seat; a Russian military
  plane crash in Siberia; earthquakes in Papua New Guinea and Romania;
  cold and floods in Gaza; Eisenkot tapped to form Israel's government;
  Cyclone Xavier and Cyclone Akvan; the world court ruling on Myanmar;
  MS Dhoni retiring from the IPL; French cost-of-living protests; a
  cyber-attack on supermarket freezers in seven European countries; US
  figures on Venezuelan oil and mineral revenue; the 330-month sentence in
  the plot to kill Trump; the UK climate body's EV warning; GTA VI's
  midnight release; and Xi on trade barriers at APEC.
- A **WHERE IT HAPPENED** world-map panel marking the day's flashpoints.
- A **MARKETS** box with the day's closes (CAC 40, DAX, FTSE 100, S&P 500,
  Nasdaq, Nikkei 225, Hang Seng, VIX, Brent, Gold).
- Sources line: BBC / Reuters / Al Jazeera / AP / NPR.

## How it works

- `render.py` — build-time script (PIL, DejaVu fonts) that draws the
  1024×1024 front page and saves it as `entry.jpg` (JPEG, quality 85).
- `main.py` — the entrypoint. Python 3 standard library only: it decodes
  the embedded base64 image and writes it to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). It never
  deletes the output directory, makes no network calls, and writes the
  same bytes on every run.

## Verify

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 -c "from PIL import Image; im = Image.open('out/entry.png'); print(im.size, im.format)"
```

## License

MIT — see [LICENSE](LICENSE).
