from ast import literal_eval

from NYC_YTTD_ingestion import get_data
#from mysimbdp_daas import insert_one
from mysimbdp_daas import insert_multiple
import db_config

def ingestion_requested():
	
	data = get_data()
	print(" > Ingesting ... ")
	insert_multiple(data)

def ingestion(file):

	#print(" > Fetching file ... ")	
	f = open(file, "r")
	data = literal_eval(f.read())
	f.close()

	#print(" > Ingesting ... ")
	insert_multiple(data)