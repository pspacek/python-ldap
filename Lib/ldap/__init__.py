# $Id: __init__.py,v 1.7 2002/02/02 11:15:49 stroeder Exp $

__version__ = '2.0.0pre04'

from _ldap import *

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
