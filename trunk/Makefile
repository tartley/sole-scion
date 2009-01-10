all: exe
.PHONY: all

pylint:
	pylint --rcfile=pylintrc -i y solescion

tests:
	python -O run_tests.py

py2exe: dist/run.exe
.PHONY: exe

dist/run.exe: run.py setup.py
	python2.5 setup.py py2exe

tags:
	(cd solescion; ctags -R .; )

sdist:
	python setup.py sdist
.PHONY: sdist

install:
	python setup.py install
.PHONY: install

clean:
	rm -rf build dist solescion/tags
	-find . \( \
		-name '*.pyc' -o \
		-name '*.pyo' \
		\) -exec rm {} \;
.PHONY: clean

