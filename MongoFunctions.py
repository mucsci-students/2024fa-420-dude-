import pymongo
import string

USERNAMES = [""]
PASSWORDS = [""]
DATABASES = [""]



# Functions for connecting to the MongoDB database

# Function to authorize the user
# If the username and password are not in the list of authorized users, the program will exit
def authorize_user(username, password):
    if username in USERNAMES and password in PASSWORDS:
        return 
    else:
        print("Invalid username or password")
        exit()

# Function to validate the database
# If the database is not in the list of authorized databases, the program will exit
def validate_database(database):
    if database in DATABASES:
        return
    else:
        print("Invalid database")
        exit()

# Connect to the MongoDB database
def connect(username, password, database):
    uri: string = "mongodb+srv://" + username + ":" + password + "@atlascluster.n5ktxxk.mongodb.net/"
    client = pymongo.MongoClient(uri)
    db = client.get_database(database)
    print("User: " + username + " connected to database: " + db.name)
    return db

print("You are using Mongo Version: " + pymongo.version)

print("Username: ")
username = input()
print("Password: ")
password = input()
authorize_user(username, password)

print("Database: ")
database = input()
validate_database(database)

db = connect(username, password, database)

# Get data from database
print("Getting data from database")
collection = db.get_collection("UML_Databases")
data = collection.find_one()
print(data)



