import pymongo
import string

# Functions for connecting to the MongoDB database

# Function to connect the user to their designated collection
def connect():
    # Get the username and password from the user
    username = input("Username: ")
    password = input("Password: ")

    # Attempt to get their respective collection from the database
    uri = "mongodb+srv://derrickboyer3:bigbangtheorY@atlascluster.n5ktxxk.mongodb.net/"
    client = pymongo.MongoClient(uri)
    db = client.get_database("UML_Collections")
    collection = db.get_collection(username)
    data = collection.find_one({ "username": username }, { "password": password })

    # If the user does not exist, return None, otherwise return the collection
    if data is None:
        return None
    else:
        return collection
        
# Function to create a new user collection
def create_collection():
    # Get the new username and password from the user
    username = input("Username: ")
    password = input("Password: ")

    # Connect to the database and get the user's collection if it already exists
    # If it does, return None, otherwise create the collection and return it
    uri = "mongodb+srv://derrickboyer3:bigbangtheorY@atlascluster.n5ktxxk.mongodb.net/"
    client = pymongo.MongoClient(uri)
    db = client.get_database("UML_Collections")
    collection = db.get_collection(username)
    data = collection.find_one({ "username": username, "password": password })
    if data is not None:
        print("Username already exists.")
        return None
    db.create_collection(username)
    collection = db.get_collection(username)
    collection.insert_one({ "username": username, "password": password })
    return collection

        




# Project Functions
# Function to create a new project object
def create_project(collection, project_data):
    collection.insert_one(project_data) # inserts the project data into the collection

# Function to get a project object
def get_project(collection, project_name):
    data = collection.find_one({ "object type": "project", "name": project_name }) # finds the project in the collection and returns it
    return data

# Function to delete a project object
def delete_project(collection, project_name):
    collection.delete_one({ "object type": "project", "name": project_name }) # deletes the project from the collection





# Class Functions
# Function to create a new class object
def create_class(collection, class_data):
    collection.insert_one(class_data) # inserts the class data into the collection

# Function to get a class object
def get_class(collection, project_name, class_name):
    data = collection.find_one({ "object type": "class", "project": project_name, "name": class_name }) # finds the class in the collection and returns it
    return data

#Function to rename a class object
def rename_class(collection, project_name, class_name, new_name):
    collection.update_one({ "object type": "class", "project": project_name, "name": class_name }, { "$set": { "name": new_name } }) # updates the class name in the collection

# Function to delete a class object
def delete_class(collection, project_name, class_name):
    collection.delete_one({ "object type": "class", "project": project_name, "name": class_name }) # deletes the class from the collection

# Function to list all classes in a project
def list_classes(collection, project_name):
    data = collection.find({ "object type": "class", "project": project_name }) # finds all classes in the collection for the project and returns them
    return data





# Relationship Functions
# Function to create a new relationship object
def create_relationship(collection, relationship_data):
    collection.insert_one(relationship_data) # inserts the relationship data into the collection

# Function to get a relationship object
def get_relationship(collection, project_name, relationship_type, class1_name, class2_name):
    data = collection.find_one({ "object type": "relationship", "project": project_name, "relationship type": relationship_type, "class1": class1_name, "class2": class2_name }) # finds the relationship in the collection and returns it
    return data

# Function to delete a relationship object
def delete_relationship(collection, project_name, relationship_type, class1_name, class2_name):
    collection.delete_one({ "object type": "relationship", "project": project_name, "relationship type": relationship_type, "class1": class1_name, "class2": class2_name }) # deletes the relationship from the collection

# Function to list all relationships in a project
def list_relationships(collection, project_name):
    data = collection.find({ "object type": "relationship", "project": project_name }) # finds all relationships in the collection for the project and returns them
    return data






# Attribute Functions
# Function to create a new attribute object
def create_attribute(collection, project_name, class_name, attribute_data):
    collection.find_one_and_update({ "object type": "class", "project": project_name, "name": class_name }, { "$push": { "attributes": attribute_data } }) # inserts the attribute data into the class in the collection

# Function to get an attribute object
def get_attribute(collection, project_name, class_name, attribute_name):
    data = collection.find_one({ "object type": "class", "project": project_name, "name": class_name, "attributes.name": attribute_name }, { "attributes.$": 1 }) # finds the attribute in the collection and returns it
    return data

# Function to rename an attribute object
def rename_attribute(collection, project_name, class_name, attribute_name, new_name):
    collection.find_one_and_update({ "object type": "class", "project": project_name, "name": class_name, "attributes.name": attribute_name }, { "$set": { "attributes.$.name": new_name } }) # updates the attribute name in the class in the collection

# Function to delete an attribute object
def delete_attribute(collection, project_name, class_name, attribute_name):
    collection.find_one_and_update({ "object type": "class", "project": project_name, "name": class_name }, { "$pull": { "attributes": { "name": attribute_name } } }) # deletes the attribute from the class in the collection



    






