/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/* 
 * version info
 * $Id: version.c,v 1.1 2000/07/27 16:08:58 leonard Exp $
 */

#include "common.h"

#define _STR(x)	#x
#define STR(x)	_STR(x)

static char version_str[] = STR(LDAPMODULE_VERSION);

void
LDAPinit_version( PyObject* d ) 
{
	PyDict_SetItemString( d, "__version__", 
				PyString_FromString(version_str) );
}
