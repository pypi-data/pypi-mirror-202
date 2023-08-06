import os
import re

import requests
from bs4 import BeautifulSoup

from .ConstantsDX import *
from .Constants import *


class YouTube:
    """
    This class represents a YouTube instance that can download audio or video files from YouTube.

    Attributes:
    -----------
    path : str
        The path where the downloaded files will be saved.
    format : MediaFormat
        The format of the downloaded files. It can be either MediaFormat.AUDIO or MediaFormat.VIDEO.
    """

    def __init__(self, path: str = '.', format: MediaFormat = MediaFormat.AUDIO) -> None:
        self.path = path
        self.format = format

    def __url__(self, query: str) -> str:
        """
        Private method that returns the URL of the video to be downloaded based on the query.

        Parameters:
        -----------
        query : str
            The query to search for the video on YouTube.

        Returns:
        --------
        str
            The URL of the video to be downloaded.
        """
        soup = BeautifulSoup(requests.get(
            f"{YOUTUBE_SEARCH_URL}{query.replace(' ', '+')}&{YOUTUBE_FILTER}").text, 'html.parser')
        match = re.search(r"watch\?v=(\S{11})", soup.prettify())
        video_id = match.group(1) if match else None
        return f"{YOUTUBE_VIDEO_URL}{video_id}"

    def make(self, query: str, query_type: QueryType = QueryType.NAME) -> None:
        """
        Public method that downloads the video or audio file from YouTube based on the query.

        Parameters:
        -----------
        query : str
            The query to search for the video on YouTube.
        query_type : QueryType
            The type of the query. It can be either QueryType.NAME or QueryType.URL.

        Raises:
        -------
        Exception
            If the format is not supported.
        """
        query = self.__url__(query) if query_type == QueryType.NAME else query
        CMD = ' '.join([f'cd {self.path}', '&&', 'youtube-dl'])
        if self.format == MediaFormat.AUDIO:
            CMD = ' '.join([CMD, AUDIO_ARGS])
        elif self.format == MediaFormat.VIDEO:
            CMD = ' '.join([CMD, VIDEO_ARGS])
        else:
            raise Exception("Unsupported format.")
        CMD = ' '.join([CMD, query, HIDE_OUTPUT])
        os.system(CMD)
