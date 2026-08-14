# Universal Downloader Bot

A Telegram bot that downloads video and audio from Instagram and YouTube links — no watermarks, no ads.

<p>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=flat-square&logo=telegram&logoColor=white">
  <img src="https://img.shields.io/badge/status-source%20upload%20in%20progress-orange?style=flat-square">
</p>

> **Status:** the bot runs privately; the source is being cleaned of credentials before it is published here.

---

## Features

- Instagram — Reels, posts, IGTV
- YouTube — video (up to 1080p) and audio-only (MP3)
- Async download queue, so several users are served concurrently
- Automatic cleanup of temporary files
- Uzbek / English interface
- Per-user rate limiting

## How it works

```
User sends link
      |
      v
 URL parser --> platform router --> yt-dlp extractor
                                          |
                                    format selection
                                          |
                                    download -> temp
                                          |
                              size check -> Telegram upload
                                          |
                                      cleanup
```

## Planned repository layout

```
bot.py              # aiogram entrypoint, handlers
downloaders/
  instagram.py
  youtube.py
utils/
  validators.py     # URL parsing and platform detection
  cleanup.py
locales/            # uz / en interface strings
requirements.txt
```

## Configuration

| Variable | Description |
|---|---|
| `BOT_TOKEN` | Token from BotFather |
| `MAX_FILE_MB` | Upload size cap (Telegram limit: 50 MB for bots) |
| `DOWNLOAD_DIR` | Temporary download path |
| `ADMIN_ID` | Telegram user ID that receives error reports |

## Legal note

Intended for downloading content you own or that is licensed for reuse. Users are responsible for complying with the terms of service of the source platform and with applicable copyright law.

## Author

**Mardonbek Sulaymonqulov** — AI / Computer Vision Engineer
[GitHub](https://github.com/Mardonaka05) · mardonbeksulaymonqulov156@gmail.com
