/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
#ifndef __h_message 
#define __h_message 

/* $Id: message.h,v 1.2 2003/10/28 10:32:21 stroeder Exp $ */

#include "Python.h"
#include "lber.h"
#include "ldap.h"

extern PyObject* LDAPmessage_to_python( LDAP*ld, LDAPMessage*m );

#endif /* __h_message_ */

