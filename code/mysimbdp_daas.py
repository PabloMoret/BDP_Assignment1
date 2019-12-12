import db_config
import logging

#def insert_one(data):
	


def insert_multiple(data):
	
	try:
		x = db_config.collection.insert_many(data)
		print(x.inserted_ids,"\n")
	except Exception as insert_e:
		print(insert_e,"\nCheck log file for detail")
		logging.error("Failed inserting")