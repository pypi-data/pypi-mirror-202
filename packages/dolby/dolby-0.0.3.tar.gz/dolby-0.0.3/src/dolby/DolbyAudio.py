from pathlib import Path
from .constants import *
from .YouTube import YouTube


class DolbyAudio:
    """
    Class representing a Dolby Audio instance that can download audio from various sources.
    """

    def __init__(self, path: str):
        """
        Constructor method that initializes the path for storing downloaded audio files.

        Args:
            path (str): The path to the directory where downloaded audio files will be saved.
        """
        self.path = path
        Path(path).mkdir(parents=True, exist_ok=True)

    def __youtube__(self, query: str, query_type: QueryType = QueryType.NAME):
        """
        Private method that downloads audio from YouTube given a query string.

        Args:
            query (str): The query string to search for on YouTube.
            query_type (QueryType): The type of query string (name or URL).

        Raises:
            Exception: If the query string is invalid or if no audio files are found.

        Returns:
            None
        """
        youtube = YouTube(self.path, MediaFormat.AUDIO)
        youtube.make(query, query_type)

    def download(self, query: str, source: AudioSource = AudioSource.YOUTUBE, query_type: QueryType = QueryType.NAME):
        """
        Public method that downloads audio from the given source.

        Args:
            query (str): The query string to search for on the specified audio source.
            source (AudioSource): The audio source to download from (e.g. YouTube, SoundCloud, Spotify).
            query_type (QueryType): The type of query string (name or URL).

        Raises:
            Exception: If the audio source is invalid or if no audio files are found.

        Returns:
            None
        """
        if source == AudioSource.YOUTUBE:
            self.__youtube__(query, query_type)
