"""
ldap.modlist - create add/modify modlist's
(c) by Michael Stroeder <michael@stroeder.com>

$Id: modlist.py,v 1.6 2002/02/18 16:42:50 stroeder Exp $

Python compability note:
This module is known to work with Python 2.0+ but should work
with Python 1.5.2 as well.
"""


__version__ = '0.0.6'


import string,ldap


def addModlist(entry,ignore_attr_types=[]):
  """Build modify list for call of method LDAPObject.add()"""
  ignore_attr_types = map(string.lower,ignore_attr_types)
  modlist = []
  for attrtype in entry.keys():
    if string.lower(attrtype) in ignore_attr_types:
      # This attribute type is ignored
      continue
    # Eliminate empty attr value strings in list
    attrvaluelist = filter(None,entry[attrtype])
    if attrvaluelist:
      modlist.append((attrtype,entry[attrtype]))
  return modlist


def modifyModlist(
  old_entry,new_entry,ignore_attr_types=[],ignore_oldexistent=0
):
  """
  Build differential modify list for calling LDAPObject.modify()/modify_s()

  old_entry
      Dictionary holding the old entry
  new_entry
      Dictionary holding what the new entry should be
  ignore_attr_types
      List of attribute type names to be ignored completely
  ignore_oldexistent
      If non-zero attribute type names which are in old_entry
      but are not found in new_entry at all are not deleted.
      This is handy for situations where your application
      sets attribute value to '' for deleting an attribute.
      In most cases leave zero.
  """
  ignore_attr_types = map(string.lower,ignore_attr_types)
  modlist = []
  attrtype_lower_map = {}
  for a in old_entry.keys():
    attrtype_lower_map[string.lower(a)]=a
  for attrtype in new_entry.keys():
    attrtype_lower = string.lower(attrtype)
    if attrtype_lower in ignore_attr_types:
      # This attribute type is ignored
      continue
    new_value = filter(None,new_entry[attrtype])
    if attrtype_lower_map.has_key(attrtype_lower):
      old_value = old_entry.get(attrtype_lower_map[attrtype_lower],[])
      del attrtype_lower_map[attrtype_lower]
    else:
      old_value = []

    if not old_value and new_value:
      # Add a new attribute to entry
      modlist.append((ldap.MOD_ADD,attrtype,new_value))

    elif old_value and new_value:
      # Replace existing attribute
      old_value_dict={}
      for v in old_value: old_value_dict[v]=None
      new_value_dict={}
      for v in new_value: new_value_dict[v]=None
      delete_values = []
      for v in old_value:
        if not new_value_dict.has_key(v):
          delete_values.append(v)
      if delete_values:
        modlist.append((ldap.MOD_DELETE,attrtype,delete_values))
      add_values = []
      for v in new_value:
        if not old_value_dict.has_key(v):
          add_values.append(v)
      if add_values:
        modlist.append((ldap.MOD_ADD,attrtype,add_values))

    elif old_value and not new_value:
      # Completely delete an existing attribute
      modlist.append((ldap.MOD_DELETE,attrtype,None))

  if not ignore_oldexistent:
    # Remove all attributes of old_entry which are not present
    # in new_entry at all
    for a in attrtype_lower_map.keys():
      if a in ignore_attr_types:
        # This attribute type is ignored
        continue
      attrtype = attrtype_lower_map[a]
      modlist.append((ldap.MOD_DELETE,attrtype,None))
  return modlist

def test():
  """Test functions"""
  
  print '\nTesting function addModlist():'
  addModlist_tests = [
    (
      {
        'objectClass':['person','pilotPerson'],
        'cn':['Michael Str\303\266der','Michael Stroeder'],
        'sn':['Str\303\266der'],
      },
      [
        ('objectClass',['person','pilotPerson']),
        ('cn',['Michael Str\303\266der','Michael Stroeder']),
        ('sn',['Str\303\266der']),
      ]
    ),
  ]
  for entry,test_modlist in addModlist_tests:
    test_modlist.sort()
    result_modlist = addModlist(entry)
    result_modlist.sort()
    if test_modlist!=result_modlist:
      print 'addModlist(%s) returns\n%s\ninstead of\n%s.' % (
        repr(entry),repr(result_modlist),repr(test_modlist)
      )

  print '\nTesting function modifyModlist():'
  modifyModlist_tests = [
    (
      {
        'objectClass':['person','pilotPerson'],
        'cn':['Michael Str\303\266der','Michael Stroeder'],
        'sn':['Str\303\266der'],
        'c':['DE'],
      },
      {
        'objectClass':['person','inetOrgPerson'],
        'cn':['Michael Str\303\266der','Michael Stroeder'],
        'sn':[],
        'mail':['michael@stroeder.com'],
      },
      [
        (ldap.MOD_DELETE,'objectClass',['pilotPerson']),
        (ldap.MOD_ADD,'objectClass',['inetOrgPerson']),
        (ldap.MOD_DELETE,'c',None),
        (ldap.MOD_DELETE,'sn',None),
        (ldap.MOD_ADD,'mail',['michael@stroeder.com']),
      ]
    ),
  ]
  for old_entry,new_entry,test_modlist in modifyModlist_tests:
    test_modlist.sort()
    result_modlist = modifyModlist(old_entry,new_entry)
    result_modlist.sort()
    if test_modlist!=result_modlist:
      print 'modifyModlist(%s,%s) returns\n%s\ninstead of\n%s.' % (
        repr(old_entry),
        repr(new_entry),
        repr(result_modlist),
        repr(test_modlist)
      )

if __name__ == '__main__':
  test()
