
exe: dist/run.exe

dist/run.exe: run.py setup.py
	python2.5 setup.py py2exe

tags:
	(cd solescion; ctags -R .; )

zip:
	bin/make_zip

clean:
	rm -rf build dist
	-find solescion \( \
		-name 'tags' -o \
		-name '*.pyc' -o \
		-name '*.pyo' \
		\) -exec rm {} \;

install:
	@echo 'There is no installer.'

.PHONY: clean, install, zip, exe, win-binary

