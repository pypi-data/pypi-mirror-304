import argparse
import re
from pytube.extract import video_id
from youtube_transcript_api import YouTubeTranscriptApi


def get_original(transcript_list):
    """Return the language code of the first generated transcript."""
    return next((transcript.language_code for transcript in transcript_list if transcript.is_generated), '')


def lang_available(transcript_list, lang):
    """Check if a specified language is available in the transcripts' translation languages."""
    return any(
        lang in (transcript_lang.get('language_code') for transcript_lang in transcript.translation_languages)
        for transcript in transcript_list
    )


def get_movie_id(url: str) -> str:
    try:
        movie_id = video_id(url)
    except Exception as e:
        return ''
    return movie_id


def get_subtitles(url, lang='') -> list:
    movie_id = get_movie_id(url)
    if not movie_id:
        return []

    transcript_list = YouTubeTranscriptApi.list_transcripts(movie_id)
    if not transcript_list:
        return []

    original_lang = get_original(transcript_list)
    if not lang:
        lang = original_lang

    if lang == original_lang:
        return transcript_list.find_transcript([original_lang]).fetch()

    if not lang_available(transcript_list, lang):
        return []

    return transcript_list.find_transcript([original_lang]).translate(lang).fetch()


def main():
    parser = argparse.ArgumentParser(description="Process a URL.")
    parser.add_argument("url", type=str, help="The URL to process")
    parser.add_argument(
        "--language", "--lang",
        type=str,
        default="",
        help="Language code for subtitles (default is '')"
    )
    args = parser.parse_args()

    if not re.match(r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+", args.url):
        return

    subtitles = get_subtitles(args.url, args.language)
    print(subtitles)


if __name__ == "__main__":
    main()