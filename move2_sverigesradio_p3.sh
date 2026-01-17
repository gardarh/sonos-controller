#!/bin/bash
HOST="${SONOS_HOST:-localhost}"
curl -X POST "http://${HOST}:5000/speakers/Move%202/play-uri" \
    -H "Content-Type: application/json" \
    -d '{"uri": "x-rincon-mp3radio://live1.sr.se/p3-aac-320", "title": "Sveriges Radio P3"}'
curl -X POST "http://${HOST}:5000/speakers/Move%202/volume" \
    -H "Content-Type: application/json" \
    -d '{"volume": 20}'
