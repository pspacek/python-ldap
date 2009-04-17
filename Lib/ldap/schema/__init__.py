"""
ldap.schema -  LDAPv3 schema handling

See http://www.python-ldap.org/ for details.

\$Id: __init__.py,v 1.6 2009/04/17 14:36:16 stroeder Exp $
"""

__version__ = '0.2.1'

from ldap.schema.subentry import SubSchema,SCHEMA_ATTRS,SCHEMA_CLASS_MAPPING,SCHEMA_ATTR_MAPPING,urlfetch
from ldap.schema.models import *
