import db_config
import logging

def insert_multiple(data):
	
	log_file = "../logs/ingestion_log.txt"
	logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

	try:
		x = db_config.collection.insert_many(data)
		#logging.info("Inserted: {}".format(str(x.inserted_ids)))
		#print(" > Document inserted")
	except Exception as insert_e:
		print(insert_e,"\nCheck log file for detail")
		logging.error("Failed inserting")