/* See http://python-ldap.sourceforge.net for details.
 * $Id: message.h,v 1.4 2008/03/20 12:24:56 stroeder Exp $ */

#ifndef __h_message 
#define __h_message 

#include "common.h"
#include "lber.h"
#include "ldap.h"

extern PyObject* LDAPmessage_to_python( LDAP*ld, LDAPMessage*m );

#endif /* __h_message_ */

