/* $Id: acconfig.h,v 1.1 2000/07/27 16:08:57 leonard Exp $ */
@TOP@

/*
 * Module version
 */
#define LDAPMODULE_VERSION	major.minor

/*
 * Case-insensitive dictionary used for evil LDAP server responses
 */
#undef USE_CIDICT

/*
 * Use Kerberos authentication
 */
#undef WITH_KERBEROS

/*
 * ldap_set_rebind_proc() with three arguments (Solaris, not OpenLDAP)
 */
#undef LDAP_SET_REBIND_PROC_3ARGS

/*
 * 'LDAP' is an opaque data type, struct ldap, in ldap.h (iSolaris, Netscape)
 */
#undef LDAP_TYPE_IS_OPAQUE

/*
 * Variant forms of ldap_modrdn2
 */
#undef HAVE_LDAP_MODRDN2_S
#undef HAVE_LDAP_MODRDN2

/*
 * Are templates available?
 */
#undef HAVE_LDAP_INIT_TEMPLATES 
