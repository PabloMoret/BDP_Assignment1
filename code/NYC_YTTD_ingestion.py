import requests
from random import seed
from random import randint
import logging

def get_data():
	# Make a request.

	log_file = "../logs/ingestion_log.txt"
	logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

	print(" > Requesting data (it might take a while) ...")
	limit = str(randint(0,20))

	offset = str(randint(0,2000))

	emulated_data_request = "https://data.cityofnewyork.us/resource/t29m-gskq.json?$limit=" + limit + "&$offset=" + offset
	
	logging.info("Request:   ["+ emulated_data_request+"]")
	r = requests.get(emulated_data_request)
	
	print(" > Data fetched from data.cityofnewyork.us\n     ->", str(limit), "documents")

	return r.json()