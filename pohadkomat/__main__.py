import logging

import typer
from rich.logging import RichHandler

from pohadkomat.chromecast import get_available_chromecasts
from pohadkomat.db import MediaDB
from pohadkomat.server import start_server

# Set-up logging using rich

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)


app = typer.Typer()


@app.command()
def chromecasts():
    for device in get_available_chromecasts():
        logging.info(device)


@app.command()
def scan():
    mediadb = MediaDB()
    mediadb.scan(True)
    mediadb.list_media()


@app.command()
def next():
    mediadb = MediaDB()
    logging.info(mediadb.get_next())


@app.command()
def serve():
    start_server()


if __name__ == "__main__":
    app()
