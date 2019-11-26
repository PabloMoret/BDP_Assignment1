import requests

def get_data():
	# Make a request.
	r = requests.get('https://soda.demo.socrata.com/resource/earthquakes.json?$limit=5&$offset=5')
	
	return r.json()

