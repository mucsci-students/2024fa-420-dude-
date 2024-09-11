import pymongo
import string

# Functions for connecting to the MongoDB database

# Function to connect the user to their designated collection
def connect():
    print("Username: ")
    username = input()
    print("Password: ")
    password = input()
    uri = "mongodb+srv://derrickboyer3:bigbangtheorY@atlascluster.n5ktxxk.mongodb.net/"
    client = pymongo.MongoClient(uri)
    db = client.get_database("UML_Collections")
    collection = db.get_collection(username)
    data = collection.find({ "username": username }, { "password": password })
    for item in data:
        if item is None:
            return None
        else:
            return collection
        
# Function to create a new class object
def create_class(collection, class_data):
    collection.insert_one(class_data)

# Function to create a new relationship object
def create_relationship(collection, relationship_data):
    collection.insert_one(relationship_data)

# Function to create a new attribute object
def create_attribute(collection, attribute_data):
    collection.insert_one(attribute_data)

    






