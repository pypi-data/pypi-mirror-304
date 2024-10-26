# YouTube Subtitles Fetcher

`YouTube Subtitles Fetcher` is a command-line tool that retrieves subtitles (with optional translations) from YouTube videos. This tool is ideal for quickly extracting YouTube transcripts with support for multiple languages.

## Features

- Fetches subtitles for a given YouTube video URL
- Supports translations into a specified language (if available)
- Command-line interface for easy integration into scripts or workflows

## Installation

First, install the package via pip:

```bash
pip install ytb2subtitles
```

## Usage

Use the command-line tool to fetch subtitles by providing a YouTube URL and optionally, a language code.

Command-Line Example

To retrieve subtitles from a YouTube video:


ytb2subtitles https://www.youtube.com/watch?v=example_video_id

To retrieve subtitles in a specific language:

ytb2subtitles https://www.youtube.com/watch?v=example_video_id --language en

Code Example

You can also import this tool as a module in your Python code:

from ytb2subtitles import get_subtitles

url = "https://www.youtube.com/watch?v=example_video_id"
subtitles = get_subtitles(url, lang="en")
print(subtitles)

Command-Line Arguments

	•	url (required): The YouTube video URL.
	•	--language or --lang (optional): The language code for subtitles (default is the original language).

Requirements

	•	Python 3.x
	•	pytube
	•	youtube-transcript-api

Contributing

We welcome contributions! If you find a bug or have an idea for a feature, please open an issue or submit a pull request.

License

This project is licensed under the MIT License.
