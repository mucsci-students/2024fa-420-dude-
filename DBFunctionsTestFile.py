import DBFunctions as dbf
import json

# Test connecting to a JSON file
project_data = dbf.json_read_file("json_files/TinyDBTestFile.json")
if project_data is None:
    print("Could not connect to the JSON file.")
    exit()
print("\nFile Data:\n" + str(project_data))

# Test getting the classes from the JSON file
classes = dbf.json_get_classes(project_data)
print("\nClasses:\n" + str(classes))

# Test getting the relationships from the JSON file
relationships = dbf.json_get_relationships(project_data)
print("\nRelationships:\n" + str(relationships))

# Test getting a specific class from the JSON file
class_name = "Tire"
class_data = dbf.json_get_class(project_data, class_name)
print("\nClass Data for " + class_name + ":\n" + str(class_data))

# Test getting a relationship between two classes
source_class = "Tire"
destination_class = "Car"
relationship = dbf.json_get_relationship(project_data, source_class, destination_class)
print("\nRelationship between " + source_class + " and " + destination_class + ":\n" + str(relationship))

# Test getting the fields of a class
class_name = "Tire"
fields = dbf.json_get_fields(project_data, class_name)
print("\nFields for " + class_name + ":\n" + str(fields))

# Test getting the methods of a class
class_name = "Tire"
methods = dbf.json_get_methods(project_data, class_name)
print("\nMethods for " + class_name + ":\n" + str(methods))

# Test adding a class to the JSON file
class_name = "Engine"
fields = [{ "name": "cylinder" }, { "name": "displacement" }, { "name": "power" }]
methods = [ { "name": "start", "params": [] }, { "name": "stop", "params": [] } ]
new_class = { "name": class_name, "fields": fields, "methods": methods }
project_data = dbf.json_add_class(project_data, new_class)
print("\nUnsaved project data after adding " + class_name + ":\n" + str(project_data))

# Test adding a relationship to the JSON file
new_relationship = { "source": "Car", "destination": "Engine", "type": "Aggregation" }
project_data = dbf.json_add_relationship(project_data, new_relationship)
print("\nUnsaved project data after adding relationship between Car and Engine:\n" + str(project_data))

# Test adding a field to a class
field_data = { "name": "fuel" }
project_data = dbf.json_add_field(project_data, "Engine", field_data)
print("\nUnsaved project data after adding field to Engine:\n" + str(project_data))

# Test adding a method to a class
method_data = { "name": "rev", "params": [] }
project_data = dbf.json_add_method(project_data, "Engine", method_data)
print("\nUnsaved project data after adding method to Engine:\n" + str(project_data))

# Test adding a parameter to a method
method_name = "rev"
param_data = { "name": "rpm" }
project_data = dbf.json_add_parameter(project_data, "Engine", method_name, param_data)
print("\nUnsaved project data after adding parameter to rev method in Engine:\n" + str(project_data))

# Test getting the parameters of a method
class_name = "Engine"
method_name = "rev"
params = dbf.json_get_parameters(project_data, class_name, method_name)
print("\nParameters for " + method_name + " method in " + class_name + ":\n" + str(params))

# Test renaming a class
old_class_name = "Engine"
new_class_name = "Motor"
project_data = dbf.json_rename_class(project_data, old_class_name, new_class_name)
print("\nUnsaved project data after renaming " + old_class_name + " to " + new_class_name + ":\n" + str(project_data))

# Test renaming a field
class_name = "Motor"
old_field_name = "cylinder"
new_field_name = "cylinders"
project_data = dbf.json_rename_field(project_data, class_name, old_field_name, new_field_name)
print("\nUnsaved project data after renaming " + old_field_name + " to " + new_field_name + " in " + class_name + ":\n" + str(project_data))

# Test renaming a method
class_name = "Motor"
old_method_name = "start"
new_method_name = "ignite"
project_data = dbf.json_rename_method(project_data, class_name, old_method_name, new_method_name)
print("\nUnsaved project data after renaming " + old_method_name + " to " + new_method_name + " in " + class_name + ":\n" + str(project_data))

# Test renaming a parameter
class_name = "Motor"
method_name = "rev"
old_param_name = "rpm"
new_param_name = "revolutions"
project_data = dbf.json_rename_parameter(project_data, class_name, method_name, old_param_name, new_param_name)
print("\nUnsaved project data after renaming " + old_param_name + " to " + new_param_name + " in " + method_name + " method in " + class_name + ":\n" + str(project_data))

# Save the project data to the JSON file
dbf.json_write_file("json_files/TinyDBTestFile.json", project_data)
project_data = dbf.json_read_file("json_files/TinyDBTestFile.json")
print("\nFile after saving:\n" + str(project_data))

# Test deleting a parameter from a method
class_name = "Motor"
method_name = "rev"
param_name = "revolutions"
project_data = dbf.json_delete_parameter(project_data, class_name, method_name, param_name)
print("\nUnsaved project data after deleting " + param_name + " from " + method_name + " method in " + class_name + ":\n" + str(project_data))

# Test deleting a method from a class
class_name = "Motor"
method_name = "ignite"
project_data = dbf.json_delete_method(project_data, class_name, method_name)
print("\nUnsaved project data after deleting " + method_name + " from " + class_name + ":\n" + str(project_data))

# Test deleting a field from a class
class_name = "Motor"
field_name = "cylinders"
project_data = dbf.json_delete_field(project_data, class_name, field_name)

# Test deleting a relationship from the JSON file
source_class = "Tire"
destination_class = "Car"
project_data = dbf.json_delete_relationship(project_data, source_class, destination_class)
print("\nUnsaved project data after deleting relationship between " + source_class + " and " + destination_class + ":\n" + str(project_data))

# Test deleting a class from the JSON file
class_name = "Motor"
project_data = dbf.json_delete_class(project_data, class_name)
print("\nUnsaved project data after deleting " + class_name + ":\n" + str(project_data))

# Save the project data to the JSON file
dbf.json_write_file("json_files/TinyDBTestFile.json", project_data)
project_data = dbf.json_read_file("json_files/TinyDBTestFile.json")
print("\nFile after saving:\n" + str(project_data))

