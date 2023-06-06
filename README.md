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
