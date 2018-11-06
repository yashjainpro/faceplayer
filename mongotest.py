from pymongo import MongoClient
# pprint library is used to make the output look more pretty

from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
from random import randint

# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")

#db_stat =db.capstone.find()
#pprint(serverStatusResult)

#pprint(db_stat)

client = MongoClient("mongodb://localhost:27017")

db = client.capstone

collection = db.songs

songs = db.songs


numbers=1
if numbers==1:
   	a = 0
   	for songs in songs.find( {'user_id':{"$eq" :a}}, {'title':1, '_id' :0}):
   		print(songs);
	
elif numbers == 2:
	a = 0
	b = 2
	for songs in songs.find( {'user_id':{"$eq": b, "$eq":a}}, {'title':1, '_id' :0}):
		print(songs)
else:
	a = 0
	b = 1
	c = 2
	for songs in songs.find( {'user_id':{"$eq": a, "$eq":b,"$eq":c}}, {'title':1, '_id' :0}):
		print(songs)
