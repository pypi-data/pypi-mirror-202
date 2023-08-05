import requests
import openai
from pathlib import Path
from icrawler.builtin import GoogleImageCrawler
from .constants import *
from .override import *
import logging
logging.basicConfig(level=logging.WARNING)


class DolbyImage:
    def init(self, path, OPENAI_API_KEY=None, PEEXELS_API_KEY=None):
        """
        Initialize DolbyImage object with the path to the directory where the image will be stored,
        and the API keys for OpenAI and Pexels APIs if needed.

        python
        Copy code
            Args:
            - path: str, the path to the directory where the downloaded image will be stored
            - OPENAI_API_KEY: str, optional, API key for OpenAI API
            - PEEXELS_API_KEY: str, optional, API key for Pexels API
        """
        self.path = path
        self.openai_api_key = OPENAI_API_KEY
        self.pexels_api_key = PEEXELS_API_KEY
        Path(path).mkdir(parents=True, exist_ok=True)

    def __openai__(self, query: str):
        """
        Private method to download an image using OpenAI API.

        Args:
        - query: str, the search query for the image
        """
        openai.api_key = self.openai_api_key
        response = openai.Image.create(
            prompt=query,
            size="full",
        )
        url = response["data"][0]["url"]  # type: ignore
        data = requests.get(url).content
        with open(f"{self.path}/image.png", 'wb') as handler:
            handler.write(data)

    def __pexels__(self, query: str):
        """
        Private method to download an image using Pexels API.

        Args:
        - query: str, the search query for the image
        """
        pass

    def __google__(self, query: str):
        """
        Private method to download an image using Google Image search.

        Args:
        - query: str, the search query for the image
        """
        self.gc = GoogleImageCrawler(downloader_cls=FileName, storage={
            'root_dir': f"{self.path}"})
        self.gc.crawl(keyword=query, max_num=1,
                      file_idx_offset='auto')  # type: ignore

    def download(self, query: str, source: ImageSource = ImageSource.GOOGLE):
        """
        Download an image using the specified source and query.

        Args:
        - query: str, the search query for the image
        - source: ImageSource, optional, the source to download the image from, default is ImageSource.GOOGLE
        """
        if source == ImageSource.GOOGLE:
            self.__google__(query)
        elif source == ImageSource.OPENAI:
            self.__openai__(query)
        elif source == ImageSource.PEXELS:
            self.__pexels__(query)
