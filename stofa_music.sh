#!/bin/bash
HOST="${SONOS_HOST:-localhost}"
curl -X POST "http://${HOST}:5000/speakers/Stofa/set-source" -H "Content-Type: application/json" -d '{"source": "music"}'
curl -X POST "http://${HOST}:5000/speakers/Stofa/volume" -H "Content-Type: application/json" -d '{"volume": 15}'
