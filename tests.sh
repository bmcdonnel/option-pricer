#!/bin/bash

rm $(find option_pricer -name \*\.pyc)

nosetests "$@"

