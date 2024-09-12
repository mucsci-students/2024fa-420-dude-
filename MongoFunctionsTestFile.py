import MongoFunctions





# Test connecting to the database
collection = MongoFunctions.connect()
if collection is None:
    print("Incorrect username or password.")
    exit()
else:
    print("Welcome to the UML Editor!")





# Project functions tests
# Test adding a Project to the database
project_object = {
    "object type": "project",
    "name": "Test Project",
}
MongoFunctions.create_project(collection, project_object)

# Test getting a Project from the database
project_object = MongoFunctions.get_project(collection, "Test Project")
print(project_object)





# Class functions tests
# Test adding a Class to the database
class_object = {
    "object type": "class",
    "project": "Test Project",
    "name": "TestClass",
    "attributes": [{ "object type": "attribute", "name": "testAttribute1", "type": "int", "value": 0 }],
}
MongoFunctions.create_class(collection, class_object)

# Test getting a class from the database
class_object = MongoFunctions.get_class(collection, "Test Project", "TestClass")
print(class_object)

# Test renaming a class in the database
MongoFunctions.rename_class(collection, "Test Project", "TestClass", "NewTestClass")
class_object2 = MongoFunctions.get_class(collection, "Test Project", "NewTestClass")
print(class_object2)
 


    



