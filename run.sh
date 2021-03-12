#!/bin/bash
export FLASK_APP=server.py
export PYTHONPATH=${PWD}
flask run --host='0.0.0.0'