"""
Various examples how to connect to a LDAP host with the new
factory function ldap.initialize() introduced in OpenLDAP 2 API.

Assuming you have LDAP servers running on
ldap://localhost:1389 (LDAP with StartTLS)
ldaps://localhost:1636 (LDAP over SSL)
ldapi://%2ftmp%2fopenldap2 (domain socket /tmp/openldap2)
"""

import ldap

# Set debugging level
ldap.set_option(ldap.OPT_DEBUG_LEVEL,255)

ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,'/etc/httpd/ssl.crt/myCA-cacerts.pem')

##################################################################
# LDAPv3 connection with StartTLS
##################################################################

# Create LDAPObject instance
l = ldap.initialize('ldap://localhost:1389')

# Set LDAP protocol version used
l.protocol_version=ldap.VERSION3

l.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)

# Try a bind to provoke failure if protocol version is not supported
l.bind_s('','',ldap.AUTH_SIMPLE)

# Now try StartTLS
l.start_tls_s()

# Close connection
l.unbind_s()

##################################################################
# LDAPv3 connection over SSL
##################################################################

# Create LDAPObject instance
l = ldap.initialize('ldaps://localhost:1636')

# Set LDAP protocol version used
l.protocol_version=ldap.VERSION3

# Try a bind to provoke failure if protocol version is not supported
l.bind_s('','',ldap.AUTH_SIMPLE)

# Close connection
l.unbind_s()

##################################################################
# LDAPv3 connection over local domain socket
##################################################################

# Create LDAPObject instance
l = ldap.initialize('ldapi://%2ftmp%2fopenldap2')

# Set LDAP protocol version used
l.protocol_version=ldap.VERSION3

# Try a bind to provoke failure if protocol version is not supported
l.bind_s('','',ldap.AUTH_SIMPLE)

# Close connection
l.unbind_s()

