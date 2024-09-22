import MongoFunctions



# Tests for getting or creating new collecions
# Comment out which way you want to test

# Test connecting to the database
print("Connecting to the database...")
collection = MongoFunctions.connect()
if collection is None:
    print("\tIncorrect username or password.")
    exit()
else:
    print("\tWelcome to the UML Editor!")

# Test creating a new collection
#print("Creating a new user...")
#collection = MongoFunctions.create_collection()
#if collection is None:
#    print("\tUsername already exists or some other error making the collection.")
#    exit()
#else:
#    print("\tCollection created successfully.")





# Project functions tests
# Test adding a Project to the database
print("\nTesting Project functions:")
project_object = {
    "object type": "project",
    "name": "TestProject",
}

# Test creating a project
print("\n\tCreating and retrieving a project:")
MongoFunctions.create_project(collection, project_object)

# Test getting a Project from the database
project_object = MongoFunctions.get_project(collection, "Test Project")
print("\t\t" + str(project_object))





# Class functions tests
print("\n\nTesting Class functions:")
# Test adding a Class to the database
class_object = {
    "object type": "class",
    "project": "TestProject",
    "name": "TestClass",
    "attributes": [{ "object type": "attribute", "name": "testAttribute1", "type": "int", "value": 0 }],
}

# Test creating a class
print("\n\tCreating and retrieving a class:")
MongoFunctions.create_class(collection, class_object)

# Test getting a class from the database
class_object = MongoFunctions.get_class(collection, "TestProject", "TestClass")
print("\t\t" + str(class_object))

# Test renaming a class in the database
print("\n\tRenaming a class:")
MongoFunctions.rename_class(collection, "TestProject", "TestClass", "NewTestClass")
class_object2 = MongoFunctions.get_class(collection, "TestProject", "NewTestClass")
print("\t\t" + str(class_object2))

# Test getting all classes in a project from the database
print("\n\tListing all classes in a project:")
class_object2 = {
    "object type": "class",
    "project": "TestProject",
    "name": "TestClass2",
    "attributes": [{ "object type": "attribute", "name": "testAttribute2", "type": "string", "value": "test value" }]
}
MongoFunctions.create_class(collection, class_object2)
class_objects = MongoFunctions.list_classes(collection, "TestProject")
for class_object in class_objects:
    print("\t\t" + str(class_object))

# Test deleting a class from the database
print("\n\tDeleting a class:")
MongoFunctions.delete_class(collection, "TestProject", "NewTestClass")
data = MongoFunctions.get_class(collection, "TestProject", "NewTestClass")
print("\t\t" + str(data))

# Recreating class for later use
print("\n\tRecreating classes for later use.")
class_object3 = {
    "object type": "class",
    "project": "TestProject",
    "name": "TestClass",
    "attributes": [{ "object type": "attribute", "name": "testAttribute1", "type": "int", "value": 0 }],
}
MongoFunctions.create_class(collection, class_object3)






# Relationship functions tests
print("\n\nTesting Relationship functions:")
# Test adding a Relationship to the database
relationship_object = {
    "object type": "relationship",
    "project": "TestProject",
    "relationship type": "association",
    "class1": "TestClass",
    "class2": "TestClass2",
}

print("\n\tCreating and retrieving a relationship:")
MongoFunctions.create_relationship(collection, relationship_object)
data = MongoFunctions.get_relationship(collection, "TestProject", "association", "TestClass", "TestClass2")
print("\t\t" + str(data))

# Test to list all relationships in a project
print("\n\tListing all relationships in a project:")
relationship_objects = MongoFunctions.list_relationships(collection, "TestProject")
for relationship_object in relationship_objects:
    print("\t\t" + str(relationship_object))

# Test deleting a Relationship from the database
print("\n\tDeleting a relationship:")
MongoFunctions.delete_relationship(collection, "TestProject", "association", "TestClass", "TestClass2")
data = MongoFunctions.get_relationship(collection, "TestProject", "association", "TestClass", "TestClass2")
print("\t\t" + str(data))







# Attribute functions tests\
print("\n\nTesting Attribute functions: ")
# Test adding an attribute to a class in the database
attribute_object = {
    "object type": "attribute",
    "name": "testAttribute2",
    "type": "string",
    "value": "testValue",
}
print("\n\tCreating and retrieving an attribute:")
MongoFunctions.create_attribute(collection, "TestProject", "TestClass", attribute_object)
data = MongoFunctions.get_class(collection, "TestProject", "TestClass")
print("\t\t" + str(data))

# Test getting an attribute from a class in the database
print("\n\tGetting an attribute:")
data = MongoFunctions.get_attribute(collection, "TestProject", "TestClass", "testAttribute2")
print("\t\t" + str(data))

# Test renaming an attribute in the database
print("\n\tRenaming an attribute:")
MongoFunctions.rename_attribute(collection, "TestProject", "TestClass", "testAttribute2", "newTestAttribute2")
data = MongoFunctions.get_class(collection, "TestProject", "TestClass")
print("\t\t" + str(data))

# Test deleting an attribute from a class in the database
print("\n\tDeleting an attribute:")
MongoFunctions.delete_attribute(collection, "TestProject", "TestClass", "testAttribute1")
data = MongoFunctions.get_class(collection, "TestProject", "TestClass")
print("\t\t" + str(data))


 


    



