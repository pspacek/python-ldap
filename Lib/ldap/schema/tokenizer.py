"""
ldap.schema.tokenizer
written by Michael Stroeder <michael@stroeder.com>

Low-level parsing functions for schema element strings

\$Id: tokenizer.py,v 1.2 2002/09/05 21:48:25 stroeder Exp $
"""

def split_tokens(s):
  """
  Returns list of syntax elements with quotes and spaces
  stripped.
  """
  result = []
  s_len = len(s)
  i = 0
  while i<s_len:
    start = i
    while i<s_len and s[i]!="'":
      if s[i]=="(" or s[i]==")":
        if i>start:
          result.append(s[start:i])
        result.append(s[i])
        i +=1 # Consume parentheses
        start = i
      elif s[i]==" ":
        if i>start:
          result.append(s[start:i])
        # Consume space chars
        while i<s_len and s[i]==" ":
          i +=1
        start = i
      else:
        i +=1
    if i>start:
      result.append(s[start:i])
    i +=1
    if i>=s_len:
      break
    start = i
    while i<s_len and s[i]!="'":
      i +=1
    if i>=start:
      result.append(s[start:i])
    i +=1
  return result # split_tokens()

def extract_tokens(l,known_tokens={}):
  """
  Returns dictionary of known tokens with all values
  """
  assert l[0].strip()=="(" and l[-1].strip()==")",ValueError(repr(s),l)
  result = {}
  result.update(known_tokens)
  i = 0
  l_len = len(l)
  while i<l_len:
    if result.has_key(l[i]):
      token = l[i]
      i += 1 # Consume token
      if i<l_len:
        if result.has_key(l[i]):
          # non-valued
          result[token] = []
        elif l[i]=="(":
          # multi-valued
          i += 1 # Consume left parentheses
          start = i
          while i<l_len and l[i]!=")":
            i += 1
          result[token] = l[start:i]
          i += 1 # Consume right parentheses
        else:
          # single-valued
          result[token] = [l[i]]
          i += 1 # Consume single value
    else:
      i += 1 # Consume unrecognized item
  return result

