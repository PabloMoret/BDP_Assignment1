import pymongo
import logging
from pymongo import MongoClient

def db_init (args):

	log_file = "../logs/ingestion_log.txt"
	logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")


	localhost = 27017
	global data_base
	global collection

	mongodb_client = MongoClient()

	#try:
		
	if args.database == "atlass":
		print(" > MongoDB Atlass DataBase ")
		mongodb_client = pymongo.MongoClient("mongodb://nyctaxi:nyctaxibdp@nyccluster-shard-00-00-843gz.gcp.mongodb.net:27017,nyccluster-shard-00-01-843gz.gcp.mongodb.net:27017,nyccluster-shard-00-02-843gz.gcp.mongodb.net:27017/test?ssl=true&replicaSet=NYCCluster-shard-0&authSource=admin&retryWrites=true&w=majority")
		logging.info("DB on Atlass. MongoDB Cluster\n\t\t\tUser: nyctaxi")
	elif args.database == "local":
		print(" > MongoDB Local Database \n   Local Host: ", str(localhost))
		mongodb_client = pymongo.MongoClient("mongodb://localhost:27017/")
		logging.info("DB on localhost. MongoDB Cluster\n\t\t\tLocal Host: {}".format(localhost))
	else:
		raise Exception("-d arguments must be   atlass   or   local")
	
	#db = mongodb_client.test

	db_list = mongodb_client.list_database_names()

	if "NYC_yellow_taxi_2018" not in db_list:

		NYC_yellow_taxi_trip_data_base = mongodb_client["NYC_yellow_taxi_2018"]
		trips = NYC_yellow_taxi_trip_data_base["trips"]
		
		init_log = { "LOG": { "id": "NYC_yellow_taxi_2018_database", "date": "11/21/2019" } }

		x = trips.insert_one(init_log)
		
		data_base = NYC_yellow_taxi_trip_data_base
		collection = trips

		logging.info(" Database initialized\n\t\t\tName: NYC_yellow_taxi_2018\n\t\t\tCollection: trips\n\t\t\t")

	elif "NYC_yellow_taxi_2018" in db_list:
		NYC_yellow_taxi_trip_data_base = mongodb_client["NYC_yellow_taxi_2018"]

		data_base = NYC_yellow_taxi_trip_data_base
		collection = NYC_yellow_taxi_trip_data_base["trips"]

		logging.info("NYC DataBase already initialized")
	"""
	except Exception as mdb_e:
		
		print(mdb_e,"\n\nCheck log file for detail")
		logging.error("Failed fetching the data base information\n\tLocalhost:",localhost,"\n\tDB Name: NYC_yellow_taxi_2018\n\tBD Collection: trips")
	"""