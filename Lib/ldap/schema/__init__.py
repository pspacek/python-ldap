"""
ldap.schema -  LDAPv3 schema handling
written by Michael Stroeder <michael@stroeder.com>

\$Id: __init__.py,v 1.1 2002/09/04 16:08:46 stroeder Exp $
"""

__version__ = '0.2.0'

from ldap.schema.subentry import SubSchema,SCHEMA_ATTRS,SCHEMA_CLASS_MAPPING,urlfetch
from ldap.schema.models import *
