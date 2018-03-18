#!/bin/bash

if [ ! -d 'venv' ]; then
  echo 'bootstrapping virtual environment'
  source bootstrap.sh
fi

rm $(find option_pricer -name \*\.pyc)

source venv/bin/activate

nosetests "$@"

