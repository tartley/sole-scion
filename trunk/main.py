#!/usr/bin/env python -O

from solescion.utils.environment import add_lib_to_path
add_lib_to_path()
from solescion.controller.application import main

if __name__ == "__main__":
    main()

