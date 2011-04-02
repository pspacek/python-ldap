# -*- coding: utf-8 -*-
"""
ldap.controls.simple - classes for some very simple LDAP controls

See http://www.python-ldap.org/ for details.

$Id: simple.py,v 1.1 2011/04/02 20:14:48 stroeder Exp $
"""

import ldap
from ldap.controls import RequestControl,LDAPControl,KNOWN_RESPONSE_CONTROLS


class ValueLessRequestControl(RequestControl):

  def __init__(self,controlType=None,criticality=False):
    self.controlType = controlType
    self.criticality = criticality

  def encodeControlValue(self):
    return None


class ManageDSAITControl(ValueLessRequestControl):

  def __init__(self,criticality=False):
    ValueLessRequestControl.__init__(self,ldap.CONTROL_MANAGEDSAIT,criticality=False)

KNOWN_RESPONSE_CONTROLS[ldap.CONTROL_MANAGEDSAIT] = ManageDSAITControl


class RelaxRulesControl(ValueLessRequestControl):

  def __init__(self,criticality=False):
    ValueLessRequestControl.__init__(self,ldap.CONTROL_RELAX,criticality=False)

KNOWN_RESPONSE_CONTROLS[ldap.CONTROL_RELAX] = RelaxRulesControl


class BooleanControl(LDAPControl):
  """
  Base class for simple request controls with booelan control value

  In this base class controlValue has to be passed as
  boolean type (True/False or 1/0).
  """
  boolean2ber = { 1:'\x01\x01\xFF', 0:'\x01\x01\x00' }
  ber2boolean = { '\x01\x01\xFF':1, '\x01\x01\x00':0 }

  def __init__(self,controlType=None,criticality=False,booleanValue=False):
    self.controlType = controlType
    self.criticality = criticality
    self.booleanValue = booleanValue

  def encodeControlValue(self):
    return self.boolean2ber[int(self.booleanValue)]

  def decodeControlValue(self,encodedControlValue):
    self.booleanValue = self.ber2boolean[encodedControlValue]
