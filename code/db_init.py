import pymongo
import logging

mongodb_client = pymongo.MongoClient("mongodb://localhost:27017/")

db_list = mongodb_client.list_database_names()

NYC_yellow_taxi_trip_data_base = None

if "NYC_yellow_taxi_2018" not in db_list:
	NYC_yellow_taxi_trip_data_base = mongodb_client["NYC_yellow_taxi_2018"]
	col_init = NYC_yellow_taxi_trip_data_base["col_init"]
	
	init_log = { "LOG": {
			"id": "NYC_yellow_taxi_2018_database",
			"date": "11/21/2019"
		} 

	}

	x = col_init.insert_one(init_log)

if "NYC_yellow_taxi_2018" in db_list:
	print("NYC_yellow_taxi_2018 Initialized")