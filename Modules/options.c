/* 
 * Options support
 * $Id: options.c,v 1.1 2001/11/14 23:22:18 leonard Exp $
 */

#include "common.h"
#include "errors.h"
#include "LDAPObject.h"
#include "options.h"

/* List of attributes that that are visible through attributes */
static struct {
	const char *attrname;
	int	option;
} option_attributes[] = {
	{ "protocol_version",	LDAP_OPT_PROTOCOL_VERSION },
	{ "deref",		LDAP_OPT_DEREF },
	{ "referrals",		LDAP_OPT_REFERRALS },
	{ "timelimit",		LDAP_OPT_TIMELIMIT },
	{ "sizelimit",		LDAP_OPT_SIZELIMIT },
	{ "error_number",	LDAP_OPT_ERROR_NUMBER },
	{ "error_string",	LDAP_OPT_ERROR_STRING },
	{ "matched_dn",		LDAP_OPT_MATCHED_DN },
};
#define lengthof(a) (sizeof (a) / sizeof (a)[0])

int
LDAP_optionval_by_name(const char *name)
{
	int i;

	for (i = 0; i < lengthof(option_attributes); i++)
	    if (strcmp(option_attributes[i].attrname, name) == 0)
		return option_attributes[i].option;
	return -1;
}

int
LDAP_set_option(LDAPObject *self, int option, PyObject *value)
{
    int res;
    int intval;
    char *strval;
    void *ptr;
    LDAP *ld;

    ld = self ? self->ldap : NULL;

    switch(option) {
    case LDAP_OPT_API_INFO:
    case LDAP_OPT_DESC:
    case LDAP_OPT_API_FEATURE_INFO:
    case LDAP_OPT_X_SASL_SSF:
	    /* Read-only options */
	    PyErr_SetString(PyExc_ValueError, "read-only option");
	    return -1;

    case LDAP_OPT_REFERRALS:
    case LDAP_OPT_RESTART:
	    /* Truth-value options */
	    ptr = PyObject_IsTrue(value) ? LDAP_OPT_ON : LDAP_OPT_OFF;
	    break;

    case LDAP_OPT_DEREF:
    case LDAP_OPT_SIZELIMIT:
    case LDAP_OPT_TIMELIMIT:
    case LDAP_OPT_PROTOCOL_VERSION:
    case LDAP_OPT_ERROR_NUMBER:
    case LDAP_OPT_DEBUG_LEVEL:
    case LDAP_OPT_X_TLS:
    case LDAP_OPT_X_TLS_REQUIRE_CERT:
    case LDAP_OPT_X_SASL_SSF_MIN:
    case LDAP_OPT_X_SASL_SSF_MAX:
	    /* integer value options */
	    if (!PyArg_Parse(value, "i:set_option", &intval))
		return NULL;
	    ptr = &intval;
	    break;

    case LDAP_OPT_HOST_NAME:
    case LDAP_OPT_URI:
    case LDAP_OPT_ERROR_STRING:
    case LDAP_OPT_MATCHED_DN:
    case LDAP_OPT_X_TLS_CACERTFILE:
    case LDAP_OPT_X_TLS_CACERTDIR:
    case LDAP_OPT_X_TLS_CERTFILE:
    case LDAP_OPT_X_TLS_KEYFILE:
    case LDAP_OPT_X_TLS_CIPHER_SUITE:
    case LDAP_OPT_X_TLS_RANDOM_FILE:
    case LDAP_OPT_X_SASL_SECPROPS:
	    /* String valued options */
	    if (!PyArg_Parse(value, "s:set_option", &strval))
		return NULL;
	    ptr = strval;
	    break;

    case LDAP_OPT_SERVER_CONTROLS:
    case LDAP_OPT_CLIENT_CONTROLS:
    case LDAP_OPT_TIMEOUT:
    case LDAP_OPT_NETWORK_TIMEOUT:
    case LDAP_OPT_X_TLS_CTX:
	    PyErr_SetString(PyExc_NotImplementedError,
		"option not yet supported");
	    return -1;

    default:
	    PyErr_SetNone(PyExc_ValueError);
	    return -1;
    }
	
    if (self) LDAP_BEGIN_ALLOW_THREADS(self);
    res = ldap_set_option(ld, option, ptr);
    if (self) LDAP_END_ALLOW_THREADS(self);

    if (res != LDAP_OPT_SUCCESS) {
	LDAPerr(res);
	return -1;
    }

    return 0;
}

PyObject *
LDAP_get_option(LDAPObject *self, int option)
{
    int res;
    int intval;
    LDAPAPIInfo apiinfo;
    char *strval;
    PyObject *extensions, *v;
    int i, num_extensions;
    LDAP *ld;

    ld = self ? self->ldap : NULL;

    switch(option) {
    case LDAP_OPT_API_INFO:
	    apiinfo.ldapai_info_version = LDAP_API_INFO_VERSION;
	    if (self) LDAP_BEGIN_ALLOW_THREADS(self);
	    res = ldap_get_option( ld, option, &apiinfo );
	    if (self) LDAP_END_ALLOW_THREADS(self);
	    if (res != LDAP_OPT_SUCCESS)
		return LDAPerr(res);
    
	    /* put the extensions into tuple form */
	    num_extensions = 0;
	    while (apiinfo.ldapai_extensions[num_extensions])
		num_extensions++;
	    extensions = PyTuple_New(num_extensions);
	    for (i = 0; i < num_extensions; i++)
		PyTuple_SET_ITEM(extensions, i,
		    PyString_FromString(apiinfo.ldapai_extensions[i]));

	    /* return api info as a dictionary */
	    v = Py_BuildValue("{s:i, s:i, s:i, s:i, s:i, s:O}",
		    "info_version",     apiinfo.ldapai_info_version,
		    "api_version",      apiinfo.ldapai_api_version,
		    "protocol_version", apiinfo.ldapai_protocol_version,
		    "vendor_name",      apiinfo.ldapai_vendor_name,
		    "vendor_version",   apiinfo.ldapai_vendor_version,
		    "extensions",       extensions);
	    Py_DECREF(extensions);
	    return v;

    case LDAP_OPT_X_SASL_SSF:
    case LDAP_OPT_REFERRALS:
    case LDAP_OPT_RESTART:
    case LDAP_OPT_DESC:
    case LDAP_OPT_DEREF:
    case LDAP_OPT_SIZELIMIT:
    case LDAP_OPT_TIMELIMIT:
    case LDAP_OPT_PROTOCOL_VERSION:
    case LDAP_OPT_ERROR_NUMBER:
    case LDAP_OPT_DEBUG_LEVEL:
    case LDAP_OPT_X_TLS:
    case LDAP_OPT_X_TLS_REQUIRE_CERT:
    case LDAP_OPT_X_SASL_SSF_MIN:
    case LDAP_OPT_X_SASL_SSF_MAX:
	    /* Integer-valued options */
	    if (self) LDAP_BEGIN_ALLOW_THREADS(self);
	    res = ldap_get_option(ld, option, &intval);
	    if (self) LDAP_END_ALLOW_THREADS(self);
	    if (res != LDAP_OPT_SUCCESS)
		return LDAPerr(res);
	    return PyInt_FromLong(intval);

    case LDAP_OPT_HOST_NAME:
    case LDAP_OPT_URI:
    case LDAP_OPT_ERROR_STRING:
    case LDAP_OPT_MATCHED_DN:
    case LDAP_OPT_X_TLS_CACERTFILE:
    case LDAP_OPT_X_TLS_CACERTDIR:
    case LDAP_OPT_X_TLS_CERTFILE:
    case LDAP_OPT_X_TLS_KEYFILE:
    case LDAP_OPT_X_TLS_CIPHER_SUITE:
    case LDAP_OPT_X_TLS_RANDOM_FILE:
    case LDAP_OPT_X_SASL_SECPROPS:
	    /* String-valued options */
	    if (self) LDAP_BEGIN_ALLOW_THREADS(self);
	    res = ldap_get_option(ld, option, &strval);
	    if (self) LDAP_END_ALLOW_THREADS(self);
	    if (res != LDAP_OPT_SUCCESS)
		return LDAPerr(res);
	    return PyString_FromString(strval);

    case LDAP_OPT_SERVER_CONTROLS:
    case LDAP_OPT_CLIENT_CONTROLS:
    case LDAP_OPT_TIMEOUT:
    case LDAP_OPT_NETWORK_TIMEOUT:
    case LDAP_OPT_API_FEATURE_INFO:
    case LDAP_OPT_X_TLS_CTX:
	    /* Unsupported options */
	    PyErr_SetString(PyExc_NotImplementedError,
		"option not yet supported");
	    return NULL;

    default:
	    PyErr_SetObject(PyExc_ValueError, Py_None);
	    return NULL;
    }
}
