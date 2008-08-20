
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
	@echo 'There is no installer. To run, type "bin/run"'

.PHONY: clean, install, zip

