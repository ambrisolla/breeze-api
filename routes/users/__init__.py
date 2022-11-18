from flask import request
from __main__ import app
from lib.users import AccessControl

@app.route('/api/v1/users', methods=['GET'])
def users():
    ac = AccessControl()
    res = ac.get_users()
    return res

@app.route('/api/v1/users/add', methods=['POST'])
def users_add():
    ac = AccessControl()
    res = ac.add()
    return res

@app.route('/api/v1/users/change', methods=['POST'])
def users_change():
    ac = AccessControl()
    res = ac.change()
    return res

@app.route('/api/v1/users/delete', methods=['POST'])
def users_del():
    ac = AccessControl()
    res = ac.delete()
    return res

