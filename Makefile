all: exe
.PHONY: all

pylint:
	pylint --rcfile=pylintrc -i y solescion
.PHONY: pylint

tests:
	python -O run_tests.py
.PHONY: tests

py2exe: dist/run.exe
.PHONY: exe

dist/run.exe: run.py setup.py
	python setup.py py2exe

winzip: dist/run.exe
	python setup.py winzip
.PHONY: winzip

tags:
	ctags -R solescion

sdist:
	python setup.py sdist
.PHONY: sdist

install:
	python setup.py install
.PHONY: install

clean:
	rm -rf build dist tags
	-find . -name '*.py[oc]' -exec rm {} \;
.PHONY: clean

