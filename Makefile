# $Id: Makefile,v 1.2 2001/11/15 00:04:22 leonard Exp $

PYTHON=	python

all:
	$(PYTHON) setup.py build
install:
	$(PYTHON) setup.py install
dist:
	$(PYTHON) setup.py bdist
clean:
	$(PYTHON) setup.py clean --all
	-rmdir build
