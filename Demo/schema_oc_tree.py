"""
Outputs the object class tree read from LDAPv3 schema
of a given server

Usage: schema_oc_tree.py [--html] [LDAP URL]
"""

import sys,getopt,ldap,ldap.schema,ldapurl

schema_allow = ldap.schema.ALLOW_ALL
schema_ignore_errors = 1

ldap_url = ldapurl.LDAPUrl(sys.argv[-1])

ldap.set_option(ldap.OPT_DEBUG_LEVEL,0)

ldap._trace_level = 0

# Connect and bind as LDAPv3
l=ldap.initialize(ldap_url.initializeUrl(),trace_level=0)
l.protocol_version = ldap.VERSION3
l.simple_bind_s('','')

# Search for DN of sub schema sub entry
subschemasubentry_dn = l.search_subschemasubentry_s(ldap_url.dn.encode('utf-8'))

if subschemasubentry_dn is None:
  print 'No sub schema sub entry found!'
  sys.exit(1)

# Read the sub schema sub entry
subschemasubentry_entry = l.read_subschemasubentry_s(
  subschemasubentry_dn,attrs=['objectClasses']
)

# Parse the schema entry
schema = ldap.schema.SubSchema(
  subschemasubentry_entry,
  schema_allow=schema_allow,
  ignore_errors=schema_ignore_errors
)

try:
  options,args=getopt.getopt(sys.argv[1:],'',['html'])
except getopt.error,e:
  print 'Error: %s\nUsage: schema_oc_tree.py [--html] [LDAP URL]'

html_output = options and options[0][0]=='--html'

objectclass_tree = schema.objectclass_tree(ignore_errors=schema_ignore_errors)

if html_output:

  # HTML output for browser

  def HTMLObjectclassTree(schema,oc_tree,oc_name,level):
    oc_obj = schema.get_schema_element(oc_name)
    assert oc_obj!=None
    print """
    <dt><strong>%s</strong></dt>
    <dd>
      OID: %s<br>
      Description: &quot;%s&quot;
    """ % (oc_name,oc_obj.oid,oc_obj.desc)
    if oc_tree[oc_name]:
      print '<dl>'
      for sub_oc_name in oc_tree[oc_name]:
        HTMLObjectclassTree(schema,oc_tree,sub_oc_name,level+1)
      print '</dl>'
    print '</dd>'

  print """<html>
<head>
  <title>Object class tree</title>
</head>
<body bgcolor="#ffffff">
<h1>Object class tree</h1>
<dl>
"""
  
  HTMLObjectclassTree(schema,objectclass_tree,'top',0)

  print """</dl>
</body>
</html>
"""

else:

  # ASCII text output for console
  def PrintObjectclassTree(schema,oc_tree,oc_name,level):
    oc_obj = schema.get_schema_element(oc_name)
    assert oc_obj!=None
    print '|    '*(level-1)+'+---'*(level>0), \
          oc_name, \
          '(%s)' % oc_obj.oid
    for sub_oc_name in oc_tree[oc_name]:
      print '|    '*(level+1)
      PrintObjectclassTree(schema,oc_tree,sub_oc_name,level+1)
  print '*** Object class tree ***'
  print
  PrintObjectclassTree(schema,objectclass_tree,'top',0)
