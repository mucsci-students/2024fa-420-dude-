import Utility_Functions
import MongoFunctions

# Tests for the utility functions
collection = MongoFunctions.connect()
if collection is None:
    print("There was an error connecting to the database!")
    exit()
else:
    print("Successfully connected to the database!")

# Tests for project functions
print("\nTesting project functions:")

# Test to create a project that doesn't yet exist
print("\n\tCreating a project that doesn't yet exist:")
data = Utility_Functions.add_project(collection, "Test Project")
if data is not None:
    print("\t\tSuccessfully created project: " + data["name"])
    print("\t\t" + str(data))

# Test to create a project that already exists
print("\n\tCreating a project that already exists:")
data = Utility_Functions.add_project(collection, "Test Project")
if data is not None:
    print("\t\tSuccessfully retrieved project: " + data["name"])
    print("\t\t" + str(data))

# Test to create a project with an empty name
print("\n\tCreating a project with an empty name:")
data = Utility_Functions.add_project(collection, "")
if data is None:
    print("\t\tSuccessfully handled empty name.")
    print("\t\t" + str(data))



# Tests for class functions
print("\nTesting class functions:")

# Test to create a class that doesn't yet exist
print("\n\tCreating a class that doesn't yet exist:")
data = Utility_Functions.add_class(collection, "Test Project", "Test Class")
if data is not None:
    print("\t\tSuccessfully created class: " + data["name"])
    print("\t\t" + str(data))

# Test to create a class that already exists
print("\n\tCreating a class that already exists:")
data = Utility_Functions.add_class(collection, "Test Project", "Test Class")
if data is not None:
    print("\t\tSuccessfully retrieved class: " + data["name"])
    print("\t\t" + str(data))

# Test to create a class with an empty name
print("\n\tCreating a class with an empty name:")
data = Utility_Functions.add_class(collection, "Test Project", "")
if data is None:
    print("\t\tSuccessfully handled empty name.")
    print("\t\t" + str(data))

# Test to create a class with a project that doesn't exist
print("\n\tCreating a class with a project that doesn't exist:")
data = Utility_Functions.add_class(collection, "Nonexistent Project", "Test Class")
if data is None:
    print("\t\tSuccessfully handled nonexistent project.")
    print("\t\t" + str(data))



# Tests for relationship functions
print("\nTesting relationship functions:")

Utility_Functions.add_class(collection, "Test Project", "Test Class2")

# Test to create a realationship that doesn't yet exist.
print("\n\tCreating a relationship that doesn't yet exist:")
data = Utility_Functions.add_relationship(collection, "Test Project", "Composition", "Test Class", "Test Class2")
if data is not None:
    print("\t\tSuccessfully created realtionship between Test Class and Test Class2")
    print("\t\t" + str(data))

# Test to create a realationship that already exists.
print("\n\tCreating a relationship that already exists:")
data = Utility_Functions.add_relationship(collection, "Test Project", "Composition", "Test Class", "Test Class2")
if data is not None:
    print("\t\tSuccessfully retrieved realtionship between Test Class and Test Class2")
    print("\t\t" + str(data))

# Test to create a realationship where one the classes doesn't exist.
print("\n\tCreating a realationship where one the classes doesn't exist:")
data = Utility_Functions.add_relationship(collection, "Test Project", "Composition", "Test Class", "I Don't Exist")
if data is not None:
    print("\t\tSuccessfully handled realtionship between Test Class and Test Class2")
    print("\t\t" + str(data))

# Test to create a realationship where the relationship type is invalid.
print("\n\tCreating a realationship where the relationship type is invalid:")
data = Utility_Functions.add_relationship(collection, "Test Project", "Ionic", "Test Class", "Test Class2")
if data is not None:
    print("\t\tSuccessfully handled invalid realtionship type.")
    print("\t\t" + str(data))


    
# Tests for attribute functions

print("\n\tCreating an attribute that doesn't yet exist:")
data = Utility_Functions.add_attribute(collection, "Test Project", "Test Class", "Test Atrribute", "int", 11)
if data is not None:
    print("\t\tSuccessfully created attribute.")
    print("\t\t" + str(data))

print("\n\tCreating an attribute that already exists:")
data = Utility_Functions.add_attribute(collection, "Test Project", "Test Class", "Test Atrribute", "int", 11)
if data is not None:
    print("\t\tSuccessfully retreived attribute.")
    print("\t\t" + str(data))

print("\n\tCreating an attribute that already exists:")
data = Utility_Functions.add_attribute(collection, "Test Project", "I Dont Exist", "Test Atrribute", "int", 11)
if data is not None:
    print("\t\tSuccessfully handled faulty attribute")
    print("\t\t" + str(data))