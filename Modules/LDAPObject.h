/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
#ifndef __h_LDAPObject 
#define __h_LDAPObject 

/* $Id: LDAPObject.h,v 1.6 2005/02/25 16:38:26 stroeder Exp $ */

#include "Python.h"

#include "lber.h"
#include "ldap.h"
#if LDAP_API_VERSION < 2000
#error Current python-ldap requires OpenLDAP 2.x
#endif

#if PYTHON_API_VERSION < 1007
typedef PyObject*	_threadstate;
#else
typedef PyThreadState*	_threadstate;
#endif

typedef struct {
        PyObject_HEAD
	LDAP* ldap;
	_threadstate	_save; /* for thread saving on referrals */
	int valid;
} LDAPObject;

extern PyTypeObject LDAP_Type;
#define LDAPObject_Check(v)     ((v)->ob_type == &LDAP_Type)

extern LDAPObject *newLDAPObject( LDAP* );

LDAPControl **List_to_LDAPControls( PyObject* );
void LDAPControl_List_DEL( LDAPControl** );

/* macros to allow thread saving in the context of an LDAP connection */

#define LDAP_BEGIN_ALLOW_THREADS( l )                                   \
	{                                                               \
	  LDAPObject *lo = (l);                                         \
	  if (lo->_save != NULL)                                        \
	  	Py_FatalError( "saving thread twice?" );                \
	  lo->_save = PyEval_SaveThread();                              \
	}

#define LDAP_END_ALLOW_THREADS( l )                                     \
	{                                                               \
	  LDAPObject *lo = (l);                                         \
	  _threadstate _save = lo->_save;                               \
	  lo->_save = NULL;                                             \
	  PyEval_RestoreThread( _save );                                \
	}

#endif /* __h_LDAPObject */

