import MongoFunctions


# All add functions.

def add_project(collection, name):

    data = MongoFunctions.get_project(collection, name)

    if data is not None: return data

    project_object = {
    "object type": "project",
    "name": name,
}

    MongoFunctions.create_project(collection, project_object)

    data = MongoFunctions.get_project(collection, name)

    if data is not None: 
        return data
    else:
        print("The was an error in making this project!")
        return None



def add_class(collection, project, name):
    
    data = MongoFunctions.get_class(collection, project, name)

    if data is not None: return data

    class_object = {
        "object type": "class",
        "project": project,
        "name": name,
        "attributes": [],
    }

    MongoFunctions.create_class(collection, class_object)

    data = MongoFunctions.get_class(collection, project, name)

    if data is not None: 
        return data
    else:
        print("The was an error in making this class!")
        return None



def add_relationship(collection, project, type, class1_name, class2_name):
    
    data = MongoFunctions.get_relationship(collection, project, type, class1_name, class2_name)

    if data is not None: return data

    relationship_object = {
    "object type": type,
    "project": project,
    "relationship type": type,
    "class1": class1_name,
    "class2": class2_name,
}

    MongoFunctions.create_relationship(collection, relationship_object)

    data = MongoFunctions.get_relationship(collection, project, type, class1_name, class2_name)

    if data is not None: 
        return data
    else:
        print("The was an error in making this relationship!")
        return None 
    

def add_attribute(collection, project, class_name, attribute_name, type, value):
    
    data = MongoFunctions.get_attribute(collection, project, class_name, attribute_name)

    if data is not None: return data

    attribute_object = {
    "object type": "attribute",
    "name": attribute_name,
    "type": type,
    "value": value,
    }

    MongoFunctions.create_attribute(collection, project, class_name, attribute_object)

    data = MongoFunctions.get_attribute(collection, project, class_name, attribute_name)

    if data is not None: 
        return data
    else:
        print("The was an error in making this attribute!")
        return None 


# All delete functions.


def delete_project(collection, project):
    data = MongoFunctions.get_project(collection, project)
    if data is None:
        print("There was an error deleting this project!")
    else:
        MongoFunctions.delete_project(collection, project)


def delete_class(collection, project, name):
    
    data = MongoFunctions.get_class(collection, project, name)
    if data is None:
        print("There was an error deleting this class!")
    else:
        MongoFunctions.delete_class(collection, project, name)

def delete_relationship(collection, project, relationship_type, class_name1, class_name2):

    data = MongoFunctions.get_relationship(collection, project, relationship_type, class_name1, class_name2)
    if data is None:
        print("There was an error deleting this relationship!")
    else:
        MongoFunctions.delete_relationship(collection, project, relationship_type, class_name1, class_name2)

def delete_attribute(collection, project, class_name, attribute_name, type, value):

    data = MongoFunctions.get_attribute(collection, project, class_name, attribute_name)
    if data is None:
        print("There was an error deleting this class!")
    else:
        MongoFunctions.delete_attribute(collection, project, class_name, attribute_name)


# All rename functions.


def rename_class(collection, project, current_name, new_name):
    data = MongoFunctions.get_class(collection, project, current_name)
    if data is None:
        print("There was an error renaming this class!")
    else:
        MongoFunctions.rename_class(collection, project, current_name, new_name)

def rename_attribute(collection, project, class_name, current_name, new_name):
    data = MongoFunctions.get_attribute(collection, project, class_name, current_name)
    if data is None:
        print("There was an error deleting this class!")
    else:
        MongoFunctions.rename_attribute(collection, project, class_name, current_name, new_name)


#Tests

