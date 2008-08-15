
tags: clean
	ctags -R .

clean:
	-find . -name '*.pyo' -exec rm {} \;
	-find . -name '*.pyc' -exec rm {} \;
	-rm tags

install:
	@echo 'There is no installer. Run with "python -O sole_scion.py"'

.PHONY: tags, clean, install
