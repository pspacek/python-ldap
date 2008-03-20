/* See http://python-ldap.sourceforge.net for details.
 * $Id: options.h,v 1.3 2008/03/20 12:24:56 stroeder Exp $ */

int	LDAP_optionval_by_name(const char *name);
int	LDAP_set_option(LDAPObject *self, int option, PyObject *value);
PyObject *LDAP_get_option(LDAPObject *self, int option);

void set_timeval_from_double( struct timeval *tv, double d );
