from lib.system.environments import ConfigEnvs
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

import routes.auth
import routes.users
import routes.budget

@app.route('/')
def hello():
  return {
    'message' : 'Hello =)!'
  }

if __name__ == '__main__':
  ConfigEnvs() # load environments
  app.run(host='0.0.0.0', port=5000, debug=True)
