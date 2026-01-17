from flask import Flask, Response, jsonify, request

import sonos

app = Flask(__name__)


@app.get("/")
def index() -> Response:
    return jsonify({
        "name": "Sonos Controller API",
        "endpoints": [
            {"method": "GET", "path": "/speakers", "description": "List all speakers"},
            {"method": "GET", "path": "/speakers/<speaker_name>", "description": "Get speaker info"},
            {"method": "POST", "path": "/speakers/<speaker_name>/play", "description": "Play on speaker"},
            {"method": "POST", "path": "/speakers/<speaker_name>/pause", "description": "Pause speaker"},
            {"method": "POST", "path": "/speakers/<speaker_name>/set-source", "description": "Set speaker source (body: {\"source\": \"line-in\" | \"music\"})"},
            {"method": "POST", "path": "/speakers/<speaker_name>/volume", "description": "Set speaker volume (body: {\"volume\": 0-100})"},
        ]
    })


@app.get("/speakers")
def list_speakers() -> Response:
    speakers = sonos.discover_speakers()
    return jsonify(speakers)


@app.get("/speakers/<speaker_name>")
def get_speaker(speaker_name: str) -> Response | tuple[Response, int]:
    info = sonos.get_speaker_info(speaker_name)
    if info:
        return jsonify(info)
    return jsonify({"status": "error", "message": f"Speaker not found: {speaker_name}"}), 404


@app.post("/speakers/<speaker_name>/play")
def play(speaker_name: str) -> Response | tuple[Response, int]:
    if sonos.play(speaker_name):
        return jsonify({"status": "ok", "message": f"Playing on {speaker_name}"})
    return jsonify({"status": "error", "message": f"Speaker not found: {speaker_name}"}), 404


@app.post("/speakers/<speaker_name>/pause")
def pause(speaker_name: str) -> Response | tuple[Response, int]:
    if sonos.pause(speaker_name):
        return jsonify({"status": "ok", "message": f"Paused {speaker_name}"})
    return jsonify({"status": "error", "message": f"Speaker not found: {speaker_name}"}), 404


@app.post("/speakers/<speaker_name>/set-source")
def set_source(speaker_name: str) -> Response | tuple[Response, int]:
    data = request.get_json()
    if not data or "source" not in data:
        return jsonify({"status": "error", "message": "Missing 'source' in request body"}), 400
    success, error = sonos.set_source(speaker_name, data["source"])
    if success:
        return jsonify({"status": "ok", "message": f"Set {speaker_name} source to {data['source']}"})
    return jsonify({"status": "error", "message": error}), 404


@app.post("/speakers/<speaker_name>/volume")
def set_volume(speaker_name: str) -> Response | tuple[Response, int]:
    data = request.get_json()
    if not data or "volume" not in data:
        return jsonify({"status": "error", "message": "Missing 'volume' in request body"}), 400
    volume = data["volume"]
    if not isinstance(volume, int) or volume < 0 or volume > 100:
        return jsonify({"status": "error", "message": "Volume must be an integer between 0 and 100"}), 400
    if sonos.set_volume(speaker_name, volume):
        return jsonify({"status": "ok", "message": f"Set {speaker_name} volume to {volume}"})
    return jsonify({"status": "error", "message": f"Speaker not found: {speaker_name}"}), 404


if __name__ == "__main__":
    app.run()
