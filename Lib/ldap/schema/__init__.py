"""
ldap.schema -  LDAPv3 schema handling
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

\$Id: __init__.py,v 1.3 2002/09/22 02:10:39 stroeder Exp $
"""

__version__ = '0.2.0'

from ldap.schema.subentry import SubSchema,SCHEMA_ATTRS,SCHEMA_CLASS_MAPPING,SCHEMA_ATTR_MAPPING,urlfetch
from ldap.schema.models import *
