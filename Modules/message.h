/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
#ifndef __h_message 
#define __h_message 

/* $Id: message.h,v 1.1 2000/07/27 16:08:58 leonard Exp $ */

#include "lber.h"
#include "ldap.h"
#include "Python.h"

extern PyObject* LDAPmessage_to_python( LDAP*ld, LDAPMessage*m );

#endif /* __h_message_ */

