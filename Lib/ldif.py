"""
ldif - generate and parse LDIF data (see RFC 2849)
written by Michael Stroeder <michael@stroeder.com>

$Id: ldif.py,v 1.15 2001/12/12 22:04:48 stroeder Exp $

License:
Public domain. Do anything you want with this module.

Python compability note:
This module should work with Python 1.5.2+.
"""

__version__ = '0.4.0'

__all__ = [
  # constants
  'ldif_pattern',
  # functions
  'AttrTypeandValueLDIF','CreateLDIF','ParseLDIF',
]

import os,string,urlparse,urllib,base64,re,types

try:
  from cStringIO import StringIO
except ImportError:
  from StringIO import StringIO

attrtype_pattern = r'[\w;.]+(;[\w_-]+)*'
data_pattern = r'(([^,]|\\,)+|".*?")'
rdn_pattern = attrtype_pattern + r'[ ]*=[ ]*' + data_pattern
dn_pattern   = rdn_pattern + r'([ ]*,[ ]*' + rdn_pattern + r')*[ ]*'
dn_regex   = re.compile('^%s$' % dn_pattern)

ldif_pattern = '^((dn(:|::) %(dn_pattern)s)|(%(attrtype_pattern)s(:|::) .*)$)+' % vars()

linesep = '\n'

MOD_OP_INTEGER = {
  'add':0,'delete':1,'replace':2
}

MOD_OP_STR = {
  0:'add',1:'delete',2:'replace'
}

CHANGE_TYPES = ['add','delete','modify','modrdn']
valid_changetype_dict = {}
for c in CHANGE_TYPES:
  valid_changetype_dict[c]=None


SAFE_STRING_PATTERN = '(^(\000|\n|\r| |:|<)|[\000\n\r\200-\377]+|[ ]+$)'
safe_string_re = re.compile(SAFE_STRING_PATTERN)


def is_dn(s):
  """
  returns 1 if s is a LDAP DN
  """
  rm = dn_regex.match(s)
  return rm!=None and rm.group(0)==s


def needs_base64(s):
  """
  returns 1 if s has to be base-64 encoded because of special chars
  """
  return not safe_string_re.search(s) is None


def list_dict(l):
  """
  return a dictionary with all items of l being the keys of the dictionary
  """
  d = {}
  for i in l:
    d[i]=None
  return d

def CreateAttrTypeandValueLDIF(attr_type,attr_value,base64_attrs=[],cols=76):
  """
  Write a single attribute to one or many folded LDIF line(s).
  
  attr_type
        attribute type
  attr_value
        attribute value
  base64_attrs
        list of attribute types to be base64-encoded in any case
  cols
        Specifies how many columns a line may have before it's
        folded into many lines.
  """
  # Encode with base64 if necessary
  if (attr_type in base64_attrs) or needs_base64(attr_value):
    line = '%s:: %s' % (
      attr_type,
      string.replace(base64.encodestring(attr_value),'\n','')
    )
  else:
    line = '%s: %s' % (attr_type,attr_value)
  # Check maximum line length
  line_len = len(line)
  if line_len<=cols:
    return line
  # Fold line
  pos = cols
  result = [line[0:min(line_len,cols)]]
  while pos<line_len:
    result.append(line[pos:min(line_len,pos+cols-1)])
    pos = pos+cols-1
  return string.join(result,linesep+' ')


def CreateLDIF(dn,data,base64_attrs=[],cols=76):
  """
  Create LDIF formatted entry including trailing empty line.
  
  dn
        string-representation of distinguished name
  data
        Either a dictionary holding the LDAP entry {attrtype:data}
        or a list with a modify list like for LDAPObject.modify().
  base64_attrs
        list of attribute types to be base64-encoded in any case
  cols
        Specifies how many columns a line may have before it's
        folded into many lines.
  """
  # At first prepare line with distinguished name
  result = [CreateAttrTypeandValueLDIF('dn',dn,cols=cols)]
  if type(data)==types.DictType:
    #-----------------------------------------------------
    # Assume data contains a dictionary with a LDAP entry
    #-----------------------------------------------------
    entry=data
    attr_types = entry.keys()[:]
    attr_types.sort()
    for attr_type in attr_types:
      for attr_value in entry[attr_type]:
        result.append(CreateAttrTypeandValueLDIF(attr_type,attr_value,base64_attrs,cols))
  elif type(data)==types.ListType:
    #-----------------------------------------------------
    # Assume data contains a list of modifications
    #-----------------------------------------------------
    modlist=data
    for mod_op,mod_type,mod_vals in modlist:
      result.append(
        AttrTypeandValueLDIF('changetype','modify',cols=cols)
      )
      result.append(
        AttrTypeandValueLDIF(MOD_OP_STR[mod_op],mod_type,cols=cols)
      )
      if type(mod_vals)==types.StringType:
        mod_vals = [mod_vals]
      for mod_val in mod_vals:
        result.append(
          AttrTypeandValueLDIF(
            mod_type,mod_val,base64_attrs,cols
          )
        )
  result.append('\n')
  return string.join(result,linesep)


class LDIFParser:
  """
  Base class for a LDIF parser. Applications should sub-class this
  class and override method handle() to implement something meaningful.

  Public class attributes:
  records_read
        Counter for records processed so far
  """

  def _stripLineSep(self,s):
    """
    Strip trailing line separators from s, but no other whitespaces
    """
    if not s:
      return s
    elif s[-2:]=='\r\n':
      return s[:-2]
    elif s[-1]=='\n':
      return s[:-1]
    else:
      return s

  def __init__(
    self,
    inputfile,
    ignored_attr_types=[],
    max_entries=0,
    process_url_schemes=[],
  ):
    """
    Parameters:
    inputfile
        File-object to read the LDIF input from
    ignored_attr_types
        Attributes with these attribute type names will be ignored.
    max_entries
        If non-zero specifies the maximum number of entries to be
        read from f.
    process_url_schemes
        List containing strings with URLs schemes to process with urllib.
        An empty list turns off all URL processing and the attribute
        is ignored completely.
    """
    self._inputfile = inputfile
    self._max_entries = max_entries
    self._process_url_schemes = list_dict(map(string.lower,process_url_schemes))
    self._ignored_attr_types = list_dict(map(string.lower,ignored_attr_types))
    self.records_read = 0

  def handle(self,*args,**kwargs):
    """
    Process a single content LDIF record. This method should be
    implemented by applications using LDIFParser.
    """

  def _unfoldLDIFLine(self):
    """
    Unfold several folded lines with trailing space into one line
    """
    unfolded_line = self._stripLineSep(self._line)
    self._line = self._inputfile.readline()
    while self._line and self._line[0]==' ':
      unfolded_line = unfolded_line+self._stripLineSep(self._line[1:])
      self._line = self._inputfile.readline()
    return unfolded_line

  def _parseAttrTypeandValue(self):
    """
    Parse a single attribute type and value pair from one or
    more lines of LDIF data
    """
    # Reading new attribute line
    unfolded_line = self._unfoldLDIFLine()
    # Ignore comments which can also be folded
    while unfolded_line and unfolded_line[0]=='#':
      unfolded_line = self._unfoldLDIFLine()
    if not unfolded_line or unfolded_line=='\n' or unfolded_line=='\r\n':
      return None,None
    attr_type,attr_value = string.split(unfolded_line,' ',1)
    # if needed attribute value is BASE64 decoded
    value_spec = attr_type[-2:]
    attr_type = string.strip(string.split(attr_type,':')[0])
    if value_spec=='::':
      # attribute value needs base64-decoding
      attr_value = base64.decodestring(attr_value)
    elif value_spec==':<':
      # fetch attribute value from URL
      url = attr_value; attr_value = None
      if self._process_url_schemes:
        u = urlparse.urlparse(url)
        if self._process_url_schemes.has_key(u[0]):
          attr_value = urllib.urlopen(url).read()
    return attr_type,attr_value

  def parse(self):
    """
    Continously read and parse LDIF records
    """
    self._line = self._inputfile.readline()

    while self._line and \
          (not self._max_entries or self.records_read<self._max_entries):

      # Reset record
      version = None; dn = None; changetype = None; modop = None; entry = {}

      attr_type,attr_value = self._parseAttrTypeandValue()

      while attr_type!=None and attr_value!=None:
        if attr_type=='dn':
          # attr type and value pair was DN of LDIF record
          if dn!=None:
	    raise ValueError, 'Two lines starting with dn: in one record.'
          if not is_dn(attr_value):
	    raise ValueError, 'No valid string-representation of distinguished name %s.' % (repr(attr_value))
          dn = attr_value
        elif attr_type=='version' and dn is None:
          version = 1
        elif attr_type=='changetype':
          # attr type and value pair was DN of LDIF record
          if dn is None:
	    raise ValueError, 'Read changetype: before getting valid dn: line.'
          if changetype!=None:
	    raise ValueError, 'Two lines starting with changetype: in one record.'
          if not valid_changetype_dict.has_key(attr_value):
	    raise ValueError, 'changetype value %s is invalid.' % (repr(attr_value))
          dn = attr_value
        elif attr_value!=None and \
             not self._ignored_attr_types.has_key(string.lower(attr_type)):
          # Add the attribute to the entry if not ignored attribute
          if entry.has_key(attr_type):
            entry[attr_type].append(attr_value)
          else:
            entry[attr_type]=[attr_value]

        # Read the next line within an entry
        attr_type,attr_value = self._parseAttrTypeandValue()

      if entry:
        # append entry to result list
        self.handle(dn,entry)
        self.records_read = self.records_read+1

    return # ParseLDIF()


class LDIFRecordList(LDIFParser):
  """
  Collect all records of LDIF input into a single dictionary
  with DN as string keys. It can be a memory hog!
  """

  def __init__(
    self,inputfile,ignored_attr_types=[],max_entries=0,process_url_schemes=[],
    all_records=[]
  ):
    """
    See LDIFParser.__init__()

    Additional Parameters:
    all_records
        List instance for storing parsed records
    """
    LDIFParser.__init__(self,input_file,ignored_attr_types,max_entries,process_url_schemes)
    self.all_records = all_records

  def handle(self,dn,entry):
    """
    Append single record to dictionary of all records.
    """
    # Hmm, strictly spoke a normalization of dn should be done before
    # using it as dictionary key...
    self.all_records.append((dn,entry))


class LDIFCopy(LDIFParser):
  """
  Copy LDIF input to LDIF output containing all data retrieved
  via URLs
  """

  def __init__(
    self,input_file,output_file,ignored_attr_types=[],max_entries=0,process_url_schemes=[]):
    """
    See LDIFParser.__init__()

    Additional Parameters:
    output_file
        File-object to write the LDIF output to
    """
    LDIFParser.__init__(self,input_file,ignored_attr_types,max_entries,process_url_schemes)
    self._output_file = output_file

  def handle(self,dn,entry):
    """
    Write single LDIF record to output file.
    """
    ldif_data = CreateLDIF(dn,entry)
    self._output_file.write(ldif_data)


def ParseLDIF(f,ignore_attrs=[],maxentries=0):
  """
  Compability function with old module.
  
  Use is deprecated!
  """
  ldif_parser = LDIFRecordList(
    f,ignored_attr_types=ignore_attrs,max_entries=maxentries,process_url_schemes=0
  )
  ldif_parser.parse()
  return ldif_parser.all_records


