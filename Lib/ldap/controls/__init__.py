# -*- coding: utf-8 -*-
"""
controls.py - support classes for LDAP controls

See http://www.python-ldap.org/ for details.

$Id: __init__.py,v 1.2 2011/04/02 20:14:48 stroeder Exp $

Description:
The ldap.controls module provides LDAPControl classes.
Each class provides support for a certain control.
"""

from ldap import __version__

__all__ = [
  # control OID to class registy
  'KNOWN_CONTROLS',
  # Classes
  'AssertionControl',
  'BooleanControl',
  'LDAPControl',
  'ManageDSAITControl',
  'MatchedValuesControl',
  'RelaxRulesControl',
  'RequestControl',
  'ResponseControl',
  'SimplePagedResultsControl',
  'ValueLessRequestControl',
  # Functions
  'RequestControlTuples',
  'DecodeControlTuples',
]

KNOWN_RESPONSE_CONTROLS = {}

import _ldap,ldap


class RequestControl:
  """
  Base class for all request controls
  """

  def __init__(self,controlType=None,criticality=False,encodedControlValue=None):
    self.controlType = controlType
    self.criticality = criticality
    self.encodedControlValue = encodedControlValue

  def encodeControlValue(self):
    return self.encodedControlValue


class ResponseControl:
  """
  Base class for all response controls
  """

  def __init__(self,controlType=None,criticality=False):
    self.controlType = controlType
    self.criticality = criticality

  def decodeControlValue(self,encodedControlValue):
    self.encodedControlValue = encodedControlValue


class LDAPControl(RequestControl,ResponseControl):

  def __init__(self,controlType=None,criticality=False,controlValue=None,encodedControlValue=None):
    self.controlType = controlType
    self.criticality = criticality
    self.controlValue = controlValue
    self.encodedControlValue = encodedControlValue


def RequestControlTuples(ldapControls):
  """
  Return list of readily encoded 3-tuples which can be directly
  passed to C module _ldap
  """
  if ldapControls is None:
    return None
  else:
    result = [
      (c.controlType,c.criticality,c.encodeControlValue())
      for c in ldapControls
    ]
    return result


def DecodeControlTuples(ldapControlTuples,knownLDAPControls):
  """
  Return list of readily decoded ResponseControl objects
  """
  knownLDAPControls = knownLDAPControls or {}
  result = []
  for controlType,criticality,encodedControlValue in ldapControlTuples or []:
    control = knownLDAPControls.get(controlType,ResponseControl)()
    control.controlType,control.criticality = controlType,criticality
    control.decodeControlValue(encodedControlValue)
    result.append(control)  
  return result

from ldap.controls.simple import *
from ldap.controls.libldap import *
