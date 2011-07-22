.. % $Id: ldap-controls.rst,v 1.7 2011/07/22 20:19:54 stroeder Exp $


*********************************************************************
:py:mod:`ldap.controls` High-level access to LDAPv3 extended controls
*********************************************************************

.. py:module:: ldap.controls
   :synopsis: High-level access to LDAPv3 extended controls.
.. moduleauthor:: python-ldap project (see http://www.python-ldap.org/)


Variables
=========

.. py:data:: KNOWN_RESPONSE_CONTROLS

   Dictionary mapping the OIDs of known response controls to the accompanying
   :py:class:`ResponseControl` classes. This is used
   by :py:func:`DecodeControlTuples` to automatically decode control values.
   Calling application can also register their custom :py:class:`ResponseControl`
   classes in this dictionary possibly overriding pre-registered classes.
   

Classes
=======

This module defines the following classes:


.. autoclass:: ldap.controls.RequestControl
   :members:

.. autoclass:: ldap.controls.ResponseControl
   :members:

.. autoclass:: ldap.controls.LDAPControl
   :members:


Functions
=========

This module defines the following functions:


.. autofunction:: ldap.controls.RequestControlTuples

.. autofunction:: ldap.controls.DecodeControlTuples


Sub-modules
===========

Various sub-modules implement specific LDAPv3 extended controls. The classes
therein are derived from the base-classes :py:class:`ldap.controls.RequestControl`,
:py:class:`ldap.controls.ResponseControl` or :py:class:`ldap.controls.LDAPControl`.

Some of them require :py:mod:`pyasn1` and :py:mod:`pyasn1_modules` to be installed.


:py:mod:`ldap.controls.simple` Very simple controls
===================================================

.. automodule:: ldap.controls.simple
   :members:


:py:mod:`ldap.controls.sessiontrack` Session tracking control
=============================================================

.. automodule:: ldap.controls.sessiontrack
   :members:


:py:mod:`ldap.controls.libldap` Various controls implemented in OpenLDAP libs
=============================================================================

.. py:module:: ldap.controls.libldap
   :synopsis: request and response controls implemented by OpenLDAP libs

This module wraps C functions in OpenLDAP client libs which implement various
request and response controls into Python classes.


.. autoclass:: ldap.controls.libldap.AssertionControl
   :members:

.. seealso::

   :rfc:`4528` - Lightweight Directory Access Protocol (LDAP) Assertion Control


.. autoclass:: ldap.controls.libldap.MatchedValuesControl
   :members:

.. seealso::

   :rfc:`3876` - Returning Matched Values with the Lightweight Directory Access Protocol version 3 (LDAPv3)


.. autoclass:: ldap.controls.libldap.SimplePagedResultsControl 
   :members:

.. seealso::

   :rfc:`2696` - LDAP Control Extension for Simple Paged Results Manipulation


:py:mod:`ldap.controls.psearch` LDAP Persistent Search
======================================================

.. py:module:: ldap.controls.psearch
   :synopsis: request and response controls for LDAP persistent
              search

This module implements request and response controls for LDAP persistent
search.

.. seealso::

   http://tools.ietf.org/html/draft-ietf-ldapext-psearch


.. autoclass:: ldap.controls.psearch.PersistentSearchControl
   :members:

.. autoclass:: ldap.controls.psearch.EntryChangeNotificationControl
   :members:

