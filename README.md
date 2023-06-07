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

## Events used:

1. Click event
2. Toggle event (combined with `1`)
3. Rotation events (2-dimensional)

## Events to consider?:

1. Accelerometer (measure acceleration forces, typically in three axes: X, Y, and Z). Flodd of events
2. Step counting? (based on accelerometer metrics)
3.
