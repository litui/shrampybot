#!/bin/bash

set -e

virtualenv virtualenv
source virtualenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
deactivate

