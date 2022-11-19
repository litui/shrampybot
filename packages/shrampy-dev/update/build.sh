#!/bin/bash

set -e

virtualenv virtualenv
source virtualenv/bin/activate
pip install -U -r requirements.txt
deactivate

