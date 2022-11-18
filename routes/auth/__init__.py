from __main__ import app
from flask import request, Response
from lib.system.routes import Routes
from lib.auth import LdapAuth

"""
    This functions will verify the request authentication
"""
@app.before_request
def authentication():
	r = Routes()
	routes_allowed = ['/api/v1/auth/login']
	if request.path in routes_allowed:
		pass
	else:
		auth = LdapAuth()
		passport = auth.passport()
		if passport != True:
			return {
				'message' : 'Access denied!'
			}, 403
		else:
			pass
"""
    Authentication functions
"""
@app.route('/api/v1/auth/login', methods=['POST'])
def auth_login():
	try:
		auth = LdapAuth()
		login = auth.login()
		return login
	except Exception as err:
		return {
				'message' : str(err)
		}, 500