#!/bin/bash
export LD_LIBRARY_PATH+=./shapely
python -O solescion.py $*

