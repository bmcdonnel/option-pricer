#!/bin/bash

# uncomment this if you need to install virtualenv
# pip install virtualenv

# create a virtual environment in case special packages are needed
rm -rf venv
virtualenv venv
source venv/bin/activate

# these packages will be installed to the venv, and will not affect the system at large
pip install pylint
pip install nose
pip install mock

