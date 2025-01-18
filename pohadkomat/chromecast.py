import logging
import threading
import time

import pychromecast

from pohadkomat.config import config


def get_available_chromecasts() -> list[str]:
    services, browser = pychromecast.discovery.discover_chromecasts()
    return [service.friendly_name for service in services if service.friendly_name]


def ensure_chromecast_available() -> bool:
    services, browser = pychromecast.discovery.discover_chromecasts()
    return config.device_name in [service.friendly_name for service in services]


class Player:
    playing: str | None = None

    def __init__(self):
        pass

    def get_media_controller(self) -> pychromecast.MediaController | None:
        assert config.device_name is not None, "No device name configured"
        logging.info(f"Looking for {config.device_name}")

        chromecasts, browser = pychromecast.get_listed_chromecasts(
            friendly_names=[config.device_name]
        )
        try:
            chromecast = chromecasts[0]
        except IndexError:
            return
        chromecast.wait()
        return chromecast.media_controller

    def play(self, url: str):
        if self.playing:
            logging.warning("Already playing. Stopping playback")
            return

        self.playing = url
        thread = threading.Thread(target=self._play_thread)
        thread.start()

    def _play_thread(self):
        media_controller = self.get_media_controller()

        if media_controller is None:
            logging.error("Chromecast not found")
            self.playing = None
            return

        if not self.playing:
            logging.error("Nothing to play")
            return

        media_controller.play_media(self.playing, "audio/mp3")
        media_controller.block_until_active()

        time.sleep(1)
        while media_controller.status.player_state == "PLAYING" and self.playing:
            logging.debug("Stopping")
            time.sleep(0.3)

        self.playing = None
        logging.info("Batch is finished. Good night")


player = Player()
