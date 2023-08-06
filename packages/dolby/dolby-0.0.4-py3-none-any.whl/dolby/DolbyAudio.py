import os
import speech_recognition as sr
from pathlib import Path
from .ConstantsDX import *
from .Constants import *
from .YouTube import YouTube
from pydub import AudioSegment
from pydub.silence import split_on_silence


class DolbyAudio:
    """
    Class representing a Dolby Audio instance that can download audio from various sources.
    """

    def __init__(self, path: str = '.') -> None:
        """
        Constructor method that initializes the path for storing downloaded audio files.

        Args:
            path(str): The path to the directory where downloaded audio files will be saved.
        """
        self.path = path
        Path(path).mkdir(parents=True, exist_ok=True)

    def __youtube__(self, query: str, query_type: QueryType = QueryType.NAME) -> None:
        """
        Private method that downloads audio from YouTube given a query string.

        Args:
            query(str): The query string to search for on YouTube.
            query_type(QueryType): The type of query string(name or URL).

        Raises:
            Exception: If the query string is invalid or if no audio files are found.

        Returns:
            None
        """
        youtube = YouTube(self.path, MediaFormat.AUDIO)
        youtube.make(query, query_type)

    def download(self, query: str, source: AudioSource = AudioSource.YOUTUBE, query_type: QueryType = QueryType.NAME) -> None:
        """
        Public method that downloads audio from the given source.

        Args:
            query(str): The query string to search for on the specified audio source.
            source(AudioSource): The audio source to download from (e.g. YouTube, SoundCloud, Spotify).
            query_type(QueryType): The type of query string(name or URL).

        Raises:
            Exception: If the audio source is invalid or if no audio files are found.

        Returns:
            None
        """
        if source == AudioSource.YOUTUBE:
            self.__youtube__(query, query_type)

    def transcribe(self, file: str) -> str:
        """
        Splitting the large audio file into chunks
        and apply speech recognition on each of these chunks

        Args:
            file(str): The path to the audio file to transcribe.

        Returns:
            str: The transcribed text.
        """
        recognizer = sr.Recognizer()
        sound = AudioSegment.from_mp3(file)
        chunks = split_on_silence(sound,
                                  min_silence_len=500,
                                  silence_thresh=sound.dBFS-14,
                                  keep_silence=500,
                                  )
        folder_name = f"{self.path}/audio-chunks"
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        transcription = ""
        for i, chunk in enumerate(chunks, start=1):
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            chunk.export(chunk_filename, format="wav")
            with sr.AudioFile(chunk_filename) as source:
                audio = recognizer.record(source)
                try:
                    tmp = recognizer.recognize_google(audio)
                except sr.UnknownValueError as e:
                    pass
                else:
                    transcription += tmp + ' '  # type: ignore
        os.system(f"rm -rf {folder_name}")
        return transcription
