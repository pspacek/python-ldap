#! /usr/bin/env python
# $Id: setup.py,v 1.25 2002/07/02 14:31:39 stroeder Exp $

from distutils.core import setup, Extension
from ConfigParser import ConfigParser
import sys,string

#-- Release version of Python-ldap
version = '2.0.0pre05'

#-- A class describing the features and requirements of OpenLDAP 2.0
class OpenLDAP2:
	library_dirs =	[ ]
	include_dirs =	[ ]
	libs =		['ldap', 'lber']
	defines =	[
			 #('WITH_KERBEROS', None),
			 #('HAVE_DES_SETKEY', None),
			 ('LDAP_TYPE_IS_OPAQUE', None),
			 ('HAVE_LDAP_DESTROY_CACHE', None),
			 ('HAVE_LDAP_DISABLE_CACHE', None),
			 ('HAVE_LDAP_ENABLE_CACHE', None),
			 ('HAVE_LDAP_FLUSH_CACHE', None),
			 ('HAVE_LDAP_MODRDN2', None),
			 ('HAVE_LDAP_MODRDN2_S', None),
			 ('HAVE_LDAP_SET_CACHE_OPTIONS', None),
			 ('HAVE_LDAP_START_TLS_S', None),
			 ('HAVE_LDAP_UNCACHE_ENTRY', None),
			 ('HAVE_LDAP_UNCACHE_REQUEST', None),
#			 ('HAVE_LDAP_INIT_TEMPLATES', None),
#			 ('HAVE_DISPTMPL_H', None),
			]

#-- Read the [_ldap] section of setup.cfg to find out which class to use
cfg = ConfigParser()
cfg.read('setup.cfg')
if cfg.has_section('_ldap'):
    if cfg.has_option('_ldap', 'class'):
	LDAP_CLASS = eval(cfg.get('_ldap', 'class'))
    else:
	LDAP_CLASS = OpenLDAP2
    for name in 'library_dirs', 'include_dirs', 'libs':
	if cfg.has_option('_ldap', name):
	    setattr(LDAP_CLASS, name, string.split(cfg.get('_ldap', name)))
else:
    LDAP_CLASS = OpenLDAP2

#-- Let distutils do the rest
setup(
	#-- Package description
	name =		'python-ldap',
	version =	version,
	description =	'Various LDAP-related Python modules',
	author =	'David Leonard et al.', 
	author_email =	'python-ldap-dev@lists.sourceforge.net',
	url =		'http://python-ldap.sourceforge.net/',
	#-- C extension modules
	ext_modules = [
		Extension(
		    '_ldap',
		    [
			'Modules/LDAPObject.c',
			'Modules/common.c',
			'Modules/constants.c',
			'Modules/errors.c',
			'Modules/functions.c',
			'Modules/schema.c',
			'Modules/ldapmodule.c',
			'Modules/linkedlist.c',
			'Modules/message.c',
			'Modules/template.c',
			'Modules/version.c',
			'Modules/options.c',
		    ],
		    libraries =		LDAP_CLASS.libs,
		    include_dirs =	['Modules'] + LDAP_CLASS.include_dirs,
		    library_dirs =	LDAP_CLASS.library_dirs,
#		    runtime_library_dirs = LDAP_CLASS.library_dirs,
		    define_macros =	LDAP_CLASS.defines + \
              ('ldap_r' in LDAP_CLASS.libs)*[('HAVE_LIBLDAP_R',None)] + \
              [('LDAPMODULE_VERSION', version)]
		),
	],
	#-- Python modules
	py_modules = [
                'ldap',
                'ldap.async',
                'ldap.functions',
		'ldap.sasl',
		'ldap.schema',
                'ldap.ldapobject',
                'ldap.modlist',
                'ldapurl',
		'ldif',
		#'perldap',
	],
	#-- where to find the python modules
	package_dir = { '': 'Lib' },
)

