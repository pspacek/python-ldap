"""
controls.py - support classes for LDAPv3 extended operations

See http://www.python-ldap.org/ for details.

\$Id: __init__.py,v 1.2 2011/04/02 21:27:28 stroeder Exp $

Description:
The ldap.extop module provides base classes for LDAPv3 extended operations.
Each class provides support for a certain extended operation request and
response.
"""

from ldap import __version__


class ExtendedRequest:
  """
  Generic base class for a LDAP extended operation request
  """

  def __init__(self,requestName,requestValue):
    self.requestName = requestName
    self.requestValue = requestValue

  def __repr__(self):
    return '%s(%s,%s)' % (self.__class__.__name__,self.requestName,self.requestValue)

  def encodedRequestValue(self):
    return self.requestValue


class ExtendedResponse:
  """
  Generic base class for a LDAP extended operation response
  """

  def __init__(self,responseName,encodedResponseValue):
    self.responseName = responseName
    self.responseValue = self.decodeResponseValue(encodedResponseValue)

  def __repr__(self):
    return '%s(%s,%s)' % (self.__class__.__name__,self.responseName,self.responseValue)

  def decodeResponseValue(self,value):
    return value


# Optionally import sub-modules which need pyasn1
try:
  from ldap.extop.dds import *
except ImportError:
  pass
