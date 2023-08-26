import os
import random

from nxtools import get_files
from pohadkomat.common import config


def get_clips() -> list[str]:
    """Returns a list of relative paths to downloaded mp3s."""
    return [
        f.path
        for f in get_files(
            config.download_path,
            relative_path=True,
            recursive=True,
            exts=["mp3"],
        )
    ]


def get_batch() -> list[str]:
    """Return a list of urls to play in the batch."""
    result = []

    all_clips = get_clips()
    if os.path.exists(config.asrun_path):
        history = [f.strip() for f in open(config.asrun_path).read().split("\n")]
        history = history[-int(len(all_clips) / 2) :]
    else:
        history = []
    pool = [clip for clip in all_clips if clip not in history]

    clips = random.sample(pool, config.clips_per_batch)
    for clip in clips:
        result.append(f"{config.access_url}/media/{clip}")
        with open(config.asrun_path, "a") as f:
            f.write(f"{clip}\n")
    return result
