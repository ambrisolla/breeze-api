import os
import json
import mysql.connector


class MySQL:

  def __init__(self):
    # set connection
    self.conn = mysql.connector.connect(
      user     = os.environ['MYSQL_USERNAME'],
      password = os.environ['MYSQL_PASSWORD'],
      host     = os.environ['MYSQL_HOSTNAME'],
      database = os.environ['MYSQL_DATABASE']
    )
    self.conn.autocommit = True

  def query(self, query):
    try:
      cursor  = self.conn.cursor()
      cursor.execute(query)
      result  = cursor.fetchall()
      columns = cursor.column_names
      cursor.close()
      return {
        'status' : 200,
        'data'   : {
          'columns' : columns,
          'result'  : result
        }
      }
    except Exception as err:
      return {
        'message' : str(err),
        'status'  : 500
      }
    
  def parse_query_result(self, data):
    try:
      output = []
      for i in data['data']['result']:
        items = {}
        for idx, j in enumerate(i):
          items[data['data']['columns'][idx]] = j
        output.append(items)
      return output
    except Exception as err:
      return {
        'message' : str(err),
        'status'  : 500
      }      