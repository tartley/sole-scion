
exe: dist/run.exe

dist/run.exe: run.py setup.py
	python2.5 setup.py py2exe

tags:
	(cd solescion; ctags -R .; )

clean:
	rm -rf build dist
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

