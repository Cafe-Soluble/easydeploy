#!/bin/bash

echo "Starting env and packages installation..."
python3 -m venv env
source env/bin/activate && pip install -r requirements.txt && pip install gunicorn
echo "Ending env and packages installation"
