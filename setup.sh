#!/bin/bash

# sudo chmod a+x setup.sh
# ./setup.sh

echo "Checking for environments..."
if [ ! -d "./venv" ]
then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

echo "Activating Environment..."
set -e
source ./venv/bin/activate
echo "Running Script..."
pip3 install -r requirements.txt
