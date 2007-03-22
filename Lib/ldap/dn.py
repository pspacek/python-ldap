"""
dn.py - misc stuff for handling distinguished names (see RFC 4514)
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

\$Id: dn.py,v 1.2 2007/03/22 22:06:06 stroeder Exp $

Compability:
- Tested with Python 2.0+
"""

__version__ = '0.1.0'


import _ldap

import ldap.functions


def escape_dn_chars(s):
  """
  Escape all DN special characters found in s
  with a back-slash
  """
  if s:
    s = s.replace('\\','\\\\')
    s = s.replace(',' ,'\\,')
    s = s.replace('+' ,'\\+')
    s = s.replace('"' ,'\\"')
    s = s.replace('<' ,'\\<')
    s = s.replace('>' ,'\\>')
    s = s.replace(';' ,'\\;')
    s = s.replace('=' ,'\\=')
    if s[0]=='#':
      s = ''.join(('\\',s))
    if s[-1]==' ':
      s = ''.join((s[:-1],'\\ '))
  return s


def str2dn(dn,flags=0):
  return ldap.functions._ldap_function_call(_ldap.str2dn,dn,flags)


def explode_dn(dn,notypes=0):
  """
  explode_dn(dn [, notypes=0]) -> list
  
  This function takes a DN and breaks it up into its component parts.
  The notypes parameter is used to specify that only the component's
  attribute values be returned and not the attribute types.
  """
  if not dn:
    return []
  dn_decomp = str2dn(dn)
  rdn_list = []
  for rdn in dn_decomp:
    if notypes:
      rdn_list.append('+'.join([escape_dn_chars(avalue or '') for atype,avalue,dummy in rdn]))
    else:
      rdn_list.append('+'.join(['='.join((atype,escape_dn_chars(avalue or ''))) for atype,avalue,dummy in rdn]))
  return rdn_list


def explode_rdn(rdn,notypes=0):
  """
  explode_rdn(rdn [, notypes=0]) -> list
  
  This function takes a RDN and breaks it up into its component parts
  if it is a multi-valued RDN.
  The notypes parameter is used to specify that only the component's
  attribute values be returned and not the attribute types.
  """
  if not rdn:
    return []
  rdn_decomp = str2dn(rdn)[0]
  if notypes:
    return [avalue or '' for atype,avalue,dummy in rdn_decomp]
  else:
    return ['='.join((atype,escape_dn_chars(avalue or ''))) for atype,avalue,dummy in rdn_decomp]
