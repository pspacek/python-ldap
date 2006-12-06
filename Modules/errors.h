/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/* $Id: errors.h,v 1.4 2006/12/06 07:36:00 stroeder Exp $ */

#ifndef __h_errors_
#define __h_errors_

#include "common.h"
#include "lber.h"
#include "ldap.h"

extern PyObject* LDAPexception_class;
extern PyObject* LDAPerror( LDAP*, char*msg );
extern void LDAPinit_errors( PyObject* );
PyObject* LDAPerr(int errnum);

#endif /* __h_errors */
