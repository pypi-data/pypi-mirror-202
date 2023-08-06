from pathlib import Path
from .ConstantsDX import *
from .Constants import *
from .YouTube import YouTube


class DolbyVideo:
    """
    Class representing a Dolby Video instance that can download video from various sources.
    """

    def __init__(self, path: str = '.') -> None:
        """
        Constructor method that initializes the path for storing downloaded video files.

        Args:
            path (str): The path to the directory where downloaded video files will be saved.
        """
        self.path = path
        Path(path).mkdir(parents=True, exist_ok=True)

    def __youtube__(self, query: str, query_type: QueryType = QueryType.NAME) -> None:
        """
        Private method that downloads video from YouTube given a query string.

        Args:
            query (str): The query string to search for on YouTube.
            query_type (QueryType): The type of query string (name or URL).

        Raises:
            Exception: If the query string is invalid or if no video files are found.

        Returns:
            None
        """
        youtube = YouTube(self.path, MediaFormat.VIDEO)
        youtube.make(query, query_type)

    def download(self, query: str, source: AudioSource = AudioSource.YOUTUBE, query_type: QueryType = QueryType.NAME) -> None:
        """
        Public method that downloads video from the given source.

        Args:
            query (str): The query string to search for on the specified video source.
            source (AudioSource): The video source to download from (e.g. YouTube, Vimeo).
            query_type (QueryType): The type of query string (name or URL).

        Raises:
            Exception: If the video source is invalid or if no video files are found.

        Returns:
            None
        """
        if source == AudioSource.YOUTUBE:
            self.__youtube__(query, query_type)
