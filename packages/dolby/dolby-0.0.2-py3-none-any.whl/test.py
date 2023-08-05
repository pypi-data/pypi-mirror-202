from dolby import *


def test_image():
    image = DolbyImage(path='assets')
    image.download(query='kanye west and elon musk')


def test_audio():
    audio = DolbyAudio(path='assets')
    audio.download(query='kanye west jesus is lord jesus is lord',
                   query_type=QueryType.NAME)


def test_video():
    video = DolbyVideo(path='assets')
    video.download(query='kanye west jesus is lord jesus is lord',
                   query_type=QueryType.NAME)

test_audio()
test_video()