import os
from dolby import DolbyImage, DolbyAudio, DolbyVideo, DolbySpeech, DolbyChat
from dolby import QueryType, Language


def image():
    image = DolbyImage(path='assets')
    image.download(query='golden retriever', count=4)


def audio():
    audio = DolbyAudio(path='assets')
    audio.download(query='kanye west jesus is lord jesus is lord',
                   query_type=QueryType.NAME)
    # audio.transcribe(
    #     file='/Users/gautam_veldanda/dolby/src/assets/Jesus Is Lord-rns_n82HiMo.mp3')


def video():
    video = DolbyVideo(path='assets')
    video.download(query='kanye west jesus is lord jesus is lord',
                   query_type=QueryType.NAME)


def text():
    speech = DolbySpeech(path='assets')
    speech.translate(query='Hello, How are you?', language=Language.SPANISH)
    speech.speak(query='Hello, How are you?')


def chat():
    chat = DolbyChat(email=os.environ['EMAIL'], password=os.environ['PASSWORD'])
    chat.talk(speak=True)
    # res = chat.ask(query='Hello, How are you?')
    # print(res)


# image()
# audio()
# video()
# text()
# chat()