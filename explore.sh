#!/bin/bash
cd explore
python3 -m venv yosemite_env
source yosemite_env/bin/activate
bash
pip install yosemite
spacy download en_core_web_sm
yosemite