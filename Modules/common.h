/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/*
 * common utility macros
 *
 * $Id: common.h,v 1.4 2004/10/06 21:26:07 stroeder Exp $ 
 */

#include "Python.h"

#ifndef __h_common 
#define __h_common 

#if defined(HAVE_CONFIG_H)
#include "config.h"
#endif

#if defined(MS_WINDOWS)
#include <winsock.h>
#else /* unix */
#include <netdb.h>
#include <sys/time.h>
#include <sys/types.h>
#endif

#include <string.h>
#define streq( a, b ) \
	( (*(a)==*(b)) && 0==strcmp(a,b) )

void LDAPadd_methods( PyObject*d, PyMethodDef*methods );
#define PyNone_Check(o) ((o) == Py_None)

#endif /* __h_common_ */

