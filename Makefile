# $Id: Makefile,v 1.1 2001/11/13 22:55:12 leonard Exp $

PYTHON=	python

all:
	$(PYTHON) setup.py build
install:
	$(PYTHON) setup.py install
clean:
	$(PYTHON) setup.py clean --all
	rm -rf build
