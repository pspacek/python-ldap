"""
ldapurl - handling of LDAP URLs as described in RFC 2255
written by Michael Stroeder <michael@stroeder.com>

\$Id: ldapurl.py,v 1.21 2002/08/08 09:17:41 stroeder Exp $

This module is part of the python-ldap project:
http://python-ldap.sourceforge.net

License:
Public domain. Do anything you want with this module.

Python compability note:
This module only works with Python 2.0+ since
1. string methods are used instead of module string and
2. list comprehensions are used.
"""

__version__ = '0.5.0'

__all__ = [
  # constants
  'SEARCH_SCOPE','SEARCH_SCOPE_STR',
  'LDAP_SCOPE_BASE','LDAP_SCOPE_ONELEVEL','LDAP_SCOPE_SUBTREE',
  # functions
  'isLDAPUrl',
  # classes
  'LDAPUrlExtension','LDAPUrlExtensions','LDAPUrl'
]

import UserDict

from urllib import quote,quote_plus,unquote_plus

LDAP_SCOPE_BASE = 0
LDAP_SCOPE_ONELEVEL = 1
LDAP_SCOPE_SUBTREE = 2

SEARCH_SCOPE_STR = {None:'',0:'base',1:'one',2:'sub'}

SEARCH_SCOPE = {
  '':None,
  # the search scope strings defined in RFC2255
  'base':LDAP_SCOPE_BASE,
  'one':LDAP_SCOPE_ONELEVEL,
  'sub':LDAP_SCOPE_SUBTREE,
}

# Some widely used types
StringType = type('')
TupleType=type(())


def isLDAPUrl(s):
  """
  Returns 1 if s is a LDAP URL, 0 else
  """
  return \
    s.startswith('ldap://') or \
    s.startswith('ldaps://') or \
    s.startswith('ldapi://')


class LDAPUrlExtension:
  """
  Class for parsing and unparsing LDAP URL extensions
  as described in RFC 2255.

  BNF definition of LDAP URL extensions:

       extensions = extension *("," extension)
       extension  = ["!"] extype ["=" exvalue]
       extype     = token / xtoken
       exvalue    = LDAPString from section 4.1.2 of [2]
       token      = oid from section 4.1 of [3]
       xtoken     = ("X-" / "x-") token

  Usable class attributes:
  critical
        Boolean integer marking the extension as critical
  extype    
        Type of extension
  exvalue
        Value of extension
  """

  def __init__(self,extensionStr=None,critical=0,extype=None,exvalue=None):
    self.critical = critical
    self.extype = extype
    self.exvalue = exvalue
    if extensionStr:
      self._parse(extensionStr)

  def _parse(self,extension):
    extension = extension.strip()
    if not extension:
      # Don't parse empty strings
      self.extype,self.exvalue = None,None
      return
    self.critical = extension[0]=='!'
    if extension[0]=='!':
      extension = extension[1:].strip()
    self.extype,self.exvalue = extension.split('=',1)
    self.extype = self.extype.strip()
    self.exvalue = unquote_plus(self.exvalue.strip())

  def unparse(self):
    return '%s%s=%s' % (
      '!'*(self.critical>0),
      self.extype,self.exvalue.replace(',',r'%2C')
    )
    
  def __str__(self):
    return self.unparse()

  def __repr__(self):
    return '<%s.%s instance at %s: %s>' % (
      self.__class__.__module__,
      self.__class__.__name__,
      hex(id(self)),
      self.__dict__
    )

  def __eq__(self,other):
    return \
      (self.critical==other.critical) and \
      (self.extype==other.extype) and \
      (self.exvalue==other.exvalue)

  def __ne__(self,other):
    return not self.__eq__(other)


class LDAPUrlExtensions(UserDict.UserDict):
  """
  Models a collection of LDAP URL extensions as
  dictionary type
  """

  def __init__(self,default={}):
    UserDict.UserDict.__init__(self,{})
    for k,v in default.items():
      self[k]=v

  def __getitem__(self,name):
    """
    This always returns LDAPUrlExtension instance
    """
    critical,exvalue = self.data[name]
    return LDAPUrlExtension(
      critical=critical,extype=name,exvalue=exvalue
    )

  def __setitem__(self,name,value):
    """
    value
        Either LDAPUrlExtension instance, (critical,exvalue)
        or string'ed exvalue
    """
    assert type(value)==TupleType or \
           type(value)==StringType or \
           isinstance(value,LDAPUrlExtension),TypeError
    if type(value)==StringType:
      self.data[name] = 0,value
    elif type(value)==TupleType and len(value==2):
      self.data[name] = value
    elif isinstance(value,LDAPUrlExtension):
      assert name==value.extype
      self.data[name] = value.critical,value.exvalue

  def __str__(self):
    return ','.join(map(str,self.values()))

  def __repr__(self):
    return '<%s.%s instance at %s: %s>' % (
      self.__class__.__module__,
      self.__class__.__name__,
      hex(id(self)),
      self.data
    )

  def __eq__(self,other):
    assert isinstance(other,self.__class__),TypeError(
      "other has to be instance of %s" % (self.__class__)
    )
    result = (self.data==other.data)
    return result
    
  def parse(self,extListStr):
    extensions = [
      LDAPUrlExtension(extension)
      for extension in extListStr.strip().split(',')
    ]
    for e in extensions:
      self[e.extype] = e

  def unparse(self):
    return ','.join([
      self[k].unparse()
      for k in self.keys()
    ])


class LDAPUrl:
  """
  Class for parsing and unparsing LDAP URLs
  as described in RFC 2255.

  BNF definition of LDAP URL:

    hostport     host:port
    dn           distinguished name
    attributes   list with attributes
    scope        search scope string
    filter       LDAP search filter
    ldapurl    = scheme "://" [hostport] ["/"
                     [dn ["?" [attrs] ["?" [scope]
                     ["?" [filter] ["?" extensions]]]]]]

  Usable class attributes:
    urlscheme
        URL scheme (either ldap, ldaps or ldapi)
    hostport
        LDAP host (default '')
    dn
        String holding distinguished name (default '')
    attrs
        list of attribute types (default None)
    scope
        integer search scope for ldap-module
    filterstr
        String representation of LDAP Search Filters
        (see RFC 2254)
    extensions
        Dictionary used as extensions store
    who
        Maps automagically to bindname LDAP URL extension
    cred
        Maps automagically to X-BINDPW LDAP URL extension
  """

  attr2extype = {'who':'bindname','cred':'X-BINDPW'}

  def __init__(
    self,
    ldapUrl=None,
    urlscheme='ldap',
    hostport='',dn=None,attrs=None,scope=None,filterstr=None,
    extensions=LDAPUrlExtensions(),
    who=None,cred=None
  ):
    self.urlscheme=urlscheme
    self.hostport=hostport
    self.dn=dn
    self.attrs=attrs
    self.scope=scope
    self.filterstr=filterstr
    self.extensions=extensions
    if ldapUrl!=None:
      self._parse(ldapUrl)
    if who!=None:
      self.who = who
    if cred!=None:
      self.cred = cred

  def __eq__(self,other):
    return \
      self.urlscheme==other.urlscheme and \
      self.hostport==other.hostport and \
      self.dn==other.dn and \
      self.attrs==other.attrs and \
      self.scope==other.scope and \
      self.filterstr==other.filterstr and \
      self.extensions==other.extensions

  def __ne__(self,other):
    return not self.__eq__(other)

  def _parse(self,ldap_url):
    """
    parse a LDAP URL and set the class attributes
    urlscheme,host,dn,attrs,scope,filterstr,extensions
    """
    if not isLDAPUrl(ldap_url):
      raise ValueError,'Parameter ldap_url does not seem to be a LDAP URL.'
    scheme,rest = ldap_url.split('://',1)
    self.urlscheme = scheme.strip()
    if not self.urlscheme in ['ldap','ldaps','ldapi']:
      raise ValueError,'LDAP URL contains unsupported URL scheme %s.' % (self.urlscheme)
    slash_pos = rest.find('/')
    qemark_pos = rest.find('?')
    if (slash_pos==-1) and (qemark_pos==-1):
      # No / and ? found at all
      self.hostport = unquote_plus(rest)
      self.dn = u''
      return
    else:
      if slash_pos!=-1 and (qemark_pos==-1 or (slash_pos<qemark_pos)):
        # Slash separates DN from hostport
        self.hostport = unquote_plus(rest[:slash_pos])
        # Eat the slash from rest
        rest = rest[slash_pos+1:]
      elif qemark_pos!=1 and (slash_pos==-1 or (slash_pos>qemark_pos)):
        # Question mark separates hostport from rest, DN is assumed to be empty
        self.hostport = unquote_plus(rest[:qemark_pos])
        # Do not eat question mark
        rest = rest[qemark_pos:]
      else:
        raise ValueError,'Something completely weird happened!'
    paramlist=rest.split('?')
    paramlist_len = len(paramlist)
    if paramlist_len>=1:
      self.dn = unquote_plus(paramlist[0]).strip()
    if (paramlist_len>=2) and (paramlist[1]):
      self.attrs = unquote_plus(paramlist[1].strip()).split(',')
    if paramlist_len>=3:
      scope = paramlist[2].strip()
      try:
        self.scope = SEARCH_SCOPE[scope]
      except KeyError:
        raise ValueError,"Search scope must be either one of base, one or sub. LDAP URL contained %s" % (repr(scope))
    if paramlist_len>=4:
      filterstr = paramlist[3].strip()
      if not filterstr:
        self.filterstr = None
      else:
        self.filterstr = unquote_plus(filterstr)
    if paramlist_len>=5:
      self.extensions = LDAPUrlExtensions()
      self.extensions.parse(paramlist[4])
    return

  def _urlEncoding(self,s):
    """Returns URL encoding of string s"""
    return quote(s).replace(',','%2C').replace('/','%2F')

  def applyDefaults(self,defaults):
    """
    Apply defaults to all class attributes which are None.

    defaults
        Dictionary containing a mapping from class attributes
        to default values
    """
    for k in defaults.keys():
      if getattr(self,k) is None:
        setattr(self,k,defaults[k])

  def initializeUrl(self):
    """
    Returns LDAP URL suitable to be passed to ldap.initialize()
    """
    if self.urlscheme=='ldapi':
      # hostport part might contain slashes when ldapi:// is used
      hostport = quote_plus(self.hostport)
    else:
      hostport = self.hostport
    return '%s://%s' % (self.urlscheme,hostport)

  def unparse(self):
    """
    Returns LDAP URL depending on class attributes set.
    """
    if self.attrs is None:
      attrs_str = ''
    else:
      attrs_str = ','.join(self.attrs)
    scope_str = SEARCH_SCOPE_STR[self.scope]
    if self.filterstr is None:
      filterstr = ''
    else:
      filterstr = self._urlEncoding(self.filterstr)
    dn = self._urlEncoding(self.dn)
    if self.urlscheme=='ldapi':
      # hostport part might contain slashes when ldapi:// is used
      hostport = quote_plus(self.hostport)
    else:
      hostport = self.hostport
    ldap_url = u'%s://%s/%s?%s?%s?%s' % (
      self.urlscheme,
      hostport,dn,attrs_str,scope_str,filterstr
    )
    if self.extensions:
      ldap_url = ldap_url+'?'+self.extensions.unparse()
    return ldap_url.encode('ascii')
  
  def htmlHREF(self,urlPrefix='',hrefText=None,hrefTarget=None):
    """Complete """
    assert type(urlPrefix)==StringType, "urlPrefix must be StringType"
    if hrefText is None:
      hrefText = self.unparse()
    assert type(hrefText)==StringType, "hrefText must be StringType"
    if hrefTarget is None:
      target = ''
    else:
      assert type(hrefTarget)==StringType, "hrefTarget must be StringType"
      target = ' target="%s"' % hrefTarget
    return '<a%s href="%s%s">%s</a>' % (
      target,urlPrefix,self.unparse(),hrefText
    )

  def __str__(self):
    return self.unparse()

  def __repr__(self):
    return '<%s.%s instance at %s: %s>' % (
      self.__class__.__module__,
      self.__class__.__name__,
      hex(id(self)),
      self.__dict__
    )

  def __getattr__(self,name):
    if self.attr2extype.has_key(name):
      extype = self.attr2extype[name]
      if self.extensions.has_key(extype):
        result = unquote_plus(
          self.extensions[extype].exvalue
        )
      else:
        return None
    else:
      raise AttributeError,"%s has no attribute %s" % (
        self.__class__.__name__,name
      )
    return result # __getattr__()

  def __setattr__(self,name,value):
    if self.attr2extype.has_key(name):
      extype = self.attr2extype[name]
      if value is None:
        # A value of None means that extension is deleted
        delattr(self,name)
      elif value!=None:
        # Add appropriate extension
        self.extensions[extype] = LDAPUrlExtension(
          extype=extype,exvalue=unquote_plus(value)
        )
    else:
      self.__dict__[name] = value

  def __delattr__(self,name):
    if self.attr2extype.has_key(name):
      extype = self.attr2extype[name]
      try:
        del self.extensions[extype]
      except KeyError:
        pass
    else:
      del self.__dict__[name]

