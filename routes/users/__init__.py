from flask import request
from __main__ import app
from lib.users import AccessControl
from lib.auth import LdapAuth


@app.route('/api/v1/users', methods=['GET'])
def users():
    auth = LdapAuth()
    login_info = auth.login_info()
    is_admin = login_info['is_admin'] == True
    if is_admin != True:
        return {
            'message': 'access denied'
        }, 500

    ac = AccessControl()
    res = ac.get_users()
    return res


@app.route('/api/v1/users/add', methods=['POST'])
def users_add():
    auth = LdapAuth()
    login_info = auth.login_info()
    is_admin = login_info['is_admin'] == True
    if is_admin != True:
        return {
            'message': 'access denied'
        }, 500
    ac = AccessControl()
    res = ac.add()
    return res


@app.route('/api/v1/users/change', methods=['POST'])
def users_change():
    auth = LdapAuth()
    login_info = auth.login_info()
    is_admin = login_info['is_admin'] == True
    if is_admin != True:
        return {
            'message': 'access denied'
        }, 500
    ac = AccessControl()
    res = ac.change()
    return res


@app.route('/api/v1/users/delete', methods=['POST'])
def users_del():
    auth = LdapAuth()
    login_info = auth.login_info()
    is_admin = login_info['is_admin'] == True
    if is_admin != True:
        return {
            'message': 'access denied'
        }, 500
    ac = AccessControl()
    res = ac.delete()
    return res
