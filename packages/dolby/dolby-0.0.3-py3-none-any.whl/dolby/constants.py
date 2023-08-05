from enum import Enum

# This module defines several enums and constants used across different scripts

# The URLs used to search for and access YouTube videos
YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query="
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v="

# The arguments used to download the best quality video and audio streams from YouTube
VIDEO_ARGS = "-f 'bestvideo[ext=mp4][vcodec!^=av0][vcodec!^=av1]+bestaudio[ext=m4a]/mp4/best' --recode-video mp4"
AUDIO_ARGS = "-f bestaudio --extract-audio --audio-format mp3 --audio-quality 0"

# The filter applied to YouTube search results to only show videos
YOUTUBE_FILTER = 'sp=EgIgAQ%253D%253D'

# Redirect stdout and stderr to /dev/null to hide the output of the download commands
HIDE_OUTPUT = '>/dev/null 2>&1'

# Enumerations used to represent different query types, media formats, image sources, and audio/video sources


class QueryType(Enum):
    URL = 'URL'
    NAME = 'NAME'


class MediaFormat(Enum):
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"


class ImageSource(Enum):
    GOOGLE = 'GOOGLE'
    OPENAI = 'OPENAI'
    PEXELS = 'PEXELS'


class AudioSource(Enum):
    YOUTUBE = 'YOUTUBE'
    SOUNDCLOUD = 'SOUNDCLOUD'
    SPOTIFY = 'SPOTIFY'


class VideoSource(Enum):
    YOUTUBE = 'YOUTUBE'
