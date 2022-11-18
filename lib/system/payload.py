from flask import request
import json

class Payload:

  def get(self):
    if request.method == 'POST':
      if request.is_json:
        data = request.json
      else:
        data = request.form
    elif request.method == 'GET':
      data = request.args
    return data
  
  def token(self):
    try:
      token = request.headers.get('token')
      return token
    except Exception as err:
      return {
        'message' : str(err)
      }, 500

  