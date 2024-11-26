from Model import DBFunctions as dbf


# Test connecting to a JSON file
def test_json_connect(capsys):
    assert dbf.json_read_file("sprint3_format.json") is not None
    captured = capsys.readouterr()

# Test file not found
def test_file_not_found(capsys):
    assert(dbf.json_file_exists("nonsense_file_path") is False)
    captured = capsys.readouterr()

# Test file not found for reading
def test_file_not_readable(capsys):
    assert(dbf.json_read_file("nonsense_file_path") is None)
    captured = capsys.readouterr()

# Test key error getting classes
def test_key_not_found_classes(capsys):
    assert(dbf.json_get_classes({}) is None)
    captured = capsys.readouterr()

# Test key error getting relationship
def test_key_not_found_relationships(capsys):
    assert(dbf.json_get_relationships({}) is None)
    captured = capsys.readouterr()

# Test no class data
def test_no_class_data(capsys):
    assert(dbf.json_get_class({}, "name") is None)
    captured = capsys.readouterr()

# Test get relationship data is none
def test_no_relationship_data(capsys):
    assert(dbf.json_get_relationship({}, "thing", "thing2") is None)
    captured = capsys.readouterr()

# Test methods are none
def test_no_methods(capsys):
    assert(dbf.json_get_method_with_same_name({}, "class_name", "method_name") is None)
    captured = capsys.readouterr()

# Test no data when adding class
def test_no_data_adding_class(capsys):
    assert(dbf.json_add_class({}, {}) is None)
    captured = capsys.readouterr()

# Test no data when adding relationship
def test_no_data_adding_relationship(capsys):
    assert(dbf.json_add_relationship({}, {}) is None)
    captured = capsys.readouterr()

# Test no data when adding fields
def test_no_data_adding_field(capsys):
    assert(dbf.json_add_field({}, "class_name", {}) is None)
    captured = capsys.readouterr()

# Test no data when adding method
def test_no_data_adding_method(capsys):
    assert(dbf.json_add_method({}, "class_name", {}) is None)
    captured = capsys.readouterr()

# Test no data when adding parameter
def test_no_data_adding_parameter(capsys):
    assert(dbf.json_add_parameter({}, "class_name", "method_name", 1, {}) is None)
    captured = capsys.readouterr()

# Test no data when renaming classes
def test_no_data_renaming_class(capsys):
    assert(dbf.json_rename_class({}, "old_name", "new_name") is None)
    captured = capsys.readouterr()


# Test no data when updating position 
def test_no_data_updating_position(capsys):
    assert(dbf.json_update_pos({}, "class_name", None) is None)
    captured = capsys.readouterr()

# Test no data when updating field
def test_no_data_updating_field(capsys):
    assert(dbf.json_rename_field({}, "class_name", "old_name", "new_name") is None)
    captured = capsys.readouterr()

# Test no data when updating method
def test_no_data_updating_method(capsys):
    assert(dbf.json_rename_method({}, "class_name", "old_method_name", "new_method_name", 1) is None)
    captured = capsys.readouterr()

# Test no data when updating parameter
def test_no_data_updating_parameter(capsys):
    assert(dbf.json_rename_parameter({}, "class_name", "method_name", 1, "old_name", "new_name") is None)
    captured = capsys.readouterr()

# Test no data when deleting class
def test_no_data_deleting_class(capsys):
    assert(dbf.json_delete_class({}, "class_name") is None)
    captured = capsys.readouterr()

# Test no data when deleting relationship
def test_no_data_deleting_relationship(capsys):
    assert(dbf.json_delete_relationship({}, "source", "dest") is None)
    captured = capsys.readouterr()

# Test no data when deleting field
def test_no_data_deleting_field(capsys):
    assert(dbf.json_delete_field({}, "class_name", "field_name") is None)
    captured = capsys.readouterr()

# Test getting the classes from the JSON file
def test_json_get_classes(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    classes = dbf.json_get_classes(project_data)
    assert classes is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test getting the relationships from the JSON file
def test_json_get_relationships(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    relationships = dbf.json_get_relationships(project_data)
    assert relationships is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test getting a specific class from the JSON file
def test_json_get_class(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Car"
    class_data = dbf.json_get_class(project_data, class_name)
    assert class_data is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test getting a relationship between two classes
def test_json_get_relationship(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    source_class = "Car"
    destination_class = "Tire"
    project_data = dbf.json_add_relationship(project_data, { "source": source_class, "destination": destination_class, "type": "Aggregation" })
    relationship = dbf.json_get_relationship(project_data, source_class, destination_class)
    assert relationship is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test getting the fields of a class
def test_json_get_fields(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Car"
    fields = dbf.json_get_fields(project_data, class_name)
    assert fields is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test getting the methods of a class
def test_json_get_methods(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Car"
    methods = dbf.json_get_methods(project_data, class_name)
    assert methods is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test adding a class to the JSON file
def test_json_add_class(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_data = { "name": "Engine", "fields": [], "methods": [], "position": { "x": 0, "y": 0 } }
    project_data = dbf.json_add_class(project_data, class_data)
    assert dbf.json_get_class(project_data, "Engine") is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test adding a relationship to the JSON file
def test_json_add_relationship(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    relationship_data = { "source": "Tire", "destination": "Car", "type": "Aggregation" }
    project_data = dbf.json_add_relationship(project_data, relationship_data)
    assert dbf.json_get_relationship(project_data, "Tire", "Car") is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test adding a field to a class
def test_json_add_field(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Engine"
    field_data = { "name": "cylinder", "type": "int" }
    project_data = dbf.json_add_field(project_data, class_name, field_data)
    assert dbf.json_get_field(project_data, "Engine", "cylinder") is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test adding a method to a class
def test_json_add_method(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Engine"
    method_data = { "name": "start", "return_type": "void", "params": [] }
    project_data = dbf.json_add_method(project_data, class_name, method_data)
    assert dbf.json_get_method(project_data, "Engine", "start", 1) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test adding a parameter to a method
def test_json_add_parameter(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Tire"
    method_name = "setPSI"
    param_data = { "name": "currentPSI", "type": "int" }
    project_data = dbf.json_add_parameter(project_data, class_name, method_name, 1, param_data)
    assert dbf.json_get_parameter(project_data, "Tire", "setPSI", "currentPSI", "int", 1) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test getting the parameters of a method
def test_json_get_parameters(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Tire"
    method_name = "setPSI"
    parameters = dbf.json_get_parameters(project_data, class_name, method_name, 1)
    assert parameters is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test renaming a class
def test_json_rename_class(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    old_class_name = "Engine"
    new_class_name = "Motor"
    project_data = dbf.json_rename_class(project_data, old_class_name, new_class_name)
    assert dbf.json_get_class(project_data, new_class_name) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test renaming a field
def test_json_rename_field(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Motor"
    old_field_name = "cylinder"
    new_field_name = "cylinders"
    project_data = dbf.json_rename_field(project_data, class_name, old_field_name, new_field_name)
    assert dbf.json_get_field(project_data, class_name, new_field_name) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test renaming a method
def test_json_rename_method(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Motor"
    old_method_name = "start"
    new_method_name = "rev"
    project_data = dbf.json_rename_method(project_data, class_name, old_method_name, new_method_name, 1)
    assert dbf.json_get_method(project_data, class_name, new_method_name, 1) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test renaming a parameter
def test_json_rename_parameter(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Tire"
    method_name = "setPSI"
    old_param_name = "currentPSI"
    new_param_name = "nowPSI"
    project_data = dbf.json_rename_parameter(project_data, class_name, method_name, 1, old_param_name, new_param_name)
    print(project_data)
    assert dbf.json_get_parameter(project_data, class_name, method_name, new_param_name, "int", 1) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test deleting a parameter from a method
def test_json_delete_parameter(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Tire"
    method_name = "setPSI"
    param_name = "newPSI"
    project_data = dbf.json_delete_parameter(project_data, class_name, method_name, 1, param_name)
    print(project_data)
    assert dbf.json_get_parameter(project_data, class_name, method_name, param_name, "string", 1) is None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test deleting a method from a class
def test_json_delete_method(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Motor"
    method_name = "rev"
    project_data = dbf.json_delete_method(project_data, class_name, method_name, 1)
    assert dbf.json_get_method(project_data, class_name, method_name, 1) is None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test deleting a field from a class
def test_json_delete_field(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Motor"
    field_name = "cylinders"
    project_data = dbf.json_delete_field(project_data, class_name, field_name)
    assert dbf.json_get_field(project_data, class_name, field_name) is None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test deleting a relationship from the JSON file
def test_json_delete_relationship(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    source_class = "Tire"
    destination_class = "Car"
    project_data = dbf.json_delete_relationship(project_data, source_class, destination_class)
    assert dbf.json_get_relationship(project_data, source_class, destination_class) is None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test deleting a class from the JSON file
def test_json_delete_class(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Motor"
    project_data = dbf.json_delete_class(project_data, class_name)
    assert dbf.json_get_class(project_data, class_name) is None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test getting all of the methods with the same name
def test_get_method_with_same_name(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Vehicle"
    project_data = dbf.json_add_class(project_data, { "name": "Vehicle", "fields": [], "methods": [], "position": { "x": 0, "y": 0 } })
    method_data1 = { "name": "rev", "return_type": "void", "params": [] }
    method_data2 = { "name": "rev", "return_type": "void", "params": [{ "name": "rpms", "type": "int"}] }
    project_data = dbf.json_add_method(project_data, class_name, method_data1)
    project_data = dbf.json_add_method(project_data, class_name, method_data2)
    methods = dbf.json_get_method_with_same_name(project_data, class_name, "rev")
    assert len(methods) == 2
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test getting the field of a class
def test_json_get_field(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Vehicle"
    field_data = { "name": "wheels", "type": "int" }
    project_data = dbf.json_add_field(project_data, class_name, field_data)
    field = dbf.json_get_field(project_data, class_name, "wheels")
    assert field is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test getting the method of a class
def test_json_get_method(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Vehicle"
    method_name = "rev"
    count = 1
    method = dbf.json_get_method(project_data, class_name, method_name, count)
    assert method is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test getting the parameter of a method
def test_json_get_parameter(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Vehicle"
    method_name = "rev"
    param_name = "rpms"
    param_type = "int"
    count = 2
    param = dbf.json_get_parameter(project_data, class_name, method_name, param_name, param_type, count)
    assert param is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test deleting all of the parameters of a method
def test_json_delete_all_parameters(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Vehicle"
    method_name = "rev"
    project_data = dbf.json_delete_all_parameters(project_data, class_name, method_name, 2)
    assert dbf.json_get_parameters(project_data, class_name, method_name, 2) == []
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Test updating the position of a class
def test_json_update_class_position(capsys):
    project_data = dbf.json_read_file("sprint3_format.json")
    class_name = "Vehicle"
    new_position = { "x": 10, "y": 20 }
    project_data = dbf.json_update_pos(project_data, class_name, new_position)
    assert dbf.json_get_class(project_data, class_name)["position"] == new_position
    captured = capsys.readouterr()
    dbf.json_write_file("sprint3_format.json", project_data)

# Reset the JSON file to its original state
def test_json_reset_file(capsys):
    project_data = {
        "classes": [
            {
            "name": "Tire",
            "fields": [
                { "name": "diameter", "type": "float" },
                { "name": "psi", "type": "float" },
                { "name": "brand", "type": "string" }
            ],
            "methods": [
                {
                "name": "setPSI",
                "return_type" : "void",
                "params": [
                    { "name": "new_psi", "type": "string" }
                ]
                }
            ]
            },
            {
            "name": "Car",
            "fields" : [
                { "name": "make", "type": "string" },
                { "name": "model", "type": "string" },
                { "name": "year", "type": "int" }
            ],
            "methods": [
                {
                "name" : "drive",
                "return_type" : "void",
                "params": []
                }
            ],
            "position": {
                "x": 0,
                "y": 0
            }
            }
        ],
        "relationships": [
            {
            "source": "Tire",
            "destination": "Car",
            "type": "Composition"
            }
        ]
        }
    dbf.json_write_file("sprint3_format.json", project_data)
    assert dbf.json_read_file("sprint3_format.json") == project_data

# Test getting the fields of a class with improper format
def test_fields_improper_format(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire",

            }
        ]
    }
    assert dbf.json_get_fields(stub_data, "Tire") == None

# Test getting the methods of a class with improper format
def test_methods_improper_format(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire",
            }
        ]
    }
    assert dbf.json_get_methods(stub_data, "Tire") == None

# Test getting the method of a class with more than one method with the same name
def test_method_multiple_amount(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire",
                "fields": [],
                "methods": [
                    {
                        "name": "setPSI",
                        "return_type": "void",
                        "params": [
                            { "name": "new_psi", "type": "string" }
                        ]
                    },
                    {
                        "name": "setPSI",
                        "return_type": "void",
                        "params": [
                            { "name": "new_psi", "type": "int" }
                        ]
                    }
                ]
            }
        ]
    }
    assert dbf.json_get_method(stub_data, "Tire", "setPSI", 2) != None

# Test getting the parameters of a method with improper format
def test_parameters_improper_format(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire",
                "fields": [],
                "methods": [
                    {
                        "name": "setPSI",
                        "return_type": "void"
                    }
                ]
            }
        ]
    }
    assert dbf.json_get_parameters(stub_data, "Tire", "setPSI", 1) == None

# Test adding a field to a class with improper format
def test_add_field_no_class(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_add_field(stub_data, "Tire", { "name": "diameter", "type": "float" }) == None

# Test adding a field to a class with improper format
def test_add_field_no_field(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_add_field(stub_data, "Tire", { "name": "psi", "type": "int" }) == None

# Test adding a method to a class with improper format
def test_add_method_no_class(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_add_method(stub_data, "Tire", { "name": "setPSI", "return_type": "void", "params": [] }) == None

# Test adding a method to a class with improper format
def test_add_method_no_method(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_add_method(stub_data, "Tire", { "name": "drive", "return_type": "void", "params": [] }) == None

# Test adding a parameter to a method with improper format
def test_add_parameter_no_class(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_add_parameter(stub_data, "Tire", "setPSI", 1, { "name": "new_psi", "type": "string" }) == None

# Test adding a parameter to a method with improper format
def test_add_parameter_no_method(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_add_parameter(stub_data, "Tire", "drive", 1, { "name": "new_psi", "type": "string" }) == None

# Test adding a parameter to a method with no param key
def test_add_parameter_no_param_key(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire",
                "fields": [],
                "methods": [
                    {
                        "name": "setPSI",
                        "return_type": "void",
                    }
                ]
            }
        ]
    }
    assert dbf.json_add_parameter(stub_data, "Tire", "setPSI", 1, { "name": "new_psi", "type": "string" }) == None

# Test renaming a class with improper format
def test_rename_class_no_class(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_rename_class(stub_data, "Tire", "Wheel") == None

# Test renaming a class with no relationship data
def test_rename_class_no_relationships(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_rename_class(stub_data, "Tire", "Wheel") == None

# Test renaming a class that is the source of a relationship
def test_rename_class_relationship_source(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire",
                "fields": [],
                "methods": []
            }
        ],
        "relationships": [
            {
                "source": "Tire",
                "destination": "Car",
                "type": "Composition"
            }
        ]
    }
    assert dbf.json_rename_class(stub_data, "Tire", "Wheel") != None

# Test updating the position of a class with improper format
def test_update_class_position_no_class(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_update_pos(stub_data, "Tire", { "x": 10, "y": 20 }) == None

# Test renaming a field with improper format
def test_rename_field_no_class(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_rename_field(stub_data, "Tire", "diameter", "size") == None

# Test renaming a field with no field data
def test_rename_field_no_field(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_rename_field(stub_data, "Tire", "diameter", "size") == None

# Test renaming a method with improper format
def test_rename_method_no_class(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_rename_method(stub_data, "Tire", "setPSI", "setPressure", 1) == None

# Test renaming a method with no method data
def test_rename_method_no_method(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_rename_method(stub_data, "Tire", "setPSI", "setPressure", 1) == None

# Test renaming a parameter with improper format
def test_rename_parameter_no_class(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_rename_parameter(stub_data, "Tire", "setPSI", 1, "new_psi", "old_psi") == None

# Test renaming a parameter with no methods
def test_rename_parameter_no_method(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_rename_parameter(stub_data, "Tire", "setPSI", 1, "new_psi", "old_psi") == None

# Test renaming a parameter with no param key
def test_rename_parameter_no_param_key(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire",
                "fields": [],
                "methods": [
                    {
                        "name": "setPSI",
                        "return_type": "void"
                    }
                ]
            }
        ]
    }
    assert dbf.json_rename_parameter(stub_data, "Tire", "setPSI", 1, "new_psi", "old_psi") == None
    
# Test deleting a class with no class data
def test_delete_class_no_class(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_delete_class(stub_data, "Tire") == None

# Test deleting a class with no relationships
def test_delete_class_no_relationships(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_delete_class(stub_data, "Tire") == None

# Test deleting a field with no class data
def test_delete_field_no_class(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_delete_field(stub_data, "Tire", "diameter") == None

# Test deleting a field with no field data
def test_delete_field_no_field(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_delete_field(stub_data, "Tire", "diameter") == None

# Test deleting a method with no class key
def test_delete_method_no_class(capsys):
    stub_data = {
    }
    assert dbf.json_delete_method(stub_data, "Tire", "setPSI", 1) == None

# Test deleting a method with no class data but a class key
def test_delete_method_no_class_data(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_delete_method(stub_data, "Tire", "setPSI", 1) == None

# Test deleting a method with no method data
def test_delete_method_no_method(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_delete_method(stub_data, "Tire", "setPSI", 1) == None

# Test deleting a parameter with no class key
def test_delete_parameter_no_class(capsys):
    stub_data = {
    }
    assert dbf.json_delete_parameter(stub_data, "Tire", "setPSI", 1, "new_psi") == None

# Test deleting a parameter with no class data but a class key
def test_delete_parameter_no_class_data(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_delete_parameter(stub_data, "Tire", "setPSI", 1, "new_psi") == None

# Test deleting a parameter with no method key
def test_delete_parameter_no_method(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_delete_parameter(stub_data, "Tire", "setPSI", 1, "new_psi") == None

# Test deleting a param with no param key
def test_delete_param_no_key(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire",
                "fields": [],
                "methods": [
                    {
                        "name": "setPSI",
                        "return_type": "void"
                    }
                ]
            }
        ]
    }
    assert dbf.json_delete_parameter(stub_data, "Tire", "setPSI", 1, "new_psi") == None

# Test deleting a param
def test_delete_param(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire",
                "fields": [],
                "methods": [
                    {
                        "name": "setPSI",
                        "return_type": "void",
                        "params": [
                            { "name": "new_psi", "type": "string" }
                        ]
                    }
                ]
            }
        ]
    }
    assert dbf.json_delete_parameter(stub_data, "Tire", "setPSI", 1, "new_psi") != None

# Test deleting all params with no class key
def test_delete_all_params_no_class(capsys):
    stub_data = {
    }
    assert dbf.json_delete_all_parameters(stub_data, "Tire", "setPSI", 1) == None

# Test deleting all params with no class data but a class key
def test_delete_all_params_no_class_data(capsys):
    stub_data = {
        "classes": []
    }
    assert dbf.json_delete_all_parameters(stub_data, "Tire", "setPSI", 1) == None

# Test deleting all params with no method key
def test_delete_all_params_no_method(capsys):
    stub_data = {
        "classes": [
            {
                "name": "Tire"
            }
        ]
    }
    assert dbf.json_delete_all_parameters(stub_data, "Tire", "setPSI", 1) == None