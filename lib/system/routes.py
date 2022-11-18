from __main__ import app

class Routes:

	def list(self):
		try:
			rules = app.url_map.iter_rules()
			routes = []
			for rule in rules:
				if str(rule) not in routes:
					routes.append(str(rule))
			return {'r':routes}
		except Exception as err:
			return {
				'message' : str(err)
			}, 500
