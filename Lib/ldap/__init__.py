"""
ldap - base module
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

$Id: __init__.py,v 1.42 2005/04/29 11:33:17 stroeder Exp $
"""

__version__ = '2.0.7'

import sys

if __debug__:
  # Tracing is only supported in debugging mode
  import traceback
  _trace_level = 0
  _trace_file = sys.stderr
  _trace_stack_limit = None

from _ldap import *

class DummyLock:
  """Define dummy class with methods compatible to threading.Lock"""
  def __init__(self):
    pass
  def acquire(self):
    pass
  def release(self):
    pass


try:
  # Check if Python installation was build with thread support
  import thread
except ImportError:
  LDAPLock = DummyLock
else:
  import threading
  LDAPLock = threading.Lock

# Create module-wide lock for serializing all calls
# into underlying LDAP lib
_ldap_module_lock = LDAPLock()

from functions import open,initialize,init,explode_dn,explode_rdn,get_option,set_option

