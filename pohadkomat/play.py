import time
import threading
import pychromecast

from nxtools import get_files, critical_error, logging
from pohadkomat.common import config
from pohadkomat.library import get_batch


def get_available_chromecasts() -> list[str]:
    services, browser = pychromecast.discovery.discover_chromecasts()
    return [service.friendly_name for service in services]


def ensure_chromecast_available() -> bool:
    services, browser = pychromecast.discovery.discover_chromecasts()
    return config.chromecast_name in [service.friendly_name for service in services]


class Player:
    def __init__(self):
        pass

    def get_media_controller(self):
        chromecasts, browser = pychromecast.get_listed_chromecasts(
            friendly_names=[config.chromecast_name]
        )
        try:
            chromecast = chromecasts[0]
        except IndexError:
            return
        chromecast.wait()
        return chromecast.media_controller

    def start(self):
        thread = threading.Thread(target=self.play_batch)
        thread.start()

    def play_batch(self):
        media_controller = self.get_media_controller()
        for url in get_batch():
            media_controller.play_media(url, "audio/mp3")
            media_controller.block_until_active()
            i = 0
            while i < 20:
                print(media_controller.status)
                time.sleep(1)
                i += 1


player = Player()
