
tags:
	(cd solescion; ctags -R .; )

clean:
	-find solescion \( \
		-name 'tags' -o \
		-name '*.pyc' -o \
		-name '*.pyo' \
		\) -exec rm {} \;

zip:
	bin/make_zip


install:
	@echo 'There is no installer. To run: "python -O solescion/run.py"'
	@echo '(or "bin/run" on Linux)'


.PHONY: clean, install, tags, zip

