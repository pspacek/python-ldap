/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/* 
 * version info
 * $Id: version.c,v 1.2 2000/08/14 22:37:37 leonard Exp $
 */

#include "common.h"

#define _STR(x)	#x
#define STR(x)	_STR(x)

static char version_str[] = STR(LDAPMODULE_VERSION);

void
LDAPinit_version( PyObject* d ) 
{
	PyObject *version;

	version = PyString_FromString(version_str);
	PyDict_SetItemString( d, "__version__", version );
	Py_DECREF(version);
}
