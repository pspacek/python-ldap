# $Id: __init__.py,v 1.3 2001/12/27 10:59:08 stroeder Exp $

from _ldap import __version__

from _ldap import *


if __debug__:
  # Tracing is only supported in debugging mode
  import sys,traceback
  _module_debug_level = 0


try:

  # Check if Python installation was build with thread support
  import threading

except ImportError:

  def _ldap_call(func,*args,**kwargs):
    """
    Wrapper function if threading module is not available
    """
    return apply(func,args,kwargs)

else:

  # Global lock for serializing all calls into underlying LDAP lib
  _ldap_lock = threading.Lock()

  def _ldap_call(func,*args,**kwargs):
    """
    Wrapper function which locks calls to func with via _ldap_lock
    """
    _ldap_lock.acquire()
    try:
      result = apply(func,args,kwargs)
    finally:
      _ldap_lock.release()
    return result


from functions import *
