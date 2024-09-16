import MongoFunctions



# Tests for getting or creating new collecions
# Comment out which way you want to test

# Test connecting to the database
collection = MongoFunctions.connect()
if collection is None:
    print("Incorrect username or password.")
    exit()
else:
    print("Welcome to the UML Editor!")

# Test creating a new collection
#collection = MongoFunctions.create_collection()
#if collection is None:
#    print("Username already exists or some other error making the collection.")
#    exit()
#else:
#    print("Collection created successfully.")





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





# Relationship functions tests
# Test adding a Relationship to the database
relationship_object = {
    "object type": "relationship",
    "project": "Test Project",
    "relationship type": "association",
    "class1": "NewTestClass",
    "class2": "TestClass",
}
MongoFunctions.create_relationship(collection, relationship_object)
data = MongoFunctions.get_relationship(collection, "Test Project", "association", "NewTestClass", "TestClass")
print(data)

# Test deleting a Relationship from the database
MongoFunctions.delete_relationship(collection, "Test Project", "association", "NewTestClass", "TestClass")





# Attribute functions tests
# Test adding an attribute to a class in the database
attribute_object = {
    "object type": "attribute",
    "name": "testAttribute2",
    "type": "string",
    "value": "test value",
}
MongoFunctions.create_attribute(collection, "Test Project", "NewTestClass", attribute_object)
data = MongoFunctions.get_class(collection, "Test Project", "NewTestClass")
print(data)

# Test getting an attribute from a class in the database
data = MongoFunctions.get_attribute(collection, "Test Project", "NewTestClass", "testAttribute2")
print(data)

# Test renaming an attribute in the database
MongoFunctions.rename_attribute(collection, "Test Project", "NewTestClass", "testAttribute2", "newTestAttribute2")
data = MongoFunctions.get_class(collection, "Test Project", "NewTestClass")
print(data)

# Test deleting an attribute from a class in the database
MongoFunctions.delete_attribute(collection, "Test Project", "NewTestClass", "testAttribute1")
data = MongoFunctions.get_class(collection, "Test Project", "NewTestClass")
print(data)


 


    



