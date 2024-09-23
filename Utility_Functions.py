import MongoFunctions


############### All add functions. ###############

# This function adds a project to the database. If the project already exists, it will return the data for the preexisting project.
def add_project(collection, name):

    # Check if the name is valid.
    if len(name) < 1:
        print("Please enter a valid name!")
        return None
    
    # Check if the project already exists.
    data = MongoFunctions.get_project(collection, name)

    # If the project already exists, return the data for the preexisting project.
    if data is not None: 
        print("Project already exists. Returning data for preexisting project.")
        return data

    # Create the project object.
    project_object = {
        "object type": "project",
        "name": name,
    }

    # Insert the project object into the collection.
    MongoFunctions.create_project(collection, project_object)

    # Get the project object from the collection.
    data = MongoFunctions.get_project(collection, name)

    # If the project object was successfully created, return the data for the project.
    if data is not None: 
        return data
    else:
        print("The was an error in making this project!")
        return None


# This function adds a class to the database. If the class already exists, it will return the data for the preexisting class.
def add_class(collection, project, name):
    
    # Check if the name is valid.
    if len(name) < 1:
        print("Please enter a valid name!")
        return None
    
    # Check if the project exists.
    data = MongoFunctions.get_project(collection, project)
    # If the project does not exist, return None.
    if data is None:
        print("Project does not exist!")
        return None
    
    # Check if the class already exists.
    data = MongoFunctions.get_class(collection, project, name)
    # If the class already exists, return the data for the preexisting class.
    if data is not None: 
        print("Class already exists. Returning data for preexisting class.")
        return data

    # Create the class object.
    class_object = {
        "object type": "class",
        "project": project,
        "name": name,
        "attributes": [],
    }

    # Insert the class object into the collection.
    MongoFunctions.create_class(collection, class_object)

    # Get the class object from the collection.
    data = MongoFunctions.get_class(collection, project, name)

    # If the class object was successfully created, return the data for the class.
    if data is not None: 
        return data
    else:
        print("The was an error in making this class!")
        return None


# This function adds a relationship to the database. If the relationship already exists, it will return the data for the preexisting relationship.
def add_relationship(collection, project, type, class1_name, class2_name):
    
    # Check if the relationship already exists.
    data = MongoFunctions.get_relationship(collection, project, type, class1_name, class2_name)
    # If the relationship already exists, return the data for the preexisting relationship.
    if data is not None: return data

    # Check if the classes exist.
    if (MongoFunctions.get_class(collection, project, class1_name) == None) or (MongoFunctions.get_class(collection, project, class2_name) == None):
        print("One or more classes does not exist!")
        return None

    # Check if the relationship type is valid.
    if (type != "Aggregation") and (type != "Composition"):
        print("Type is not a valid relationship type!")
        return None

    # Create the relationship object.
    relationship_object = {
        "object type": "relationship",
        "project": project,
        "relationship type": type,
        "class1": class1_name,
        "class2": class2_name,
    }

    # Insert the relationship object into the collection.
    MongoFunctions.create_relationship(collection, relationship_object)

    # Get the relationship object from the collection.
    data = MongoFunctions.get_relationship(collection, project, type, class1_name, class2_name)

    # If the relationship object was successfully created, return the data for the relationship.
    if data is not None: 
        return data
    else:
        print("The was an error in making this relationship!")
        return None 
    

# This function adds an attribute to the database. If the attribute already exists, it will return the data for the preexisting attribute.
def add_attribute(collection, project, class_name, attribute_name, type, value):
    
    # Checks for a valid name.
    if len(attribute_name) < 1:
        print("Please enter a valid name!")
        return None

    # Checks if the class exists.
    if MongoFunctions.get_class(collection, project, class_name) == None:
        print("This class doesn't exist!")
        return None

    # Checks if the attribute already exists.
    data = MongoFunctions.get_attribute(collection, project, class_name, attribute_name)
    # If the attribute already exists, return the data for the preexisting attribute.
    if data is not None: return data

    # Create the attribute object.
    attribute_object = {
        "object type": "attribute",
        "name": attribute_name,
        "type": type,
        "value": value,
    }

    # Insert the attribute object into the collection.
    MongoFunctions.create_attribute(collection, project, class_name, attribute_object)

    # Get the attribute object from the collection.
    data = MongoFunctions.get_attribute(collection, project, class_name, attribute_name)

    # If the attribute object was successfully created, return the data for the attribute.
    if data is not None: 
        return data
    else:
        print("There was an error in making this attribute!")
        return None 





############### All delete functions. ###############

# This function deletes a project from the database.
def delete_project(collection, project):
    # Check if the project exists. If so, delete it.
    data = MongoFunctions.get_project(collection, project)
    if data is None:
        print("There was an error deleting this project!")
    else:
        MongoFunctions.delete_project(collection, project)


# This function deletes a class from the database.
def delete_class(collection, project, name):
    # Check if the class exists. If so, delete it.
    data = MongoFunctions.get_class(collection, project, name)
    if data is None:
        print("There was an error deleting this class!")
    else:
        MongoFunctions.delete_class(collection, project, name)


# This function deletes a relationship from the database.
def delete_relationship(collection, project, relationship_type, class_name1, class_name2):
    # Check if the relationship exists. If so, delete it.
    data = MongoFunctions.get_relationship(collection, project, relationship_type, class_name1, class_name2)
    if data is None:
        print("There was an error deleting this relationship!")
    else:
        MongoFunctions.delete_relationship(collection, project, relationship_type, class_name1, class_name2)


# This function deletes an attribute from the database.
def delete_attribute(collection, project, class_name, attribute_name, type, value):
    # Check if the attribute exists. If so, delete it.
    data = MongoFunctions.get_attribute(collection, project, class_name, attribute_name)
    if data is None:
        print("There was an error deleting this class!")
    else:
        MongoFunctions.delete_attribute(collection, project, class_name, attribute_name)





############### All rename functions. ###############

# This function renames a project in the database.
def rename_class(collection, project, current_name, new_name):
    # Check if the class exists. If so, rename it.
    data = MongoFunctions.get_class(collection, project, current_name)
    if data is None:
        print("There was an error renaming this class!")
    else:
        # Check if the new name is valid.
        if len(new_name) < 1:
            print("Please enter a valid name!")
            return None
        MongoFunctions.rename_class(collection, project, current_name, new_name)


# This function renames a relationship in the database.
def rename_attribute(collection, project, class_name, current_name, new_name):
    # Check if the attribute exists. If so, rename it.
    data = MongoFunctions.get_attribute(collection, project, class_name, current_name)
    if data is None:
        print("There was an error deleting this class!")
    else:
        # Check if the new name is valid.
        if len(new_name) < 1:
            print("Please enter a valid name!")
            return None
        MongoFunctions.rename_attribute(collection, project, class_name, current_name, new_name)




