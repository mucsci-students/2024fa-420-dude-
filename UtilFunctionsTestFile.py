import Utility_Functions as uf
import DBFunctions as dbf
import pytest

# The project data to pass around
project_data = dbf.json_read_file("json_files/TinyDBTestFile.json")
print("Project Data: ", project_data)

########## All Add Tests ##########

# Test 1: Add a new class to the project data that does not exist.
def test_add_nonexisting_class(capsys):
    data = uf.add_class(project_data, "Truck")
    captured = capsys.readouterr()
    try: 
        assert dbf.json_get_class(data, "Truck") is not None
        captured = capsys.readouterr()
    except AssertionError:
        print("Class was not added.")

# Test 2: Add a new class to the project data that already exists.
def test_add_existing_class(capsys):
    data = uf.add_class(project_data, "Car")
    data = uf.add_class(data, "Car")
    classes = dbf.json_get_classes(data)
    count = 0
    for c in classes:
        if c["name"] == "Car":
            count += 1
    captured = capsys.readouterr()
    try:
        assert count == 1
        captured = capsys.readouterr()
    except AssertionError:
        print("Class was not added or was added more than 1x.")

# Test 3: Add a new relationship to the project data that does not exist.
def test_add_nonexisting_relationship(capsys):
    data = uf.add_relationship(project_data, "Car", "Truck", "Aggregation")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_relationship(data, "Car", "Truck") is not None
        captured = capsys.readouterr()
    except AssertionError:
        print("Relationship was not added.")

# Test 4: Add a new relationship to the project data that already exists.
def test_add_existing_relationship(capsys):
    data = uf.add_relationship(project_data, "Tire", "Car", "Composition")
    data = uf.add_relationship(data, "Tire", "Car", "Composition")
    relationships = dbf.json_get_relationships(data)
    count = 0
    for r in relationships:
        if r["source"] == "Tire" and r["destination"] == "Car":
            count += 1
    captured = capsys.readouterr()
    try:
        assert count == 1
        captured = capsys.readouterr()
    except AssertionError:
        print("Relationship was not added or was added more than 1x.")

# Test 5: Add a relationship to the project data where the source/dest does not exist.
def test_add_relationship_no_class(capsys):
    data = uf.add_relationship(project_data, "Car", "Bike", "Aggregation")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_relationship(data, "Car", "Bike") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Relationship was added.")

# Test 6: Add a relationship to the project data where the source/dest is the same.
def test_add_relationship_same_class(capsys):
    data = uf.add_relationship(project_data, "Car", "Car", "Aggregation")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_relationship(data, "Car", "Car") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Relationship was added.")

# Test 7: Add a relationship to the project data with an invalid relationship type.
def test_add_relationship_invalid_type(capsys):
    data = uf.add_class(project_data, "Engine")
    data = uf.add_relationship(data, "Car", "Truck", "None")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_relationship(data, "Car", "Truck") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Relationship was added.")

# Test 8: Add a new field to a class in the project data that does not exist.
def test_add_nonexisting_field(capsys):
    data = uf.add_field(project_data, "Car", "Color")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_field(data, "Car", "Color") is not None
        captured = capsys.readouterr()
    except AssertionError:
        print("Field was not added.")

# Test 9: Add a new field to a class in the project data that already exists.
def test_add_existing_field(capsys):
    data = uf.add_field(project_data, "Car", "Color")
    data = uf.add_field(data, "Car", "Color")
    fields = dbf.json_get_fields(data, "Car")
    count = 0
    for f in fields:
        if f["name"] == "Color":
            count += 1
    captured = capsys.readouterr()
    try:
        assert count == 1
        captured = capsys.readouterr()
    except AssertionError:
        print("Field was not added or was added more than 1x.")

# Test 10: Add a field to a class in the project data that does not exist.
def test_add_field_no_class(capsys):
    data = uf.add_field(project_data, "None", "Color")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_field(data, "None", "Color") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Field was added.")

# Test 11: Add a method to a class in the project data that does not exist.
def test_add_nonexisting_method(capsys):
    data = uf.add_method(project_data, "Car", "drive", [])
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_method(data, "Car", "drive") is not None
        captured = capsys.readouterr()
    except AssertionError:
        print("Method was not added.")

# Test 12: Add a method to a class in the project data that already exists.
def test_add_existing_method(capsys):
    data = uf.add_method(project_data, "Car", "drive", [])
    data = uf.add_method(data, "Car", "drive", [])
    methods = dbf.json_get_methods(data, "Car")
    count = 0
    for m in methods:
        if m["name"] == "drive":
            count += 1
    captured = capsys.readouterr()
    try:
        assert count == 1
        captured = capsys.readouterr()
    except AssertionError:
        print("Method was not added or was added more than 1x.")

# Test 13: Add a method to a class in the project data that does not exist.
def test_add_method_no_class(capsys):
    data = uf.add_method(project_data, "Nothing", "drive", [])
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_method(data, "Nothing", "drive") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Method was added.")

# Test 14: Add a method to a class in the project data with parameters.
def test_add_method_with_params(capsys):
    data = uf.add_method(project_data, "Car", "drive", [{ "name": "speed" }])
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_method(data, "Car", "drive") is not None
        captured = capsys.readouterr()
    except AssertionError:
        print("Method was not added.")

# Test 15: Add a parameter to a method in the project data that does not exist.
def test_add_nonexisting_param(capsys):
    data = uf.add_param(project_data, "Car", "drive", "speed")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_parameter(data, "Car", "drive", "speed") is not None
        captured = capsys.readouterr()
    except AssertionError:
        print("Parameter was not added.")

# Test 16: Add a parameter to a method in the project data that already exists.
def test_add_existing_param(capsys):
    data = uf.add_param(project_data, "Car", "drive", "speed")
    data = uf.add_param(data, "Car", "drive", "speed")
    parameters = dbf.json_get_parameters(data, "Car", "drive")
    count = 0
    for p in parameters:
        if p["name"] == "speed":
            count += 1
    captured = capsys.readouterr()
    try:
        assert count == 1
        captured = capsys.readouterr()
    except AssertionError:
        print("Parameter was not added or was added more than 1x.")

# Test 17: Add a parameter to a method in the project data that does not exist.
def test_add_param_no_class(capsys):
    data = uf.add_param(project_data, "Truck", "drive", "speed")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_parameter(data, "Truck", "drive", "speed") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Parameter was added.")

# Test 18: Add a parameter to a method in the project data that does not exist.
def test_add_param_no_method(capsys):
    data = uf.add_param(project_data, "Car", "stop", "speed")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_parameter(data, "Car", "stop", "speed") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Parameter was added.")

# Test 19: Add a parameter to a method in the project data with the same name.
def test_add_param_same_name(capsys):
    data = uf.add_param(project_data, "Car", "drive", "speed")
    data = uf.add_param(data, "Car", "drive", "speed")
    parameters = dbf.json_get_parameters(data, "Car", "drive")
    count = 0
    for p in parameters:
        if p["name"] == "speed":
            count += 1
    captured = capsys.readouterr()
    try:
        assert count == 1
        captured = capsys.readouterr()
    except AssertionError:
        print("Parameter was not added or was added more than 1x.")





########## All Delete Tests ##########

# Test 20: Delete a class from the project data that does not exist.
def test_delete_nonexisting_class(capsys):
    data = uf.delete_class(project_data, "None")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_class(data, "None") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 21: Delete a class from the project data that exists.
def test_delete_existing_class(capsys):
    data = uf.delete_class(project_data, "Car")
    relationships = dbf.json_get_relationships(data)
    count = 0
    for r in relationships:
        if r["source"] == "Car" or r["destination"] == "Car":
            count += 1
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_class(data, "Car") is None
        assert count == 0
        captured = capsys.readouterr()
    except AssertionError:
        print("Class was not deleted or relationships were not deleted.")

# Test 22: Delete a relationship from the project data that does not exist.
def test_delete_nonexisting_relationship(capsys):
    data = uf.delete_relationship(project_data, "Car", "Truck")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_relationship(data, "Car", "Truck") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 23: Delete a relationship from the project data that exists.
def test_delete_existing_relationship(capsys):
    data = uf.add_relationship(project_data, "Tire", "Car", "Composition")
    data = uf.delete_relationship(data, "Tire", "Car")
    relationships = dbf.json_get_relationships(data)
    count = 0
    for r in relationships:
        if r["source"] == "Tire" and r["destination"] == "Car":
            count += 1
    captured = capsys.readouterr()
    try:
        assert count == 0
        captured = capsys.readouterr()
    except AssertionError:
        print("Relationship was not deleted.")

# Test 24: Delete a relationship from the project data where the source/dest does not exist.
def test_delete_relationship_no_class(capsys):
    data = uf.delete_relationship(project_data, "Car", "Bike")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_relationship(data, "Car", "Bike") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 25: Delete a relationship from the project data where the source/dest is the same.
def test_delete_relationship_same_class(capsys):
    data = uf.delete_relationship(project_data, "Car", "Car")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_relationship(data, "Car", "Car") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 26: Delete a field from a class in the project data that does not exist.
def test_delete_nonexisting_field(capsys):
    data = uf.delete_field(project_data, "Car", "Color")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_field(data, "Car", "Color") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 27: Delete a field from a class in the project data that exists.
def test_delete_existing_field(capsys):
    data = uf.add_field(project_data, "Truck", "Color")
    data = uf.delete_field(data, "Truck", "Color")
    field = dbf.json_get_field(data, "Truck", "Color")
    captured = capsys.readouterr()
    try:
        assert field is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Field was not deleted.")

# Test 28: Delete a field from a class in the project data that does not exist.
def test_delete_field_no_class(capsys):
    data = uf.delete_field(project_data, "None", "Color")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_field(data, "None", "Color") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 29: Delete a method from a class in the project data that does not exist.
def test_delete_nonexisting_method(capsys):
    data = uf.delete_method(project_data, "Car", "drive")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_method(data, "Car", "drive") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 30: Delete a method from a class in the project data that exists.
def test_delete_existing_method(capsys):
    data = uf.add_method(project_data, "Car", "drive", [])
    data = uf.delete_method(data, "Car", "drive")
    method = dbf.json_get_method(data, "Car", "drive")
    captured = capsys.readouterr()
    try:
        assert method is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Method was not deleted.")

# Test 31: Delete a method from a class in the project data that does not exist.
def test_delete_method_no_class(capsys):
    data = uf.delete_method(project_data, "None", "drive")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_method(data, "None", "drive") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 32: Delete a parameter from a method in the project data that does not exist.
def test_delete_nonexisting_param(capsys):
    data = uf.delete_param(project_data, "Truck", "drive", "speed")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_parameter(data, "Car", "drive", "speed") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 33: Delete a parameter from a method in the project data that exists.
def test_delete_existing_param(capsys):
    data = uf.add_param(project_data, "Car", "drive", "speed")
    data = uf.delete_param(data, "Car", "drive", "speed")
    parameter = dbf.json_get_parameter(data, "Car", "drive", "speed")
    captured = capsys.readouterr()
    try:
        assert parameter is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Parameter was not deleted.")

# Test 34: Delete a parameter from a method in the project data that does not exist.
def test_delete_param_no_class(capsys):
    data = uf.delete_param(project_data, "None", "drive", "speed")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_parameter(data, "None", "drive", "speed") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 35: Delete a parameter from a method in the project data that does not exist.
def test_delete_param_no_method(capsys):
    data = uf.delete_param(project_data, "Car", "stop", "speed")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_parameter(data, "Car", "stop", "speed") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")



########## All Update Tests ##########

# Test 36: Update a class in the project data that does not exist.
def test_update_nonexisting_class(capsys):
    data = uf.update_class_name(project_data, "None", "Truck")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_class(data, "Truck") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 37: Update a class in the project data that exists.
def test_update_existing_class(capsys):
    relationships = dbf.json_get_relationships(project_data)
    count = 0
    for r in relationships:
        if r["source"] == "Truck" or r["destination"] == "Truck":
            count += 1
    data = uf.update_class_name(project_data, "Truck", "Car")
    relationships = dbf.json_get_relationships(data)
    count2 = 0
    for r in relationships:
        if r["source"] == "Car" or r["destination"] == "Car":
            count2 += 1
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_class(data, "Truck") is None
        assert dbf.json_get_class(data, "Car") is not None
        assert count == count2
        captured = capsys.readouterr()
    except AssertionError:
        print("Class was not updated or relationships were not updated.")

# Test 38: Update a field in a class in the project data that does not exist.
def test_update_nonexisting_field(capsys):
    data = uf.update_field_name(project_data, "Truck", "None", "Color")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_field(data, "Truck", "Color") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 39: Update a field in a class in the project data that exists.
def test_update_existing_field(capsys):
    data = uf.add_field(project_data, "Truck", "Color")
    data = uf.update_field_name(data, "Truck", "Color", "Paint")
    field = dbf.json_get_field(data, "Truck", "Paint")
    captured = capsys.readouterr()
    try:
        assert field is not None
        captured = capsys.readouterr()
    except AssertionError:
        print("Field was not updated.")

# Test 40: Update a field in a class in the project data that does not exist.
def test_update_field_no_class(capsys):
    data = uf.update_field_name(project_data, "None", "Color", "Paint")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_field(data, "None", "Paint") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 41: Update a method in a class in the project data that does not exist.
def test_update_nonexisting_method(capsys):
    data = uf.update_method_name(project_data, "Truck", "None", "drive")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_method(data, "Truck", "drive") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 42: Update a method in a class in the project data that exists.
def test_update_existing_method(capsys):
    data = uf.add_method(project_data, "Truck", "drive", [])
    data = uf.update_method_name(data, "Truck", "drive", "drive")
    method = dbf.json_get_method(data, "Truck", "drive")
    captured = capsys.readouterr()
    try:
        assert method is not None
        captured = capsys.readouterr()
    except AssertionError:
        print("Method was not updated.")

# Test 43: Update a method in a class in the project data that does not exist.
def test_update_method_no_class(capsys):
    data = uf.update_method_name(project_data, "None", "drive", "drive")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_method(data, "None", "drive") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 44: Update a parameter in a method in the project data that does not exist.
def test_update_nonexisting_param(capsys):
    data = uf.update_param_name(project_data, "Truck", "drive", "None", "speed")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_parameter(data, "Truck", "drive", "speed") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 45: Update a parameter in a method in the project data that exists.
def test_update_existing_param(capsys):
    data = uf.add_param(project_data, "Truck", "drive", "speed")
    data = uf.update_param_name(data, "Truck", "drive", "speed", "velocity")
    parameter = dbf.json_get_parameter(data, "Truck", "drive", "velocity")
    captured = capsys.readouterr()
    try:
        assert parameter is not None
        captured = capsys.readouterr()
    except AssertionError:
        print("Parameter was not updated.")

# Test 46: Update a parameter in a method in the project data that does not exist.
def test_update_param_no_class(capsys):
    data = uf.update_param_name(project_data, "None", "drive", "speed", "velocity")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_parameter(data, "None", "drive", "velocity") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

# Test 47: Update a parameter in a method in the project data that does not exist.
def test_update_param_no_method(capsys):
    data = uf.update_param_name(project_data, "Truck", "None", "speed", "velocity")
    captured = capsys.readouterr()
    try:
        assert dbf.json_get_parameter(data, "Truck", "None", "velocity") is None
        captured = capsys.readouterr()
    except AssertionError:
        print("Function errored.")

