
tags:
	ctags -R -f solescion/tags solescion

clean:
	-find solescion \( \
		-name 'tags' -o \
		-name '*.pyc' -o \
		-name '*.pyo' \
		\) -exec rm {} \;

install:
	@echo 'There is no installer. To run: "python -O solescion/run.py"'
	@echo '(or "bin/run" on Linux)'

.PHONY: tags, clean, install
