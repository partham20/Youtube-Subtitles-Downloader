# YouTube Subtitles Downloader

A small desktop app that pulls the transcript for any YouTube video and saves it as **SRT** (with timestamps) or **TXT** (clean prose).

## How it works

- The video ID is extracted from whatever URL form you paste (`?v=` or a `/`-style short link)
- `youtube-transcript-api` fetches the transcript without needing an API key or login
- **SRT** output keeps the original cue timings
- **TXT** output runs the text through NLTK's `sent_tokenize` so the result reads as sentences rather than caption fragments
- A Tkinter file dialog picks the save location, and errors (bad URL, no transcript available) surface as message boxes

## Requirements

```bash
pip install youtube-transcript-api nltk
```

Tkinter ships with most Python installations. The `punkt` tokenizer model is downloaded automatically on first run.

## Usage

```bash
python app.py
```

1. Paste a YouTube URL
2. Choose **SRT** or **TXT**
3. Click download and pick where to save

## Files

| File | Purpose |
|------|---------|
| `app.py` | The whole application — GUI, transcript fetch, SRT/TXT writers |

## Note

Only works for videos that have captions available (auto-generated counts). Videos with captions disabled will report a fetch error.

## See also

[Youtube-Video-Downloader](https://github.com/partham20/Youtube-Video-Downloader) — the companion video/audio downloader.
