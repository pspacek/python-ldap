"""
ldifcopy - reads LDIF from stdin, retrieve values by URL and
           write resulting LDIF to stdout

Written by Michael Stroeder <michael@stroeder.com>

$Id: ldifcopy.py,v 1.1 2001/12/12 18:57:14 stroeder Exp $

This example translates the naming context of data read from
input, sanitizes some attributes, maps/removes object classes,
maps/removes attributes., etc. It's far from being complete though.

Python compability note:
Tested on Python 2.0+, should run on Python 1.5.x.
"""

import sys,ldif

infile = sys.stdin
outfile = sys.stdout

ldif_collector = ldif.LDIFCopy(
  infile,
  outfile,
)
ldif_collector.parse()

