#!/bin/bash
python -u scripts/populate.py
flyway -configFiles=/app/flyway/flyway.conf migrate
python -u -m flask migrate-mongo
python -u -m flask run -h 0.0.0.0 -p 5000