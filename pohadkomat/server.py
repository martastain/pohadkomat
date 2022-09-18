import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from pohadkomat.common import config
from pohadkomat.library import get_clips
from pohadkomat.play import player

app = FastAPI()
app.mount("/media", StaticFiles(directory=config.download_path))


@app.get("/clips")
async def clips():
    return get_clips()


@app.post("/play")
def play():
    player.start()


def start_server():
    uvicorn.run(app, host="0.0.0.0", port=config.http_port)
