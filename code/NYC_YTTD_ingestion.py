import requests
from random import seed
from random import randint

def get_data():
	# Make a request.

	limit = str(randint(0,20))

	offset = str(randint(0,2000))

	emulated_data_request = "https://data.cityofnewyork.us/resource/t29m-gskq.json?$limit=" + limit# + "&$offset=" + offset

	print(emulated_data_request)
	r = requests.get(emulated_data_request)
	return r.json()