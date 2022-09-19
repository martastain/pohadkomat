Pohadkomat
==========

An overengineered fairy tale player.

The goal
--------

Anežka requires two fairy tales to be played before she goes to the bed. 
This automates the process so I can skip searching for a clip and allows 
me to take a long bath without handling her 'I WANT ONE MORE!' request.

Pohadkomat downloads fairy tales from RSS feeds (podcasts).
A small list of feeds is included, pull requests are welcome.

During the download, all audio files are processed and loudnes is normalized
to -14 LUFS.

Using a webhook from Home assistant, pohadkomat plays two clips using a good old 
[Dramatica](https://github.com/immstudios/dramatica) algorithm on a chromecast
(Google nest) device.

Everything is configurable using toml files.

Usage
-----

Pohadkomat requires poetry and ffmpeg. 


Use `poetry run -m pohadkomat list` to list all chromecast device on the network
Set the correct name in the `pohadkomat.toml`

Set a cron job to execute `poetry run -m pohadkomat download`, which 
updates the fairy tale library. RSS sources are definded in
`feeds.toml`.

Run `poetry run -m pohadkomat serve` runs as a background service (systemd). 
It exposes downloaded files over plain http (to allow chromecasts to play them) 
as well as a webhook triggered by a big red button (using home assistant). 

### Home assistant

Add the following lines to your Home assistant `configuration.yaml`

```yaml
rest_command:
  pohadkomat:
    url: "https://your_server:9734/play”
    method: post
```

Then you can call `RESTful Command: pohadkomat` service to start playing
