/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/* 
 * LDAP module
 * $Id: ldapmodule.c,v 1.7 2005/06/14 17:49:14 stroeder Exp $
 */

#include "common.h"
#include "version.h"
#include "constants.h"
#include "errors.h"
#include "functions.h"
#include "schema.h"
#include "ldapcontrol.h"

#include "LDAPObject.h"

DL_EXPORT(void) init_ldap(void);

/* dummy module methods */

static PyMethodDef methods[]  = {
	{ NULL, NULL }
};

/* module initialisation */

DL_EXPORT(void)
init_ldap()
{
	PyObject *m, *d;

#if defined(MS_WINDOWS) || defined(__CYGWIN__)
	LDAP_Type.ob_type = &PyType_Type;
#endif

	/* Create the module and add the functions */
	m = Py_InitModule("_ldap", methods);

	/* Add some symbolic constants to the module */
	d = PyModule_GetDict(m);

	LDAPinit_version(d);
	LDAPinit_constants(d);
	LDAPinit_errors(d);
	LDAPinit_functions(d);
	LDAPinit_schema(d);
	LDAPinit_control(d);

	/* Check for errors */
	if (PyErr_Occurred())
		Py_FatalError("can't initialize module _ldap");
}
