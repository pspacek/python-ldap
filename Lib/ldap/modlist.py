"""
ldap.modlist - create add/modify modlist's
(c) by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

$Id: modlist.py,v 1.12 2002/09/18 14:04:47 stroeder Exp $

Python compability note:
This module is known to work with Python 2.0+ but should work
with Python 1.5.2 as well.
"""

__version__ = '0.1.0'


import string,ldap


def list_dict(l):
  """
  return a dictionary with all items of l being the keys of the dictionary
  """
  d = {}
  for i in l:
    d[i]=None
  return d


def addModlist(entry,ignore_attr_types=None):
  """Build modify list for call of method LDAPObject.add()"""
  ignore_attr_types = list_dict(map(string.lower,(ignore_attr_types or [])))
  modlist = []
  for attrtype in entry.keys():
    if ignore_attr_types.has_key(string.lower(attrtype)):
      # This attribute type is ignored
      continue
    # Eliminate empty attr value strings in list
    attrvaluelist = filter(None,entry[attrtype])
    if attrvaluelist:
      modlist.append((attrtype,entry[attrtype]))
  return modlist # addModlist()


def modifyModlist(
  old_entry,new_entry,ignore_attr_types=None,ignore_oldexistent=0
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
  ignore_attr_types = list_dict(map(string.lower,(ignore_attr_types or [])))
  modlist = []
  attrtype_lower_map = {}
  for a in old_entry.keys():
    attrtype_lower_map[string.lower(a)]=a
  for attrtype in new_entry.keys():
    attrtype_lower = string.lower(attrtype)
    if ignore_attr_types.has_key(attrtype_lower):
      # This attribute type is ignored
      continue
    # Filter away null-strings
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
      add_values = []
      for v in new_value:
        if not old_value_dict.has_key(v):
          add_values.append(v)
      if add_values or delete_values:
        modlist.append((ldap.MOD_DELETE,attrtype,None))
        modlist.append((ldap.MOD_ADD,attrtype,new_value))
    elif old_value and not new_value:
      # Completely delete an existing attribute
      modlist.append((ldap.MOD_DELETE,attrtype,None))
  if not ignore_oldexistent:
    # Remove all attributes of old_entry which are not present
    # in new_entry at all
    for a in attrtype_lower_map.keys():
      if ignore_attr_types.has_key(a):
        # This attribute type is ignored
        continue
      attrtype = attrtype_lower_map[a]
      modlist.append((ldap.MOD_DELETE,attrtype,None))
  return modlist # modifyModlist()
