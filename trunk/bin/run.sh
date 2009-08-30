#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:solescion/lib
python -O main.py $*

