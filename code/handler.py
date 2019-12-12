import pymongo
import logging
import argparse

import db_config

from mysimbdp_dataingest import ingestion

parser = argparse.ArgumentParser(description="MongoDB Platform")
group = parser.add_mutually_exclusive_group()

group.add_argument("-r", "--request", help="Intestion method: server request", action='store_true')
group.add_argument("-l", "--local", help="Intestion method: local file", type=str)

args = parser.parse_args()

db_config.db_init()

if args.local:

	file = str(args.local)
	print(file)	
	ingestion(file)

elif args.request:
	print(args.request)



#logging.basicConfig(filename="../logs/mongodb_debug.log", level=logging.DEBUG)