import pymongo
import logging

def db_init ():

	log_file = "../logs/ingestion_log.txt"
	logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")


	localhost = 27017
	global data_base
	global collection


	try:
		mongodb_client = pymongo.MongoClient("mongodb://localhost:27017/")
		db_list = mongodb_client.list_database_names()

		if "NYC_yellow_taxi_2018" not in db_list:

			NYC_yellow_taxi_trip_data_base = mongodb_client["NYC_yellow_taxi_2018"]
			trips = NYC_yellow_taxi_trip_data_base["trips"]
			
			init_log = { "LOG": { "id": "NYC_yellow_taxi_2018_database", "date": "11/21/2019" } }

			x = trips.insert_one(init_log)
			
			data_base = NYC_yellow_taxi_trip_data_base
			collection = trips

			logging.info("NYC DataBase correctly initialized")

		elif "NYC_yellow_taxi_2018" in db_list:
			NYC_yellow_taxi_trip_data_base = mongodb_client["NYC_yellow_taxi_2018"]

			data_base = NYC_yellow_taxi_trip_data_base
			collection = NYC_yellow_taxi_trip_data_base["trips"]

			#logging.info("NYC DataBase already initialized")

	except Exception as mdb_e:
		
		print(mdb_e,"\n\nCheck log file for detail")
		logging.error("Failed fetching the data base information\n\tLocalhost:",localhost,"\n\tDB Name: NYC_yellow_taxi_2018\n\tBD Collection: trips")


