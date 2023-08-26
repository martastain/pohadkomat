import time
import threading
import pychromecast

from nxtools import logging, get_base_name
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
        self.should_run = False
        self.batch = []

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
        if self.batch:
            logging.warning("Already playing")
            return

        self.should_run = False
        time.sleep(0.5)
        self.should_run = True
        thread = threading.Thread(target=self.play_batch)
        thread.start()

    def play_batch(self):
        self.batch = get_batch()
        media_controller = self.get_media_controller()

        if media_controller is None:
            logging.error("Chromecast not found")
            self.batch = []
            self.should_run = False
            return

        start_time = time.time()

        for url in self.batch:
            if not self.should_run:
                break

            if time.time() - start_time > 3600:
                self.batch = []
                self.should_run = False
                break

            logging.info(f"Playing {get_base_name(url)}")
            media_controller.play_media(url, "audio/mp3")
            media_controller.block_until_active()

            # TODO: wait for play somehow smarter
            # after play_media, there's a IDLE state for a while, then PLAY
            # and after playback stops, it changes again to IDLE
            time.sleep(5)
            while media_controller.status.player_state == "PLAYING" and self.should_run:
                time.sleep(0.3)
            logging.info(
                f"Stopped {get_base_name(url)} ({media_controller.status.player_state})"
            )

        self.batch = []
        logging.info("Batch is finished. Good night")


player = Player()
