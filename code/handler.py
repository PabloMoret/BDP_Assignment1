import pymongo
import logging
import argparse
import threading
import time

import db_config

from mysimbdp_dataingest import ingestion
from mysimbdp_dataingest import ingestion_requested

global timer0
global timer1

def ingest(args):

	if args.local:

		file = str(args.local)
		ingestion(file)

	elif args.request:
		ingestion_requested()


def parallelize(n, args):
	thread_list = []
	for x in range(0, n):
		thread = threading.Thread(target=ingest, args=[args])
		thread_list.append(thread)

	for thread in thread_list:
		thread.start()

	for thread in thread_list:
		thread.join()




log_file_control = "../logs/ingestion_log.txt"
logging.basicConfig(filename=log_file_control, level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

parser = argparse.ArgumentParser(description="MongoDB Platform")
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("-r", "--request", help="Ingestion method: server request", action='store_true')
group.add_argument("-l", "--local", help="Ingestion method: local file", type=str)

parser.add_argument("-p", "--parallel", help="Parallelize n instances of ingestion", type=int)
parser.add_argument("-t", "--timer", help="Set a timer", action='store_true')
parser.add_argument("-d", "--database", help="Use the atlass database or your own local database", required=True, type=str)

args = parser.parse_args()

print(" > Initialiting BD ... ")
db_config.db_init(args)

n = args.parallel

if args.timer:
	timer0 = time.time()

if args.parallel:
	if n < 2 or n > 128:
		print("  *! No correct input threads number (2-128)")
		logging.error("Concurrent function call failed\n\t\t\tNumber of threads: {}".format(n))
	else:
		logging.info("Parallelized ingestions: {}".format(args.parallel))
		print(" > Running", args.parallel, "parallelized instances of ingestion")
		parallelize(args.parallel, args)

else:
	ingest(args)

if args.timer:
	timer1 = time.time()
	print(" > Ingestion time of",args.parallel,"concurrent sources in",timer1-timer0)
	logging.info("Timer: {}".format(str(timer1-timer0)))

#print(" *! Check the log files for more details")