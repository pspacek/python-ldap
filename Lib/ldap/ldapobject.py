"""
ldapobject.py - mimics LDAPObject class with some extra features
written by Michael Stroeder <michael@stroeder.com>

\$Id: ldapobject.py,v 1.2 2001/12/21 17:49:07 jajcus Exp $

License:
Public domain. Do anything you want with this module.

Compability:
- Should work with Python 1.5.x+
- Needs module threading (build Python with thread support
- The behaviour of the ldapthreadlock.LDAPObject class should be
  exactly the same like _ldap.LDAPObject
- This module needs your Python installation to be built with
  thread support (module threading is imported).

Usage:
You can simply use function open() / intialize() of this module
instead of function open() / intialize() of module ldap to create
an instance of LDAPObject class.

Basically calls into the LDAP lib are serialized by the module-wide
lock _ldapmodule_lock. To avoid blocking of other threads synchronous
methods like search_s() etc. and the result() method were rewritten to do
solely asynchronous LDAP lib calls with zero timeout.

The timeout handling is done within the method result() which probably leads
to less exact timing.
"""

__version__ = '0.0.1'

__all__ = ['open','initialize','init','get_option','set_option']

import sys,time,_ldap

if __debug__:
  import sys,traceback
  _module_debug_level = 0


try:

  # Check if Python installation has thread support
  import threading

except ImportError:

  def _ldap_call(func,*args,**kwargs):
    """Wrapper function if threading module is not available"""
    return apply(func,args,kwargs)

else:

  # Global lock for serializing all calls into underlying LDAP lib
  _ldapmodule_lock = threading.Lock()

  def _ldap_call(func,*args,**kwargs):
    """Wrapper function which locks calls to func with via ldap_module_lock"""
    _ldapmodule_lock.acquire()
    try:
      result = apply(func,args,kwargs)
    finally:
      _ldapmodule_lock.release()
    return result


class LDAPObject:
  """
  Drop-in wrapper class around __ldap.LDAPObject
  """

  def __init__(
    self,
    use_threadlock=0,trace_level=0,trace_file=sys.stdout,
    host=None,uri=None,
  ):
    self._use_threadlock = use_threadlock
    self._trace_level = trace_level
    self._trace_file = trace_file
    if uri!=None:
      self._l = self._ldap_call(_ldap.intialize,uri)
    elif host!=None:
      self._l = self._ldap_call(_ldap.open,host)
    else:
      raise ValueError,"Either host or uri must be set."

  def _ldap_call(self,func,*args,**kwargs):
    """Wrapper method mainly for trace logs"""
    if __debug__:
      if self._trace_level>=1 and func.__name__!='result':
        self._trace_file.write('*** %s.%s (%s,%s)\n' % (
          self.__module__,
          self.__class__.__name__+'.'+func.__name__,
          repr(args),repr(kwargs)
        ))
        if self._trace_level>=2:
          traceback.print_stack(file=self._trace_file)
    result = _ldap_call(func,*args,**kwargs)
    if __debug__:
      if self._trace_level>=1 and result!=None and result!=(None,None):
        self._trace_file.write('=> result: %s\n' % (repr(result)))
    return result

  def __setattr__(self,name,value):
    if not name in ['_l','_use_threadlock','_trace_level','_trace_file']:
      if __debug__:
        if self._trace_level>=1:
          self._trace_file.write('*** %s:' % (self.__module__),\
            self.__class__.__name__+'.__setattr__(%s,%s)' % (name,value)
          )
          if self._trace_level>=2:
            traceback.print_stack(file=self._trace_file)
      _ldapmodule_lock.acquire()
      try:
        setattr(self._l,name,value)
      finally:
        _ldapmodule_lock.release()
    else:
      self.__dict__[name] = value

  def __getattr__(self,name):
    if not name in ['_l','_use_threadlock','_trace_level','_trace_file']:
      _ldapmodule_lock.acquire()
      try:
        value = getattr(self._l,name)
      finally:
        _ldapmodule_lock.release()
      if __debug__:
        if self._trace_level>=1:
          self._trace_file.write('*** %s:' % (self.__module__),\
            self.__class__.__name__+'.__getattr__(%s)' % (name),'=>',value
          )
          if self._trace_level>=2:
            traceback.print_stack(file=sys.stdout)
    else:
      value = self.__dict__[name]
    return value

  def abandon(self,msgid):
    """
    abandon(msgid) -> None    
        Abandons or cancels an LDAP operation in progress. The msgid should
        be the message id of an outstanding LDAP operation as returned
        by the asynchronous methods search(), modify() etc.  The caller
        can expect that the result of an abandoned operation will not be
        returned from a future call to result().
    """
    return self._ldap_call(self._l.abandon,msgid)

  def add(self,dn,modlist):
    """
    add(dn, modlist) -> int    
        This function is similar to modify(), except that no operation
        integer need be included in the tuples.
    """
    return self._ldap_call(self._l.add,dn,modlist)

  def add_s(self,dn,modlist):
    msgid = self.add(dn,modlist)
    return self.result(msgid)

  def bind(self,who,cred,method):
    """
    bind(who, cred, method) -> int
    """
    return self._ldap_call(self._l.bind,who,cred,method)

  def bind_s(self,who,cred,method):
    """
    bind_s(who, cred, method) -> None
    """
    msgid = self.bind(who,cred,method)
    return self.result(msgid)

  def compare(self,*args,**kwargs):
    """
    compare(dn, attr, value) -> int
    compare_s(dn, attr, value) -> int    
        Perform an LDAP comparison between the attribute named attr of
        entry dn, and the value value. The synchronous form returns 0
        for false, or 1 for true.  The asynchronous form returns the
        message id of the initiates request, and the result of the
        asynchronous compare can be obtained using result().

        Note that this latter technique yields the answer by raising
        the exception objects COMPARE_TRUE or COMPARE_FALSE.

        A design bug in the library prevents value from containing
        nul characters.
    """
    return self._ldap_call(self._l.compare,*args,**kwargs)

  def compare_s(self,*args,**kwargs):
    msgid = self.compare(*args,**kwargs)
    return self.result(msgid)

  def delete(self,dn):
    """
    delete(dn) -> int
    delete_s(dn) -> None    
        Performs an LDAP delete operation on dn. The asynchronous
        form returns the message id of the initiated request, and the
        result can be obtained from a subsequent call to result().
    """
    return self._ldap_call(self._l.delete,dn)

  def delete_s(self,dn):
    msgid = self.delete(dn)
    return self.result(msgid)

  def destroy_cache(self):
    """
    destroy_cache() -> None    
        Turns off caching and removed it from memory.
    """
    return self._ldap_call(self._l.destroy_cache,)

  def disable_cache(self):
    """
    disable_cache() -> None    
        Temporarily disables use of the cache. New requests are
        not cached, and the cache is not checked when returning
        results. Cache contents are not deleted.
    """
    return self._ldap_call(self._l.disable_cache,)

  def enable_cache(self,timeout=_ldap.NO_LIMIT,maxmem=_ldap.NO_LIMIT):
    """
    enable_cache([timeout=NO_LIMIT, [maxmem=NO_LIMIT]]) -> None    
        Using a cache often greatly improves performance. By default
        the cache is disabled. Specifying timeout in seconds is used
        to decide how long to keep cached requests. The maxmem value
        is in bytes, and is used to set an upper bound on how much
        memory the cache will use. A value of NO_LIMIT for either
        indicates unlimited.  Subsequent calls to enable_cache()
        can be used to adjust these parameters.

        This and other caching methods are not available if the library
        and the ldap module were compiled with support for it.
    """
    return self._ldap_call(self._l.enable_cache,timeout,maxmem)

  def fileno(self):
    """
    fileno() -> int
        Return the file descriptor associated with this connection.
    """
    return self._ldap_call(self._l.fileno,)

  def flush_cache(self):
    """
    flush_cache() -> None    
        Deletes the cache's contents, but does not affect it in any other way.
    """
    return self._ldap_call(self._l.flush_cache)

  def modify(self,dn,modlist):
    """
    modify(dn, modlist) -> int
    modify_s(dn, modlist) -> None    
        Performs an LDAP modify operation on an entry's attributes.
        dn is the DN of the entry to modify, and modlist is the list
        of modifications to make to the entry.

        Each element of the list modlist should be a tuple of the form
        (mod_op,mod_type,mod_vals), where mod_op is the operation (one
        of MOD_ADD, MOD_DELETE, or MOD_REPLACE), mod_type is a string
        indicating the attribute type name, and mod_vals is either
        a string value or a list of string values to add, delete or
        replace respectively.  For the delete operation, mod_vals may
        be None indicating that all attributes are to be deleted.

        The asynchronous modify() returns the message id of the
        initiated request.
    """
    return self._ldap_call(self._l.modify,dn,modlist)

  def modify_s(self,dn,modlist):
    return self._ldap_call(self._l.modify_s,dn,modlist)

  def modrdn(self,dn,newrdn,delold=1):
    """
    modrdn(dn, newrdn [,delold=1]) -> int
    modrdn_s(dn, newrdn [,delold=1]) -> None    
        Perform a modify RDN operation. These routines take dn, the
        DN of the entry whose RDN is to be changed, and newrdn, the
        new RDN to give to the entry. The optional parameter delold
        is used to specify whether the old RDN should be kept as
        an attribute of the entry or not.  The asynchronous version
        returns the initiated message id.

        This actually corresponds to the modrdn2* routines in the
        C library.
    """
    return self._ldap_call(self._l.modrdn,dn,newrdn,delold)

  def modrdn_s(self,dn,newrdn,delold=1):
    msgid = self.modrdn(dn,newrdn,delold)
    return self.result(msgid)

  def rename(self,dn,newrdn,newSuperior,delold=1):
    """
    rename(dn, newrdn, newSuperior, [,delold=1]) -> int
    rename_s(dn, newrdn, newSuperior, [,delold=1]) -> None    
        Perform a rename entry operation. These routines take dn, the
        DN of the entry whose RDN is to be changed, newrdn, the
        new RDN, and newSuperior, the new parent DN, to give to the entry.
        The optional parameter delold
        is used to specify whether the old RDN should be kept as
        an attribute of the entry or not.  The asynchronous version
        returns the initiated message id.

        This actually corresponds to the rename* routines in the
        LDAP-EXT C API library.
    """
    return self._ldap_call(self._l.rename,dn,newrdn,newSuperior,delold)

  def rename_s(self,dn,newrdn,newSuperior,delold=1):
    msgid = self.rename(dn,newrdn,newSuperior,delold)
    return self.result(msgid)

  def result(self,msgid=_ldap.RES_ANY,all=1,timeout=-1):
    """
    result([msgid=RES_ANY [,all=1 [,timeout=-1]]]) -> (result_type, result_data)

        This method is used to wait for and return the result of an
        operation previously initiated by one of the LDAP asynchronous
        operation routines (eg search(), modify(), etc.) They all
        returned an invocation identifier (a message id) upon successful
        initiation of their operation. This id is guaranteed to be
        unique across an LDAP session, and can be used to request the
        result of a specific operation via the msgid parameter of the
        result() method.

        If the result of a specific operation is required, msgid should
        be set to the invocation message id returned when the operation
        was initiated; otherwise RES_ANY should be supplied.

        The all parameter only has meaning for search() responses
        and is used to select whether a single entry of the search
        response should be returned, or to wait for all the results
        of the search before returning.

        A search response is made up of zero or more search entries
        followed by a search result. If all is 0, search entries will
        be returned one at a time as they come in, via separate calls
        to result(). If all is 1, the search response will be returned
        in its entirety, i.e. after all entries and the final search
        result have been received.

        The method returns a tuple of the form (result_type,
        result_data).  The result_type is a string, being one of:
        'RES_BIND', 'RES_SEARCH_ENTRY', 'RES_SEARCH_RESULT',
        'RES_MODIFY', 'RES_ADD', 'RES_DELETE', 'RES_MODRDN', or
        'RES_COMPARE'.

        The constants RES_* are set to these strings, for convenience.

        See search() for a description of the search result's
        result_data, otherwise the result_data is normally meaningless.

        The result() method will block for timeout seconds, or
        indefinitely if timeout is negative.  A timeout of 0 will effect
        a poll.  The timeout can be expressed as a floating-point value.

        If a timeout occurs, a TIMEOUT exception is raised, unless
        polling (timeout = 0), in which case (None, None) is returned.
    """
    if timeout==0:
      return self._ldap_call(self._l.result,msgid,all,0)
    else:
      result_ldap = None
      start_time = time.time()
      while (result_ldap is None) or (result_ldap==(None,None)):
        if (timeout>0) and (time.time()-start_time>timeout):
          self._ldap_call(self._l.abandon,msgid)
          raise _ldap.TIMELIMIT_EXCEEDED(
            "LDAP time limit (%d secs) exceeded." % (timeout)
          )
        result_ldap = self._ldap_call(self._l.result,msgid,all,0)
      return result_ldap

  def search(self,base,scope,filterstr,attrlist=None,attrsonly=0):
    """
    search(base, scope, filter [,attrlist=None [,attrsonly=0]]) -> int
    search_s(base, scope, filter [,attrlist=None [,attrsonly=0]])
    search_st(base, scope, filter [,attrlist=None [,attrsonly=0 [,timeout=-1]]])

        Perform an LDAP search operation, with base as the DN of
        the entry at which to start the search, scope being one of
        SCOPE_BASE (to search the object itself), SCOPE_ONELEVEL
        (to search the object's immediate children), or SCOPE_SUBTREE
        (to search the object and all its descendants).

        filter is a string representation of the filter to
        apply in the search (see RFC 2254).

        When using the asynchronous form and result(), the all parameter
        affects how results come in.  For all set to 0, result tuples
        trickle in (with the same message id), and with the result type
        RES_SEARCH_ENTRY, until the final result which has a result
        type of RES_SEARCH_RESULT and a (usually) empty data field.
        When all is set to 1, only one result is returned, with a
        result type of RES_SEARCH_RESULT, and all the result tuples
        listed in the data field.

        Each result tuple is of the form (dn,entry), where dn is a
        string containing the DN (distinguished name) of the entry, and
        entry is a dictionary containing the attributes.
        Attributes types are used as string dictionary keys and attribute
        values are stored in a list as dictionary value.

        The DN in dn is extracted using the underlying ldap_get_dn(),
        which may raise an exception of the DN is malformed.

        If attrsonly is non-zero, the values of attrs will be
        meaningless (they are not transmitted in the result).

        The retrieved attributes can be limited with the attrlist
        parameter.  If attrlist is None, all the attributes of each
        entry are returned.

        The synchronous form with timeout, search_st(), will block
        for at most timeout seconds (or indefinitely if timeout is
        negative). A TIMEOUT exception is raised if no result is
        received within the time.
    """
    return self._ldap_call(self._l.search,base,scope,filterstr,attrlist,attrsonly)

  def search_s(self,base,scope,filterstr,attrlist=None,attrsonly=0):
    return self.search_st(base,scope,filterstr,attrlist,attrsonly,timeout=-1)

  def search_st(self,base,scope,filterstr,attrlist=None,attrsonly=0,timeout=-1):
    msgid = self.search(base,scope,filterstr,attrlist,attrsonly)
    result = []
    result_type,result_data = self.result(msgid,0,timeout)
    while result_data:
      result.extend(result_data)
      result_type,result_data = self.result(msgid,0,timeout)
    return result

  def set_cache_options(self,*args,**kwargs):
    """
    set_cache_options(option) -> None    
        Changes the caching behaviour. Currently supported options are
            CACHE_OPT_CACHENOERRS, which suppresses caching of requests
                that resulted in an error, and
            CACHE_OPT_CACHEALLERRS, which enables caching of all requests.
        The default behaviour is not to cache requests that result in
        errors, except those that result in a SIZELIMIT_EXCEEDED exception.
    """
    return self._ldap_call(self._l.set_cache_options,*args,**kwargs)

  def set_rebind_proc(self,func):
    """
    set_rebind_proc(func) -> None    
        If a referral is returned from the server, automatic re-binding
        can be achieved by providing a function that accepts as an
        argument the newly opened LDAP object and returns the tuple
        (who, cred, method).

        Passing a value of None for func will disable this facility.

        Because of restrictions in the implementation, only one
        rebinding function is supported at any one time. This method
        is only available if the module and library were compiled with
        support for it.
    """
    return self._ldap_call(self._l.set_rebind_proc,func)

  def simple_bind(self,who,passwd):
    """
    simple_bind(who, passwd) -> int
    """
    return self.bind(who,passwd,_ldap.AUTH_SIMPLE)

  def simple_bind_s(self,who,passwd):
    """
    simple_bind_s(who, passwd) -> None
    """
    return self.bind_s(who,passwd,_ldap.AUTH_SIMPLE)

  def start_tls_s(self,*args,**kwargs):
    """
    start_tls_s() -> None    
    Negotiate TLS with server. The `version' attribute must have been
    set to VERSION3 before calling start_tls_s.
    If TLS could not be started an exception will be raised.
    """
    return self._ldap_call(self._l.start_tls_s,*args,**kwargs)
  
  def unbind(self):
    """
    unbind_s() -> None
    unbind() -> int    
        This call is used to unbind from the directory, terminate
        the current association, and free resources. Once called, the
        connection to the LDAP server is closed and the LDAP object
        is invalid. Further invocation of methods on the object will
        yield an exception.
    
        The unbind and unbind_s methods are identical, and are
        synchronous in nature
    """
    return self._ldap_call(self._l.unbind,)

  def unbind_s(self):
    return self._ldap_call(self._l.unbind_s,)

  def uncache_entry(self,dn):
    """
    uncache_entry(dn) -> None    
        Removes all cached entries that make reference to dn. This should be
        used, for example, after doing a modify() involving dn.
    """
    return self._ldap_call(self._l.uncache_entry,dn)

  def uncache_request(self,msgid):
    """
    uncache_request(msgid) -> None    
        Remove the request indicated by msgid from the cache.
    """
    return self._ldap_call(self._l.uncache_request,msgid)

  def url_search_s(self,url,attrsonly=0):
    """
    url_search_s(url [,attrsonly=0])
    url_search_st(url [,attrsonly=0 [,timeout=-1]])
        These routine works much like search_s*, except that many
        search parameters are pulled out of the URL url (see RFC 2255).
    """
    return self.url_search_st(url,attrsonly,timeout=-1)

  def url_search_st(self,url,attrsonly=0,timeout=-1):
    return self._ldap_call(self._l.url_search_st,url,attrsonly,timeout)

  def get_option(self,*args,**kwargs):
    return self._ldap_call(self._l.get_option,*args,**kwargs)

  def set_option(self,*args,**kwargs):
    return self._ldap_call(self._l.set_option,*args,**kwargs)

def open(host,use_threadlock=0,trace_level=0,trace_file=sys.stdout):
  """
  Return LDAPObject instance by opening LDAP connection to
  specified LDAP host
  
  Parameters:
  host
        LDAP host and port
  use_threadlock
        If non-zero a global lock is used to serialize all
        calls into underlying (not thread-safe) LDAP libs.
  trace_level
        If non-zero a trace output of LDAP calls is generated.
  trace_file
        File object where to write the trace output to.
        Default is to use stdout.
  """
  return LDAPObject(use_threadlock,trace_level,trace_file,host=host)

def initialize(uri,use_threadlock=0,trace_level=0,trace_file=sys.stdout):
  """
  Return LDAPObject instance by opening LDAP connection to
  specified LDAP host
  
  Parameters:
  uri
        LDAP URL containing at least connection scheme and hostport.
  use_threadlock
        If non-zero a global lock is used to serialize all
        calls into underlying (not thread-safe) LDAP libs.
  trace_level
        If non-zero a trace output of LDAP calls is generated.
  trace_file
        File object where to write the trace output to.
        Default is to use stdout.
  """
  return LDAPObject(use_threadlock,trace_level,trace_file,uri=uri)

# init() is just an alias for initialize()
init = initialize

def get_option(*args,**kwargs):
  return _ldap_call(_ldap.get_option,*args,**kwargs)

def set_option(*args,**kwargs):
  return _ldap_call(_ldap.set_option,*args,**kwargs)

