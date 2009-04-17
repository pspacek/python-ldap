/* See http://www.python-ldap.org/ for details.
 * $Id: ldapcontrol.h,v 1.5 2009/04/17 12:19:09 stroeder Exp $ */

#ifndef __h_ldapcontrol
#define __h_ldapcontrol

#include "common.h"
#include "ldap.h"

void LDAPinit_control(PyObject *d);
void LDAPControl_List_DEL( LDAPControl** );
LDAPControl** List_to_LDAPControls( PyObject* );
PyObject* LDAPControls_to_List(LDAPControl **ldcs);

#endif /* __h_ldapcontrol */
