from flask import session, request, Response
from ldap3 import Server, Connection, ALL, SUBTREE, MODIFY_REPLACE
from ldap3.core.exceptions import LDAPException, LDAPBindError
from lib.system.database import MySQL
import os
import hashlib
from datetime import datetime
from lib.system.payload import Payload

class LdapAuth:
  def __init__(self):
    self.ldap_host          = os.environ['LDAP_HOST'] 
    self.ldap_bind_username = os.environ['LDAP_BIND_USERNAME']
    self.ldap_bind_dn       = os.environ['LDAP_BIND_DN'] 
    self.ldap_bind_password = os.environ['LDAP_BIND_PASSWORD'] 
    self.token = Payload().token()

  """
    Create connection
  """
  def connect_ldap_server(self):
    try:     
      server_uri = f"ldap://{self.ldap_host}:389"
      server     = Server(server_uri, get_info=ALL)
      connection = Connection(server, user=f'cn={self.ldap_bind_username},{self.ldap_bind_dn}', 
                              password=self.ldap_bind_password)
      connection.bind()  
      return connection    
    except LDAPBindError as e:
        return {
          'message' : str(e)
        }, 500
        

  '''
    User login. 
      - Arguments: username and password
  '''
  def login(self):
    try:     
      pl = Payload()
      data = pl.get()
      if 'username' not in data or 'password' not in data:
        return {
          'message' : 'Access denied!'
        }, 403
      username = data['username']
      password = data['password']
      server_uri = f"ldap://{self.ldap_host}:389"
      server = Server(server_uri, get_info=ALL)
      # if admin use cn to search, if not admin, use uid to search
      if username == 'admin':
        user_search = 'cn'
      else:
        user_search = 'uid'
      connection    = Connection(server, user=f'{user_search}={username},{self.ldap_bind_dn}', 
                              password=password)
      bind_response = connection.bind()      
      if bind_response:
        token = self.generate_token(username)
        return {
          'message' : 'Access granted!',
          'token' : token['token']
        }
      else:
        return {
          'message' : 'Access denied!'
        }, 500
    except LDAPBindError as e:
        return {
          'message' : str(e)
        }, 500
  
  def generate_token(self, uid):
    try:
      db = MySQL()
      query_user_token = db.query(f'select * from user_token where uid="{uid}"')
      token            = query_user_token['data']['result']
      
      if len(token) == 0:
        valid_token  = False
        exists_token = False
      else:
        exists_token = True
        query_user_token_parsed = db.parse_query_result(query_user_token)
        # check if token is expired    
        token_birth = query_user_token_parsed[0]['token_birth']
        now         = datetime.now()
        timedelta   = (now-token_birth)
        days        = timedelta.days
        if days == 0:
          valid_token = True
        else:
          valid_token = False    
      if not valid_token:
        hash_string  = '{}-{}'.format(datetime.now(),uid)
        set_hash     = hashlib.sha512()
        set_hash.update(hash_string.encode())
        if not exists_token:
          db.query(f'insert into user_token (uid, token, token_birth) values ("{uid}","{set_hash.hexdigest()}","{datetime.now()}")')
        else:
          db.query(f'update user_token set token = "{set_hash.hexdigest()}", token_birth="{datetime.now()}" where uid="{uid}"')
      # return token
      query_get_token = db.query(f'select token from user_token where uid="{uid}"')
      query_get_token_parsed = db.parse_query_result(query_get_token)
      db.conn.close()
      return query_get_token_parsed[0]
    except Exception as err:
      return {
        'messages' : str(err)
      }, 500

  def passport(self):
    try:
      db = MySQL()
      query = db.query(f'select * from user_token where token="{self.token}"')
      parse_query = db.parse_query_result(query)
      data = parse_query[0]
      set_now = datetime.now()
      token_birth = data['token_birth']
      timedelta = set_now - token_birth
      if timedelta.days > 0:
        return False
      else:
        return True
    except Exception as err:
      return {  
          'message' : str(err)
        }, 500

######################################3 criar outra classe para as acoes abaixo
  