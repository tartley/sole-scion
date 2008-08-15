
tags:
	ctags -R -f solescion/tags solescion

clean:
	-find solescion \
		-name '*.pyo' -o \
		-name '*.pyc' -o \
		-name 'tags' \
		-exec rm {} \;

install:
	@echo 'There is no installer. To run: "python -O solescion/run.py"'
	@echo '(or "bin/run" on Linux)'

.PHONY: tags, clean, install
