all: exe
.PHONY: all

exe: dist/run.exe
.PHONY: exe

dist/run.exe: run.py setup.py
	python2.5 setup.py py2exe

tags:
	(cd solescion; ctags -R .; )

zip:
	bin/make_zip
.PHONY: zip

clean:
	rm -rf build dist run.py?
	-find solescion \( \
		-name 'tags' -o \
		-name '*.pyc' -o \
		-name '*.pyo' \
		\) -exec rm {} \;
.PHONY: clean

install:
	@echo 'There is no installer.'
.PHONY: install

