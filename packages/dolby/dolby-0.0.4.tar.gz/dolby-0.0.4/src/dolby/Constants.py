YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query="
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v="

VIDEO_ARGS = "-f 'bestvideo[ext=mp4][vcodec!^=av0][vcodec!^=av1]+bestaudio[ext=m4a]/mp4/best' --recode-video mp4"
AUDIO_ARGS = "-f bestaudio --extract-audio --audio-format mp3 --audio-quality 0"

YOUTUBE_FILTER = 'sp=EgIgAQ%253D%253D'

HIDE_OUTPUT = '>/dev/null 2>&1'
