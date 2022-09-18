import typer

from pohadkomat.download import download_all
from pohadkomat.play import get_available_chromecasts
from pohadkomat.server import start_server


app = typer.Typer()


@app.command()
def list():
    for device in get_available_chromecasts():
        print(device)


@app.command()
def download():
    download_all()


@app.command()
def serve():
    start_server()


if __name__ == "__main__":
    app()
