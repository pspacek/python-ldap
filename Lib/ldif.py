# python
# $Id: ldif.py,v 1.4 2001/06/05 14:51:53 stroeder Exp $

"""
ldif.py - Various routines for handling LDIF data

This module is distributed under the terms of the
GPL (GNU GENERAL PUBLIC LICENSE) Version 2
(see http://www.gnu.org/copyleft/gpl.html)
"""

__version__ = '0.2.8'

import sys,string,binascii,re

try:
  from cStringIO import StringIO
except ImportError:
  from StringIO import StringIO

attrtype_pattern = r'[\w;.]+(;[\w_-]+)*'
data_pattern = r'(([^,]|\\,)+|".*?")'
rdn_pattern = attrtype_pattern + r'[ ]*=[ ]*' + data_pattern
dn_pattern   = rdn_pattern + r'([ ]*,[ ]*' + rdn_pattern + r')*[ ]*'
dn_regex   = re.compile('^%s$' % dn_pattern)

ldif_pattern = '^((dn(:|::) %(dn_pattern)s)|(%(attrtype_pattern)s(:|::) .*)$)+' % vars()
ldif_regex   = re.compile('^%s$' % ldif_pattern,re.M)

non_ldif_value_re = re.compile('(^( |:|<)|[\x80-\xff]+)')

def is_dn(s):
  """
  returns 1 if s is a LDAP DN
  """
  rm = dn_regex.match(s)
  return rm!=None and rm.group(0)==s

def is_valid_ldif_value(s):
  """
  returns 1 if s does not need base-64 encoding because of special chars
  """
  return non_ldif_value_re.search(s) is None


def BinaryAttribute(attrtype,value,cols=66):
  """
  Convert value to a binary attribute representation (base64 encoded)

  attrtype
        string of attribute type
  value
        string containing the attribute value
  cols
        Number of text columns to use for base64 output
  """
  b64buf = '%s:: ' % (attrtype)
  buflen = len(value)
  pos=0
  while pos<buflen:
    b64buf = '%s%s' % (b64buf,binascii.b2a_base64(value[pos:min(buflen,pos+57)])[:-1])
    pos = pos+57
  b64buflen = len(b64buf)
  pos=cols
  result = b64buf[0:min(b64buflen,cols)]
  while pos<b64buflen:
    result = '%s\n %s' % (result,b64buf[pos:min(b64buflen,pos+cols-1)])
    pos = pos+cols-1
  return '%s\n' % result


def CreateLDIF(dn,entry={},binary_attrs=[]):
  """
  Create LDIF formatted entry without trailing empty line.
  
  dn
        string-representation of distinguished name
  entry
        dictionary holding the LDAP entry {attrtype:data}
  binary_attrs
        list of attribute types to be base64-encoded in any case
  """
  # Get all attribute types
  attrs = entry.keys()[:]
  attrs.sort()
  # Write line dn: first
  if is_valid_ldif_value(dn):
    result = ['dn: %s\n' % (dn)]
  else:
    result = [BinaryAttribute('dn',dn)]
  # Write all attrtype: value lines
  for attr in attrs:
    # Write all values of an attribute
    for data in entry[attr]:
      if (attr in binary_attrs) or not is_valid_ldif_value(data):
        result.append(BinaryAttribute(attr,data))
      else:
  	result.append('%s: %s\n' % (attr,data))
  return string.join(result,'')


def ParseLDIF(f,ignore_attrs=[],maxentries=0):
  """
  Parse LDIF data read from file object f

  f
        file-object for reading LDIF input
  ignore_attrs
        list of attributes to be ignored
  maxentries
        if non-zero) specifies the maximum number of
  	entries to be read from f
  """
  
  result = []

  # lower-case all
  ignore_attrs = map(string.lower,ignore_attrs)

  # Read very first line
  s = f.readline()

  entries_read = 0

  while s and (not maxentries or entries_read<maxentries):

    # Reading new entry

    # Reset entry data
    dn = ''; entry = {}; attr = ''; data = ''

    s = string.rstrip(s)

    while s:
    
      # Reading new attribute line
      attr,data=string.split(s,':',1)
      if data[0]==':':
        # Read attr:: data line => binary data assumed
        data = data[1:]
        binary = 1
      else:
        # Read attr: data line
        binary = 0

      s = f.readline()
      s = string.rstrip(s)

      # Reading continued multi-line data
      while s and s[0]==' ':
        data = data + string.strip(s)
        # Read next line
        s = f.readline()
        s = string.rstrip(s)

      attr = string.strip(attr)

      if not string.lower(attr) in ignore_attrs:

	if binary:
          # binary data has to be BASE64 decoded
          data = binascii.a2b_base64(data)
	else:
          data = string.strip(data)

        # Add attr: data to entry
	if attr=='dn':
          dn = string.strip(data) ; attr = '' ; data = ''
          if not is_dn(dn):
	    raise ValueError, 'No valid string-representation of distinguished name.'
	else:
          if entry.has_key(attr):
            entry[attr].append(data)
          else:
            entry[attr]=[data]

    # end of entry reached marked by newline character(s)

    if entry:
      # append entry to result list
      result.append((dn,entry))
      entries_read = entries_read+1

    # Start reading next entry
    s = f.readline()

  return result


def test():
  test_entry = {
    'objectClass':['test'],
    'cn':['Michael Str\303\266der'],
    'bin':['\000\001\002'*200],
    'extraspace':[' bla'],
  }
  ldif = CreateLDIF(
    'cn=Michael Str\303\266der,dc=stroeder,dc=com',test_entry,['bin']
  )
  print ldif
  test_result = ParseLDIF(StringIO(ldif))
  print test_result
  for a in test_entry.keys():
    if test_entry[a]!=test_result[0][1][a]:
      print 'Error in attribute %s: "%s"!="%s"' % (
        a,repr(test_entry[a]),repr(test_result[0][1][a])
      )

if __name__ == '__main__':
  test()
