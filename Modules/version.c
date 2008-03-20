/* Set release version
 * See http://python-ldap.sourceforge.net for details.
 * $Id: version.c,v 1.3 2008/03/20 12:24:56 stroeder Exp $ */

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
