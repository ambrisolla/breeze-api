from lib.system.database import MySQL
from lib.users           import AccessControl
from flask import        request
from lib.system.payload	 import Payload


class Budget:
	def __init__(self):
		self.payload = Payload().get()
		self.token   = Payload().token()

	def add(self):
		#return self.payload
		try:
			args           = self.payload
			token          = self.token
			ac             = AccessControl()
			user_info 		 = ac.get_user_info_by_token()
			uid       		 = user_info[0]['uid']
			_type		  		 = args['type']
			category  		 = args['category']
			amount    		 = args['amount']
			description    = args['description']
			datetime			 = args['datetime']
			
			db = MySQL()
			query_res = db.query(f'insert into budget (uid, _type, category, amount, description, datetime) \
															values ("{uid}","{_type}",{category},{amount},"{description}", "{datetime}")')
			if query_res['status'] == 200:
				return {
					'message' : 'Value successfully addedd!'
				}, 200
			else:
				return {
					'message' : 'Error to add value!'
				}, 500
		except Exception as err:
			return {
				'message' : str(err)
			}, 500
	
	def get(self):
		try:
			args										 = self.payload
			token      				 			 = self.token
			ac         				 			 = AccessControl()
			user_info  				 			 = ac.get_user_info_by_token()
			uid        				 			 = user_info[0]['uid']
			db 				 				 			 = MySQL()
			# custom queries
			query_datetime_range = ''   # default date range
			limit								 = 1000 # default itens per page
			page 							   = 0    # default page number
			if 'from' in args and 'to' in args:
				_from = args['from']
				_to = args['to']
				query_datetime_range = f'and datetime >= "{_from}" and datetime <= "{_to}"'
			# limit
			if 'limit' in args:
				limit = int(args['limit'])
			# page
			if 'page' in args:
				page = args['page']
				if page < 0:
					return {
						'message' : 'Out of range!'
					}, 400	
				else:
					limit_start = page * limit
					limit = f'{limit_start},{limit}'

			# query
			query_count 		 = db.query(f'select count(*) from budget where uid="{uid}" {query_datetime_range}')			
			query_get 			 = db.query(f'select * from budget where uid="{uid}" order by datetime desc {query_datetime_range} limit {limit}')
			parse_query_get  = db.parse_query_result(query_get)
			total_items = query_count['data']['result'][0][0]
			
			if len(parse_query_get) > 0:
				pages = total_items / len(parse_query_get)
			else: 
				return {
					'data' : []
				}
			
			# this is necessary to transform amount column type to float
			parsed = []
			for item in parse_query_get:
				new_item = item
				new_item['amount'] = float(item['amount'])
				parsed.append(new_item)

			return {
				'total_items' : total_items,
				'pages' : int(abs(pages)),
				'data'  : parsed,
				'page'  : page
			}
		except Exception as err:
			return {
				'message' : str(err)
			}, 500

	class Category():
		
		def __init__(self):
			self.payload = Payload().get()

		def get(self):
			try:	
				token      = Budget().token
				ac         = AccessControl()				
				user_info = ac.get_user_info_by_token()
				uid       = user_info[0]['uid']
				db = MySQL()
				query_get_category = db.query(f'select _type,color,name,id from budget_category where uid="{uid}"')
				parse_query_get_category = db.parse_query_result(query_get_category)
				return parse_query_get_category
			except Exception as err:
				return {
					'message' : str(err)
				}, 500
		
		def add(self):
			try:
				args			 = self.payload
				name       = args['name']
				type       = args['type']
				color      = args['color']
				ac = AccessControl()
				user_info = ac.get_user_info_by_token()
				uid       = user_info[0]['uid']
				##
				categories = [ x['name'] for x in self.get() ]
				if name in categories:
					return {
						'message' : 'Category already exists!'
					}, 400
				db = MySQL()	
				a = db.query(f'insert into budget_category (name, _type, uid, color) values ("{name}","{type}","{uid}","{color}")')
				db.conn.close()
				return {
					'message' : 'Category addedd successfully!'
				}
			except Exception as err:
				return {
					'message' : str(err)
				}, 500
			
		def delete(self):
			try:
				ac         = AccessControl()				
				user_info = ac.get_user_info_by_token()
				uid       = user_info[0]['uid']
				category_id = self.payload[0]
				db = MySQL()
				# check if exists budgets with this category
				get_budget = db.query(f'select count(*) as count from budget where category={category_id}')
				parsed_get_budget = db.parse_query_result(get_budget)
				if parsed_get_budget[0]['count'] == 0:
					res = db.query(f'delete from budget_category where uid="{uid}" and id={category_id}')
					if 'data' not in res:
						return {
							'message' : str(res[0])
						}
					else:
						return {
							'message' : 'Category removed successfully!'
						}
				elif parsed_get_budget[0]['count'] > 0:
					return {
						'message' : 'This category is associated with one or more income!'
					}, 400

			except Exception as err:
				return {
					'message' : str(err)
				}, 500
			

	
