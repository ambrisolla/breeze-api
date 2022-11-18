from ldap3 import Server, Connection, ALL, SUBTREE, MODIFY_REPLACE
from ldap3.core.exceptions import LDAPException, LDAPBindError
from lib.auth import LdapAuth
from lib.system.database import MySQL
from lib.system.payload	 import Payload

class AccessControl:
  ''' 
    List users 
  '''
  def __init__(self):
    self.token   = Payload().token()
    self.payload   = Payload().get()

  def get_users(self, **kwargs):
    try:
      ldap_auth = LdapAuth()
      ldap_conn = ldap_auth.connect_ldap_server()
      ldap_conn.search(search_base    = {ldap_auth.ldap_bind_dn},       
        search_filter = '(uid=*)',
        search_scope  = SUBTREE, 
        attributes    = "*")
      users = []
      for entry in ldap_conn.entries:
        users.append({
          'cn'          : str(getattr(entry,'cn')),
          'uid'         : str(getattr(entry,'uid')),
          'user_type'   : str(getattr(entry,'title')),
          'description' : str(getattr(entry,'description'))
        })        
      return users
    except Exception as e:
      return {
      'message' : str(e)
      }, 500
  
  '''
    Delete a user
  '''
  def delete(self):
    try:
      ldap_auth = LdapAuth()
      ldap_conn = ldap_auth.connect_ldap_server()
      db = MySQL()
      for user_to_remove in self.payload:
        ldap_conn.delete(dn=f'uid={user_to_remove},{ldap_auth.ldap_bind_dn}')
        db.query(f'delete from user_token where uid="{user_to_remove}"')
      return {
        'message' : 'User deleted!'
      }
    except Exception as e:
      return {
        'message' : str(e)
      }, 500

  '''
    Add a user
  '''
  def add(self):
    try:     
      
      if 'uid' not in self.payload or 'cn' not in self.payload or 'description' not in self.payload or 'is_admin' not in self.payload or 'user_password' not in self.payload:
        return {
          'status' : False,
          'message' : 'Missed parameters'
        }, 500
      else:
        # check if users exists
        users = [ x['uid'] for x in self.get_users() ]
        
        if self.payload['uid'] in users:
          return {
            'message' : 'User already exists!'
          }, 400
        
        ldap_auth = LdapAuth()
        ldap_conn = ldap_auth.connect_ldap_server()
        
        attrs        = {}
        attrs['sn']  = self.payload['cn']
        attrs['cn']  = self.payload['cn']
        attrs['uid'] = self.payload['uid']
        is_admin     = self.payload['is_admin'] == 'true'
        if is_admin:
          title = 'admin'
        else:
          title = 'user'
        attrs['title'] = title
        if self.payload['user_password'] != '__NOT_CHANGED__':
          attrs['userPassword'] = self.payload['user_password']  
        attrs['description'] = self.payload['description']
        uid                  = self.payload['uid']
        user_dn              = f"uid={uid},{ldap_auth.ldap_bind_dn}"
        try:
          ldap_conn.add(dn = user_dn, object_class = 'inetOrgPerson', attributes   = attrs)
          return {
            'message' : 'User created!'
          }
        except LDAPException as e:
          return {
            'message' : str(e)
          }, 500  
    except Exception as e:
      return {
        'message' : str(e)
      }, 500

  def change(self):
    try:            
      if 'uid' not in self.payload or 'cn' not in self.payload or 'description' not in self.payload or 'is_admin' not in self.payload or 'user_password' not in self.payload:
        return {
          'status' : False,
          'message' : 'Missed parameters'
        }, 500
      else:
        users = [ x['uid'] for x in self.get_users() ]
        if self.payload['uid'] not in users:
          return {
            'message' : 'User doesn\'t exists!'
          }, 400
        ldap_auth = LdapAuth()
        ldap_conn = ldap_auth.connect_ldap_server()
        attrs        = {}
        attrs['sn']  = self.payload['cn']
        attrs['cn']  = self.payload['cn']
        attrs['uid'] = self.payload['uid']
        is_admin     = self.payload['is_admin'] == 'true'
        if is_admin:
          title = 'admin'
        else:
          title = 'user'
        attrs['title'] = title
        if self.payload['user_password'] != '__NOT_CHANGED__':
          attrs['userPassword'] = self.payload['user_password']
        attrs['description'] = self.payload['description']
        uid                  = self.payload['uid']
        user_dn              = f"uid={uid},{ldap_auth.ldap_bind_dn}"
        try:
          if self.payload['user_password'] == '__NOT_CHANGED__':
            response = ldap_conn.modify(user_dn,{
                'description' : [(MODIFY_REPLACE,[self.payload['description']])],
                'cn'          : [(MODIFY_REPLACE,[self.payload['cn']])],                  
                'title'       : [(MODIFY_REPLACE,[title])] })
          else:
            response = ldap_conn.modify(user_dn,{
                'description'  : [(MODIFY_REPLACE,[self.payload['description']])],
                'cn'           : [(MODIFY_REPLACE,[self.payload['cn']])],        
                'userPassword' : [(MODIFY_REPLACE,[self.payload['user_password']])],
                'title'        : [(MODIFY_REPLACE,[title])]})              
          return {
            'status' : True,
            'message' : 'User has been changed!'
          }
        except LDAPException as e:
          return {
            'message' : str(e)
          }, 500  
    except Exception as e:
      return {
        'message' : str(e)
      }, 500

  '''
    self.get_user_info_by_token(token='<token>')
  '''
  def get_user_info_by_token(self):
    try:
      db = MySQL()
      query_get_uid = db.query(f'select uid from user_token where token="{self.token}"')
      parse_query_get_uid = db.parse_query_result(query_get_uid)
      uid = parse_query_get_uid[0]['uid']
      user = [ x for x  in self.get_users() if x['uid'] == uid ]
      return user
    except Exception as e:
      return {
        'message' : str(e)
      }, 500