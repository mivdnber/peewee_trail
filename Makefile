SHELL := /bin/bash

test:
	pushd tests && py.test && popd

cleandoc:
	rm -rf docenv

docenv:
	virtualenv docenv && source docenv/bin/activate &&  \
	python setup.py develop && pip install sphinx sphinx_rtd_theme

doc: docenv
	pushd docs && rm -rf _build && make html && popd
