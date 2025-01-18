import logging
import os

import uvicorn
from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import FileResponse

from pohadkomat.chromecast import player
from pohadkomat.config import config
from pohadkomat.db import MediaDB

app = FastAPI()


@app.get("/clips/{path:path}")
async def get_clip(path: str = Path(...)) -> FileResponse:
    """Return actual media file"""

    base_dir = config.media_dir
    full_path = os.path.join(base_dir, path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(full_path)


@app.post("/play")
def play():
    if config.device_name is None:
        logging.error("No device name configured")
        raise HTTPException(status_code=500, detail="Chromecast not configured")

    if config.base_url is None:
        logging.error("No base URL configured")
        raise HTTPException(status_code=500, detail="Base URL not configured")

    db = MediaDB()
    next_media = db.get_next()

    url = f"{config.base_url}/clips/{next_media}"
    logging.info(f"Playing {url}")
    player.play(url)


def start_server():
    uvicorn.run(app, host="0.0.0.0", port=config.http_port)
