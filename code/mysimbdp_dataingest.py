from ast import literal_eval

from NYC_YTTD_ingestion import get_data
#from mysimbdp_daas import insert_one
from mysimbdp_daas import insert_multiple
import db_config

def ingestion():
		
	data = get_data()
	print(type(data))
	"""
	trips = db["trips"]

	insert_one()
	"""

def ingestion(file):

	f = open(file, "r")
	data = literal_eval(f.read())
	f.close()


	insert_multiple(data)