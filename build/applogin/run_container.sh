#!/bin/sh
HOME=$3
cd $HOME
pip install --no-cache-dir --upgrade -r requirements.txt
python setup.py install --user
uvicorn applogin.app:app --reload --host 0.0.0.0 --port 8080
