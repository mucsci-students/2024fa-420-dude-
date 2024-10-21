from Model import DBFunctions as dbf


# Test connecting to a JSON file
def test_json_connect(capsys):
    assert dbf.json_read_file("sprint2_format.json") is not None
    captured = capsys.readouterr()

# Test getting the classes from the JSON file
def test_json_get_classes(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    classes = dbf.json_get_classes(project_data)
    assert classes is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test getting the relationships from the JSON file
def test_json_get_relationships(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    relationships = dbf.json_get_relationships(project_data)
    assert relationships is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test getting a specific class from the JSON file
def test_json_get_class(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Car"
    class_data = dbf.json_get_class(project_data, class_name)
    assert class_data is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test getting a relationship between two classes
def test_json_get_relationship(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    source_class = "Car"
    destination_class = "Tire"
    project_data = dbf.json_add_relationship(project_data, { "source": source_class, "destination": destination_class, "type": "Aggregation" })
    relationship = dbf.json_get_relationship(project_data, source_class, destination_class)
    assert relationship is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test getting the fields of a class
def test_json_get_fields(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Car"
    fields = dbf.json_get_fields(project_data, class_name)
    assert fields is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test getting the methods of a class
def test_json_get_methods(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Car"
    methods = dbf.json_get_methods(project_data, class_name)
    assert methods is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test adding a class to the JSON file
def test_json_add_class(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_data = { "name": "Engine", "fields": [], "methods": [], "position": { "x": 0, "y": 0 } }
    project_data = dbf.json_add_class(project_data, class_data)
    assert dbf.json_get_class(project_data, "Engine") is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test adding a relationship to the JSON file
def test_json_add_relationship(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    relationship_data = { "source": "Tire", "destination": "Car", "type": "Aggregation" }
    project_data = dbf.json_add_relationship(project_data, relationship_data)
    assert dbf.json_get_relationship(project_data, "Tire", "Car") is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test adding a field to a class
def test_json_add_field(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Engine"
    field_data = { "name": "cylinder", "type": "int" }
    project_data = dbf.json_add_field(project_data, class_name, field_data)
    assert dbf.json_get_field(project_data, "Engine", "cylinder") is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test adding a method to a class
def test_json_add_method(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Engine"
    method_data = { "name": "start", "return_type": "void", "params": [] }
    project_data = dbf.json_add_method(project_data, class_name, method_data)
    assert dbf.json_get_method(project_data, "Engine", "start", 1) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test adding a parameter to a method
def test_json_add_parameter(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Tire"
    method_name = "setPSI"
    param_data = { "name": "currentPSI", "type": "int" }
    project_data = dbf.json_add_parameter(project_data, class_name, method_name, 1, param_data)
    assert dbf.json_get_parameter(project_data, "Tire", "setPSI", "currentPSI", "int", 1) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test getting the parameters of a method
def test_json_get_parameters(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Tire"
    method_name = "setPSI"
    parameters = dbf.json_get_parameters(project_data, class_name, method_name, 1)
    assert parameters is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test renaming a class
def test_json_rename_class(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    old_class_name = "Engine"
    new_class_name = "Motor"
    project_data = dbf.json_rename_class(project_data, old_class_name, new_class_name)
    assert dbf.json_get_class(project_data, new_class_name) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test renaming a field
def test_json_rename_field(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Motor"
    old_field_name = "cylinder"
    new_field_name = "cylinders"
    project_data = dbf.json_rename_field(project_data, class_name, old_field_name, new_field_name)
    assert dbf.json_get_field(project_data, class_name, new_field_name) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test renaming a method
def test_json_rename_method(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Motor"
    old_method_name = "start"
    new_method_name = "rev"
    project_data = dbf.json_rename_method(project_data, class_name, old_method_name, new_method_name, 1)
    assert dbf.json_get_method(project_data, class_name, new_method_name, 1) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test renaming a parameter
def test_json_rename_parameter(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Tire"
    method_name = "setPSI"
    old_param_name = "currentPSI"
    new_param_name = "nowPSI"
    project_data = dbf.json_rename_parameter(project_data, class_name, method_name, 1, old_param_name, new_param_name)
    print(project_data)
    assert dbf.json_get_parameter(project_data, class_name, method_name, new_param_name, "int", 1) is not None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test deleting a parameter from a method
def test_json_delete_parameter(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Tire"
    method_name = "setPSI"
    param_name = "newPSI"
    project_data = dbf.json_delete_parameter(project_data, class_name, method_name, 1, param_name)
    print(project_data)
    assert dbf.json_get_parameter(project_data, class_name, method_name, param_name, "string", 1) is None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test deleting a method from a class
def test_json_delete_method(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Motor"
    method_name = "rev"
    project_data = dbf.json_delete_method(project_data, class_name, method_name, 1)
    assert dbf.json_get_method(project_data, class_name, method_name, 1) is None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test deleting a field from a class
def test_json_delete_field(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Motor"
    field_name = "cylinders"
    project_data = dbf.json_delete_field(project_data, class_name, field_name)
    assert dbf.json_get_field(project_data, class_name, field_name) is None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test deleting a relationship from the JSON file
def test_json_delete_relationship(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    source_class = "Tire"
    destination_class = "Car"
    project_data = dbf.json_delete_relationship(project_data, source_class, destination_class)
    assert dbf.json_get_relationship(project_data, source_class, destination_class) is None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

# Test deleting a class from the JSON file
def test_json_delete_class(capsys):
    project_data = dbf.json_read_file("sprint2_format.json")
    class_name = "Motor"
    project_data = dbf.json_delete_class(project_data, class_name)
    assert dbf.json_get_class(project_data, class_name) is None
    captured = capsys.readouterr()
    dbf.json_write_file("sprint2_format.json", project_data)

