#!/bin/bash
curl -X POST http://localhost:5000/speakers/Stofa/set-source -H "Content-Type: application/json" -d '{"source": "line-in"}'
curl -X POST http://localhost:5000/speakers/Stofa/volume -H "Content-Type: application/json" -d '{"volume": 75}'
curl -X POST http://localhost:5000/speakers/Stofa/play
