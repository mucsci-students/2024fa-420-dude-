import MongoFunctions


collection = MongoFunctions.connect()
if collection is None:
    print("Incorrect username or password.")
    exit()
else:
    print("Welcome to the UML Editor!")



