#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:shapely
python -O main.py $*

