/* $Id: options.h,v 1.1 2001/11/14 23:22:18 leonard Exp $ */

int	LDAP_optionval_by_name(const char *name);
int	LDAP_set_option(LDAPObject *self, int option, PyObject *value);
PyObject *LDAP_get_option(LDAPObject *self, int option);
