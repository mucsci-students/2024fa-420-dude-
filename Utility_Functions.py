import DBFunctions as dbf


############### All add functions. ####################

# Function to add a class to the project data.
def add_class(project_data, class_name):
    class_data = dbf.json_get_class(project_data, class_name)
    if class_data is not None:
        print("Class already exists.")
        return project_data

    class_data = {
        "name": class_name,
        "fields": [],
        "methods": []
    }
    print("Added class " + class_name)
    return dbf.json_add_class(project_data, class_data)

# Function to add a relationship to the project data.
def add_relationship(project_data, source, dest, rel_type):
    rel_data = dbf.json_get_relationship(project_data, source, dest)
    if rel_data is not None:
        print("Relationship already exists.")
        return project_data
    
    source_data = dbf.json_get_class(project_data, source)
    dest_data = dbf.json_get_class(project_data, dest)
    if source_data is None or dest_data is None:
        print("Source or destination class does not exist.")
        return project_data
    
    if source == dest:
        print("Source and destination class cannot be the same.")
        return project_data
    
    if rel_type != "Aggregation" and rel_type != "Composition" and rel_type != "Inheritance" and rel_type != "Realization":
        print("Invalid relationship type.")
        return project_data

    rel_data = {
        "source": source,
        "destination": dest,
        "type": rel_type
    }

    print("Created relationship between " +  source  + " and " + dest + " with type " + rel_type)
    return dbf.json_add_relationship(project_data, rel_data)

# Function to add a field to a class in the project data.
def add_field(project_data, class_name, field_name):
    field_data = dbf.json_get_fields(project_data, class_name)
    if field_data is None:
        print("Class does not exist.")
        return project_data
    
    for field in field_data:
        if field["name"] == field_name:
            print("Field already exists.")
            return project_data

    field_data = {
        "name": field_name
    }
    print("Added field " + field_name + " to class " + class_name + ".")
    return dbf.json_add_field(project_data, class_name, field_data)

# Function to add a method to a class in the project data.
def add_method(project_data, class_name, method_name, params):
    class_data = dbf.json_get_class(project_data, class_name)
    if class_data is None:
        print("Class does not exist.")
        return project_data
    
    method_data = dbf.json_get_method(project_data, class_name, method_name)
    if method_data is not None:
        print("Method already exists.")
        return project_data

    method_data = {
        "name": method_name,
        "params": params
    }
    print("Added parameters [", end="")
    print(*params, sep=", ", end="")
    print("] to method " + method_name + " for class " + class_name + ".")
    return dbf.json_add_method(project_data, class_name, method_data)

# Function to add a parameter to a method in the project data.
def add_param(project_data, class_name, method_name, param_name):
    class_data = dbf.json_get_class(project_data, class_name)
    if class_data is None:
        print("Class does not exist.")
        return project_data
    method_data = dbf.json_get_method(project_data, class_name, method_name)
    if method_data is None:
        print("Method does not exist.")
        return project_data
    param_data = dbf.json_get_parameters(project_data, class_name, method_name)
    for param in param_data:
        if param["name"] == param_name:
            print("Parameter already exists.")
            return project_data

    param_data = {
        "name": param_name
    }

    return dbf.json_add_parameter(project_data, class_name, method_name, param_data)


############### All delete functions. ####################

# Function to delete a class from the project data.
def delete_class(project_data, class_name):
    class_data = dbf.json_get_class(project_data, class_name)
    if class_data is None:
        print("Class does not exist.")
        return project_data

    print("Removed class " + class_name)
    return dbf.json_delete_class(project_data, class_name)

# Function to delete a relationship from the project data.
def delete_relationship(project_data, source, dest):
    class1_data = dbf.json_get_class(project_data, source)
    class2_data = dbf.json_get_class(project_data, dest)
    if class1_data is None or class2_data is None:
        print("Source or destination class does not exist.")
        return project_data
    rel_data = dbf.json_get_relationship(project_data, source, dest)
    if rel_data is None:
        print("Relationship does not exist.")
        return project_data
    print("Removed relationship between class " + source + " and " + dest)
    return dbf.json_delete_relationship(project_data, source, dest)

# Function to delete a field from a class in the project data.
def delete_field(project_data, class_name, field_name):
    class_data = dbf.json_get_class(project_data, class_name)
    if class_data is None:
        print("Class does not exist.")
        return project_data
    field_data = dbf.json_get_field(project_data, class_name, field_name)
    if field_data is None:
        print("Field does not exist.")
        return project_data

    return dbf.json_delete_field(project_data, class_name, field_name)

# Function to delete a method from a class in the project data.
def delete_method(project_data, class_name, method_name):
    class_data = dbf.json_get_class(project_data, class_name)
    if class_data is None:
        print("Class does not exist.")
        return project_data
    method_data = dbf.json_get_method(project_data, class_name, method_name)
    if method_data is None:
        print("Method does not exist.")
        return project_data

    print("Removed method " + method_name + " from class " + class_name)
    return dbf.json_delete_method(project_data, class_name, method_name)

# Function to delete a parameter from a method in the project data.
def delete_param(project_data, class_name, method_name, param_name):
    class_data = dbf.json_get_class(project_data, class_name)
    if class_data is None:
        print("Class does not exist.")
        return project_data
    method_data = dbf.json_get_method(project_data, class_name, method_name)
    if method_data is None:
        print("Method does not exist.")
        return project_data
    param_data = dbf.json_get_parameter(project_data, class_name, method_name, param_name)
    if param_data is None:
        print("Method does not exist or class does not exist.")
        return project_data
    print("Parameter does not exist.")
    return project_data

############### All update functions. ####################

# Function to rename a class in the project data.
def update_class_name(project_data, old_name, new_name):
    class_data = dbf.json_get_class(project_data, old_name)
    if class_data is None:
        print("Class does not exist.")
        return project_data

    print("Changed class " + old_name + " to " + new_name)
    return dbf.json_rename_class(project_data, old_name, new_name)

# Function to rename a field in a class in the project data.
def update_field_name(project_data, class_name, old_name, new_name):
    class_data = dbf.json_get_class(project_data, class_name)
    if class_data is None:
        print("Class does not exist.")
        return project_data
    field_data = dbf.json_get_field(project_data, class_name, old_name)
    if field_data is None:
        print("Field does not exist.")
        return project_data

    return dbf.json_rename_field(project_data, class_name, old_name, new_name)

# Function to rename a method in a class in the project data.
def update_method_name(project_data, class_name, old_name, new_name):
    class_data = dbf.json_get_class(project_data, class_name)
    if class_data is None:
        print("Class does not exist.")
        return project_data
    method_data = dbf.json_get_method(project_data, class_name, old_name)
    if method_data is None:
        print("Method does not exist.")
        return project_data

    return dbf.json_rename_method(project_data, class_name, old_name, new_name)

# Function to rename a parameter in a method in the project data.
def update_param_name(project_data, class_name, method_name, old_name, new_name):
    class_data = dbf.json_get_class(project_data, class_name)
    if class_data is None:
        print("Class does not exist.")
        return project_data
    method_data = dbf.json_get_method(project_data, class_name, method_name)
    if method_data is None:
        print("Method does not exist.")
        return project_data
    param_data = dbf.json_get_parameter(project_data, class_name, method_name, old_name)
    if param_data is None:
        print("Parameter does not exist.")
        return project_data
    return dbf.json_rename_parameter(project_data, class_name, method_name, old_name, new_name)
    

############### All display functions. ####################

# Function to display all classes in the project data.
def display_class(project_data, class_name):
    class_data = dbf.json_get_class(project_data, class_name)
    if class_data is None:
        print("Class does not exist.")
        return project_data
    print("\nClass Data:\n")
    print("Class Name: " + class_data["name"])
    print("Fields:")
    for field in class_data["fields"]:
        print(field["name"])
    print("Methods:")
    for method in class_data["methods"]:
        param_string = "("
        for param in method["params"]:
            param_string += param["name"] + ", "
        if len(param_string) > 1:
            param_string = param_string[:-2] + ")"
        else:
            param_string += ")"
        print(method["name"] + param_string + "\n")
    return project_data
    
# Function to display a relationship in the project data.
def display_relationship(project_data, source, dest):
    rel_data = dbf.json_get_relationship(project_data, source, dest)
    if rel_data is None:
        print("Relationship does not exist.")
        return project_data
    print("\nRelationship Data:\n")
    print("Source: " + rel_data["source"])
    print("Destination: " + rel_data["destination"])
    print("Type: " + rel_data["type"] + "\n")
    return project_data


############### Create file function. ####################

# Function to create a new project data file.
def create_project_data_file(file_path):
    project_data = {
        "classes": [],
        "relationships": []
    }
    dbf.json_write_file(file_path, project_data)
    project_data = dbf.json_read_file(file_path)
    if project_data is None:
        print("Error creating project data file.")
        return None
    print("Created new project data file at path: " + file_path)
    return project_data



