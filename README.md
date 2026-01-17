# Introduction
This is a command line application to control local Sonos controller.

## Running the Web Server

```
uv run flask --app web run
```

## Docker

```
docker compose up
```

Note: Host network mode is required for Sonos speaker discovery to work. This does not work
correctly on macOS as Docker runs in a VM. On macOS, run the web server natively instead.
