## Installation Guide

1. Install `poetry`: [Installation Guide](https://python-poetry.org/docs/#installation).

Note: you might need to use python ^3.10.

2. Install python dependencies:

```bash
poetry install
```

3. Start the server:

```bash
poetry run poe start
```

4. Open the `./arduino/watch_event_processing` in Arduino IDE
5. Upload the sketch to the watch

## Watch Events:

1. Click event
2. Toggle event (combined with `1`)
3. Rotation events (2-dimensional)

## Run on a Pi

1. Install `Docker` and `docker compose` by running

```bash
./install_docker.sh
```

2. Start the services with

```bash
sudo DEVICE_ID=<pi_id> docker compose up
```

where `pi_id` is the ID of the current rasberry pi.

It spins up two services: (a) the fastapi http server with the event processing app Siddhi and (b) the service to reads sensor data from the pi and send it to the http server

