import os
import requests

from pohadkomat.common import config, FeedConfig

from nxtools import (
    log_traceback,
    xml,
    FileObject,
    slugify,
    ffmpeg,
)


def process_feed(feed: FeedConfig):
    try:
        rss_data = requests.get(feed.url)
        rss = xml(rss_data.text)
        channel = rss.find("channel")
    except Exception:
        log_traceback()
        return

    for item in channel.findall("item"):
        try:
            item_title = item.find("title").text
            item_url = item.find("enclosure").attrib["url"]
        except Exception:
            log_traceback()
            continue

        target_path = FileObject(
            os.path.expanduser(config.download_path),
            slugify(feed.title),
            slugify(item_title) + ".mp3",
        )

        if target_path.exists:
            continue

        if not os.path.isdir(target_path.dir_name):
            os.makedirs(target_path.dir_name)

        result = ffmpeg(
            "-y",
            "-i",
            item_url,
            "-filter:a",
            "loudnorm=i=-14",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "128k",
            "-map_metadata",
            "-1",
            "-metadata",
            f"title={item_title}",
            "-metadata",
            f"album={feed.title}",
            "-metadata",
            f"artist={feed.artist or config.default_artist}",
            target_path,
        )

        # If download fails, remove the paratial file
        if not result:
            if target_path.exists:
                os.remove(target_path.path)


def main():
    for feed in config.feeds:
        process_feed(feed)
