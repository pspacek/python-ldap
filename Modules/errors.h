/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/* $Id: errors.h,v 1.3 2001/11/14 23:14:13 leonard Exp $ */

#ifndef __h_errors_
#define __h_errors_

#include "Python.h"
#include "lber.h"
#include "ldap.h"

extern PyObject* LDAPexception_class;
extern PyObject* LDAPerror( LDAP*, char*msg );
extern void LDAPinit_errors( PyObject* );
PyObject* LDAPerr(int errnum);

#endif /* __h_errors */
