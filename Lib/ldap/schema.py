""" schema.py - RootDSE schema information support for
python_ldap.

Written by Hans Aschauer <Hans.Aschauer@epost.de>

\$Id: schema.py,v 1.2 2002/05/04 18:25:59 stroeder Exp $

License:
Public domain. Do anything you want with this module.
"""

__version__ = '0.0.1'


import ldap, _ldap

def str2objectclass(str):
    return ldap._ldap_call(_ldap.str2objectclass,str)
def str2attributetype(str):
    return ldap._ldap_call(_ldap.str2attributetype,str)
def str2syntax(str):
    return ldap._ldap_call(_ldap.str2syntax,str)
def str2matchingrule(str):
    return ldap._ldap_call(_ldap.str2matchingrule,str)



class objectClass:
    def __init__(self, str):
        (self.oid,           #REQUIRED 
         self.names,         #OPTIONAL
         self.desc,          #OPTIONAL
         self.obsolete,      #0=no, 1=yes
         self.sup_oids,      #OPTIONAL
         self.kind,          #0=ABSTRACT
         self.oids_must,     #OPTIONAL
         self.oids_may,      #OPTIONAL
         self.ext,           #OPTIONAL
         ) = str2objectclass(str)

class attributeType:
    def __init__(self, str):
        (self.oid,             #REQUIRED				    
         self.names,           #OPTIONAL				    
         self.desc,            #OPTIONAL				    
         self.obsolete,        #0=no, 1=yes 			    
         self.sup_oid,         #OPTIONAL				    
         self.equaltity_oid,   #OPTIONAL				    
         self.ordering_oid,    #OPTIONAL				    
         self.substr_oid,      #OPTIONAL				    
         self.syntax_oid,      #OPTIONAL				    
         self.syntax_len,      #OPTIONAL				    
         self.single_value,    #0=no, 1=yes		    
         self.collectiove,     #0=no, 1=yes			    
         self.no_user_mod,     #0=no, 1=yes 			    
         self.usage,           #0=userApplications, 1=directoryOperation,
                               #2=distributedOperation, 3=dSAOperation
         self.ext              #OPTIONAL
         ) = str2attributetype(str)

class ldapSyntax:
    def __init__(self, str):
        (self.oid,    #REQUIRED
         self.names,  #OPTIONAL
         self.desc,   #OPTIONAL
         self.ext     #OPTIONAL
         ) = str2syntax(str)

class matchingRule:
    def __init__(self, str):
        (self.oid,         #REQUIRED
         self.names,       #OPTIONAL
         self.desc,        #OPTIONAL
         self.obsolete,    #OPTIONAL
         self.syntax_oid,  #REQUIRED
         self.ext          #OPTIONAL
         ) = str2matchingrule(str)

class rootDSESchema:
    oc="objectClasses"
    at="attributeTypes"
    syn="ldapSyntaxes"
    mr="matchingRules"
    
    def __init__(self, l):
        self.objectClasses = {}
        self.objectClassesByName = {}
        self.attributeTypes = {}
        self.attributeTypesByName = {}
        self.ldapSyntaxes = {}
        self.ldapSyntaxesByName = {}
        self.matchingRules = {}
        self.matchingRulesByName = {}
        type = self.oc
        result = l.search_s("cn=Subschema",
                            ldap.SCOPE_BASE,
                            "(objectClass=*)",
                            [type])
        for schema_string in result[0][1][type]:
            oc = objectClass(schema_string)
            self.objectClasses[oc.oid] = oc
            for name in oc.names:
                self.objectClassesByName[name]= oc
        
        type = self.at
        result = l.search_s("cn=Subschema",
                            ldap.SCOPE_BASE,
                            "(objectClass=*)",
                            [type])
        for schema_string in result[0][1][type]:
            at = attributeType(schema_string)
            self.attributeTypes[at.oid] = at
            for name in at.names:
                self.attributeTypesByName[name]= at
        
        type = self.syn
        result = l.search_s("cn=Subschema",
                            ldap.SCOPE_BASE,
                            "(objectClass=*)",
                            [type])
        for schema_string in result[0][1][type]:
            syn = ldapSyntax(schema_string)
            self.ldapSyntaxes[syn.oid] = syn
            for name in syn.names:
                self.ldapSyntaxesByName[name]= syn
        
        type = self.mr
        result = l.search_s("cn=Subschema",
                            ldap.SCOPE_BASE,
                            "(objectClass=*)",
                            [type])
        for schema_string in result[0][1][type]:
            mr = matchingRule(schema_string)
            self.matchingRules[mr.oid] = mr
            for name in mr.names:
                self.matchingRulesByName[name]= mr
        

if __name__ == '__main__':
    l=ldap.initialize("ldap://localhost:1389")
    l.simple_bind_s("","")

    schema = rootDSESchema(l)
    
