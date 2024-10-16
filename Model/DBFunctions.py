import json

# Global for the JSON file format required by the backend functions
json_format = '''Please make sure data is formatted like so:
                {
                    "classes": [
                        {
                            "name": "Class Name",
                            "fields": [
                                {
                                    { "name": "field1name" },
                                    { "name": "field2name" }
                                }
                            ],
                            "methods": [
                                {
                                    { 
                                        "name": "method1name",
                                        "parameters": [
                                            { "name": "parameter1name" },
                                            { "name": "parameter2name" }
                                        ] 
                                    },
                                    { 
                                        "name": "method2name",
                                        "parameters": [
                                            { "name": "parameter1name" },
                                            { "name": "parameter2name" }
                                        ] 
                                    }
                                }
                            ]
                        }
                    ],
                    "relationships": [
                        {
                            "source": "Class Name",
                            "destination": "Class Name",
                            "type": "Aggregation/Composition/Inheritance/Realization"
                        }
                    ]
                }'''

def json_file_exists(file_path):
    try:
        with open(file_path, "r") as file:
            return True
    except FileNotFoundError:
        return False

############### READ/QUERY FUNCTIONS ###############

# Function to get the JSON file to read from
def json_read_file(file_path):
    if json_file_exists(file_path) == False:
        return None
    with open (file_path, "r") as file:
        data = json.load(file)
    return data

# Function to get the classes from the JSON file
def json_get_classes(data):
    try :
        class_data = data["classes"]
    except KeyError:
        print("Classes could not be found. Empty file or Improperly formatted JSON file.")
        print(json_format)
        return None
    return class_data

# Function to get the relationships from the JSON file
def json_get_relationships(data):
    try:
        relationship_data = data["relationships"]
    except KeyError:
        print("Relationships could not be found. Empty file or Improperly formatted JSON file.")
        print(json_format)
        return None
    return relationship_data

# Function to get a specific class from the JSON file
def json_get_class(data, class_name):
    class_data = json_get_classes(data)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    for c in class_data:
        if c["name"] == class_name:
            return c
    # Commented this out so it would not intefer with the cli interface.
    # print("Class not found. Class may not exist.")
    return None

# Function to get a relationship between two classes
def json_get_relationship(data, source_class, destination_class):
    relationship_data = json_get_relationships(data)
    if relationship_data is None:
        print("Error getting relationship data.")
        print(json_format)
        return None
    for r in relationship_data:
        if r["source"] == source_class and r["destination"] == destination_class:
            return r
    # Commented this out so it would not intefer with the cli interface.
    # print("Relationship not found. One or more classes may not exist or a relationship may not exist.")
    return None

# Function to get the fields of a class
def json_get_fields(data, class_name):
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    try: 
        fields = class_data["fields"]
    except KeyError:
        print("Fields could not be found for class " + class_name + ".")
        print(json_format)
        return None
    return fields

# Function to get a specific field of a class
def json_get_field(data, class_name, field_name):
    fields = json_get_fields(data, class_name)
    if fields is None:
        print("Error getting field data.")
        print(json_format)
        return None
    for f in fields:
        if f["name"] == field_name:
            return f
    print("Field not found. Field may not exist.")
    return None

# Function to get the methods of a class
def json_get_methods(data, class_name):
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    try:
        methods = class_data["methods"]
    except KeyError:
        print("Methods could not be found for class " + class_name + ".")
        print(json_format)
        return None
    return methods

# Function to get a specific method of a class
def json_get_method(data, class_name, method_name):
    methods = json_get_methods(data, class_name)
    if methods is None:
        print("Error getting method data.")
        print(json_format)
        return None
    for m in methods:
        if m["name"] == method_name:
            return m
    # print("Method not found. Method may not exist.")
    return None

# Function to get the parameters of a method
def json_get_parameters(data, class_name, method_name):
    methods = json_get_methods(data, class_name)
    if methods is None:
        print("Error getting method data.")
        print(json_format)
        return None
    for m in methods:
        if m["name"] == method_name:
            try:
                parameters = m["params"]
            except KeyError:
                print("Parameters could not be found for method " + method_name + ".")
                print(json_format)
                return None
            return parameters
    print("Method not found. Method may not exist.")
    return None

# Function to get a specific parameter of a method
def json_get_parameter(data, class_name, method_name, parameter_name):
    parameters = json_get_parameters(data, class_name, method_name)
    if parameters is None:
        print("Error getting parameter data.")
        print(json_format)
        return None
    for p in parameters:
        if p["name"] == parameter_name:
            return p
    print("Parameter not found. Parameter may not exist.")
    return None



############### ADD FUNCTIONS ###############

# Function to write to a JSON file
def json_write_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Function to add a new class to the JSON file
def json_add_class(data, new_class_data):
    # Check if class for format is correct
    class_data = json_get_classes(data)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Add class to JSON file
    class_data.append(new_class_data)
    data["classes"] = class_data
    return data

# Function to add a new relationship to the JSON file
def json_add_relationship(data, new_relationship_data):
    # Check if relationship format is correct
    relationship_data = json_get_relationships(data)
    if relationship_data is None:
        print("Error getting relationship data.")
        print(json_format)
        return None
    # Add relationship to JSON file
    relationship_data.append(new_relationship_data)
    data["relationships"] = relationship_data
    return data

# Function to add a new field to a class in the JSON file
def json_add_field(data, class_name, new_field_data):
    # Get all classes from JSON file
    all_classes = json_get_classes(data)
    if all_classes is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if class format is correct
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if field format is correct
    fields = json_get_fields(data, class_name)
    if fields is None:
        print("Error getting field data.")
        print(json_format)
        return None
    # Add field to JSON file
    fields.append(new_field_data)
    class_data["fields"] = fields
    for c in all_classes:
        if c["name"] == class_name:
            c = class_data
    data["classes"] = all_classes
    return data


# Function to add a new method to a class in the JSON file
def json_add_method(data, class_name, new_method_data):
    # Get all classes from JSON file
    all_classes = json_get_classes(data)
    if all_classes is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if class format is correct
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if method format is correct
    methods = json_get_methods(data, class_name)
    if methods is None:
        print("Error getting method data.")
        print(json_format)
        return None
    # Add method to JSON file
    methods.append(new_method_data)
    class_data["methods"] = methods
    for c in all_classes:
        if c["name"] == class_name:
            c = class_data
    data["classes"] = all_classes
    return data

# Function to add a new parameter to a method in the JSON file
def json_add_parameter(data, class_name, method_name, new_parameter_data):
    # Get all classes from JSON file
    all_classes = json_get_classes(data)
    if all_classes is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if class format is correct
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if method format is correct
    methods = json_get_methods(data, class_name)
    if methods is None:
        print("Error getting method data.")
        print(json_format)
        return None
    # Check if parameter format is correct
    for m in methods:
        if m["name"] == method_name:
            parameters = m["params"]
            if parameters is None:
                print("Error getting parameter data.")
                print(json_format)
                return None
            # Add parameter to JSON file
            parameters.append(new_parameter_data)
            m["params"] = parameters
    class_data["methods"] = methods
    for c in all_classes:
        if c["name"] == class_name:
            c = class_data
    data["classes"] = all_classes
    return data

############### UPDATE FUNCTIONS ###############

# Function to rename a class in the JSON file
def json_rename_class(data, old_class_name, new_class_name):
    # Get all classes from JSON file
    all_classes = json_get_classes(data)
    if all_classes is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if class format is correct
    class_data = json_get_class(data, old_class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Rename class in JSON file
    for c in all_classes:
        if c["name"] == old_class_name:
            c["name"] = new_class_name
    
    # Rename class in relationships
    relationship_data = json_get_relationships(data)
    if relationship_data is None:
        print("Error getting relationship data.")
        print(json_format)
        return None
    for r in relationship_data:
        if r["source"] == old_class_name:
            r["source"] = new_class_name
        if r["destination"] == old_class_name:
            r["destination"] = new_class_name
    # Update project data and return it
    data["classes"] = all_classes
    data["relationships"] = relationship_data
    return data

# Function to rename a field in a class in the JSON file
def json_rename_field(data, class_name, old_field_name, new_field_name):
    # Get all classes from JSON file
    all_classes = json_get_classes(data)
    if all_classes is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if class format is correct
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if field format is correct
    fields = json_get_fields(data, class_name)
    if fields is None:
        print("Error getting field data.")
        print(json_format)
        return None
    # Rename field in JSON file
    for f in fields:
        if f["name"] == old_field_name:
            f["name"] = new_field_name
    class_data["fields"] = fields
    for c in all_classes:
        if c["name"] == class_name:
            c = class_data
    data["classes"] = all_classes
    return data

# Function to rename a method in a class in the JSON file
def json_rename_method(data, class_name, old_method_name, new_method_name):
    # Get all classes from JSON file
    all_classes = json_get_classes(data)
    if all_classes is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if class format is correct
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if method format is correct
    methods = json_get_methods(data, class_name)
    if methods is None:
        print("Error getting method data.")
        print(json_format)
        return None
    # Rename method in JSON file
    for m in methods:
        if m["name"] == old_method_name:
            m["name"] = new_method_name
    class_data["methods"] = methods
    for c in all_classes:
        if c["name"] == class_name:
            c = class_data
    data["classes"] = all_classes
    return data

# Function to rename a parameter in a method in the JSON file
def json_rename_parameter(data, class_name, method_name, old_parameter_name, new_parameter_name):
    # Get all classes from JSON file
    all_classes = json_get_classes(data)
    if all_classes is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if class format is correct
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if method format is correct
    methods = json_get_methods(data, class_name)
    if methods is None:
        print("Error getting method data.")
        print(json_format)
        return None
    # Check if parameter format is correct
    for m in methods:
        if m["name"] == method_name:
            parameters = m["params"]
            if parameters is None:
                print("Error getting parameter data.")
                print(json_format)
                return None
            # Rename parameter in JSON file
            for p in parameters:
                if p["name"] == old_parameter_name:
                    p["name"] = new_parameter_name
            m["params"] = parameters
    class_data["methods"] = methods
    for c in all_classes:
        if c["name"] == class_name:
            c = class_data
    data["classes"] = all_classes
    return data

############### DELETE FUNCTIONS ###############

# Function to remove a class from the JSON file
def json_delete_class(data, class_name):
    # Get all classes from JSON file
    all_classes = json_get_classes(data)
    if all_classes is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if class format is correct
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Remove class from JSON file
    for c in all_classes:
        if c["name"] == class_name:
            all_classes.remove(c)
    # Remove class from relationships
    relationship_data = json_get_relationships(data)
    if relationship_data is None:
        print("Error getting relationship data.")
        print(json_format)
        return None
    for r in relationship_data:
        if r["source"] == class_name or r["destination"] == class_name:
            relationship_data.remove(r)
    # Update project data and return it
    data["classes"] = all_classes
    data["relationships"] = relationship_data
    return data

# Function to remove a relationship from the JSON file
def json_delete_relationship(data, source_class, destination_class):
    # Get all relationships from JSON file
    relationship_data = json_get_relationships(data)
    if relationship_data is None:
        print("Error getting relationship data.")
        print(json_format)
        return None
    # Remove relationship from JSON file
    for r in relationship_data:
        if r["source"] == source_class and r["destination"] == destination_class:
            relationship_data.remove(r)
    # Update project data and return it
    data["relationships"] = relationship_data
    return data

# Function to remove a field from a class in the JSON file
def json_delete_field(data, class_name, field_name):
    # Get all classes from JSON file
    all_classes = json_get_classes(data)
    if all_classes is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if class format is correct
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if field format is correct
    fields = json_get_fields(data, class_name)
    if fields is None:
        print("Error getting field data.")
        print(json_format)
        return None
    # Remove field from JSON file
    for f in fields:
        if f["name"] == field_name:
            fields.remove(f)
    class_data["fields"] = fields
    for c in all_classes:
        if c["name"] == class_name:
            c = class_data
    data["classes"] = all_classes
    return data

# Function to remove a method from a class in the JSON file
def json_delete_method(data, class_name, method_name):
    # Get all classes from JSON file
    all_classes = json_get_classes(data)
    if all_classes is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if class format is correct
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if method format is correct
    methods = json_get_methods(data, class_name)
    if methods is None:
        print("Error getting method data.")
        print(json_format)
        return None
    # Remove method from JSON file
    for m in methods:
        if m["name"] == method_name:
            methods.remove(m)
    class_data["methods"] = methods
    for c in all_classes:
        if c["name"] == class_name:
            c = class_data
    data["classes"] = all_classes
    return data

# Function to remove a parameter from a method in the JSON file
def json_delete_parameter(data, class_name, method_name, parameter_name):
    # Get all classes from JSON file
    all_classes = json_get_classes(data)
    if all_classes is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if class format is correct
    class_data = json_get_class(data, class_name)
    if class_data is None:
        print("Error getting class data.")
        print(json_format)
        return None
    # Check if method format is correct
    methods = json_get_methods(data, class_name)
    if methods is None:
        print("Error getting method data.")
        print(json_format)
        return None
    # Check if parameter format is correct
    for m in methods:
        if m["name"] == method_name:
            parameters = m["params"]
            if parameters is None:
                print("Error getting parameter data.")
                print(json_format)
                return None
            # Remove parameter from JSON file
            for p in parameters:
                if p["name"] == parameter_name:
                    parameters.remove(p)
            m["params"] = parameters
    class_data["methods"] = methods
    for c in all_classes:
        if c["name"] == class_name:
            c = class_data
    data["classes"] = all_classes
    return data

    
        
    

