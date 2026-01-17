#!/bin/bash
HOST="${SONOS_HOST:-localhost}"
curl -X POST "http://${HOST}:5000/speakers/Stofa/set-source" -H "Content-Type: application/json" -d '{"source": "line-in"}'
curl -X POST "http://${HOST}:5000/speakers/Stofa/volume" -H "Content-Type: application/json" -d '{"volume": 75}'
curl -X POST "http://${HOST}:5000/speakers/Stofa/play"
