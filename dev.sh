#!/bin/bash
# Local development script with hot-reloading
./venv/bin/watchmedo auto-restart --pattern="*.py" --recursive -- ./venv/bin/python bot.py
