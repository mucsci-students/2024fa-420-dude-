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




# Tests for relationship functions




# Tests for attribute functions