import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")

mydb = myclient["mydatabase"]

if "mydatabase" in mydb:
	print("The database exists")