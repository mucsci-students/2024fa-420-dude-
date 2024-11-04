# This file controls the CLI.
import sys
import copy
from pathlib import Path

# Add the project root to sys.path dynamically
project_root = Path(__file__).resolve().parent.parent
print(project_root)
sys.path.append(str(project_root))

# Import Utility_Functions from the Control package
from Control import Utility_Functions as uf
from Model import DBFunctions as db


global g_file_path; g_file_path = ""

# Command options printed if user inputs "help"
options = '''Commmands:
    mkclass [Name] : 
        - Create a new class with [Name]
    rmclass [Class] : 
        - Deletes [Class] 
    chclass [Class] [New Name] :
        - Rename [Class] with [New Name] 
    mkrelationship [Type] [Class 1] [Class 2] : 
        - Create a new relationship between [Class 1] and [Class 2]
        - Type must be of Aggregation, Composition, Inheritance, or Realization
    rmrelationship[Class 1] [Class 2] : 
        - Delete a relationship between [Class 1] and [Class 2]
        - Type must be of Aggregation, Composition, Inheritance, or Realization
    mkfield [Class] [Field Name] [Type] :
        - Adds fields to the specified [Class]
    rmfield [Class] [Name] :
        - Removes the field [Name] from the class with name [Class]
    chfield [Class] [Old Field] [New Field] :
        - Changes the name of [Old Field] to [New Field] in [Class]
    mkmethod [Class] [Method Name] [Return Type] [Parameter 1] [Parameter 1 Type] [Parameter 2] [Parameter 2 Type]... :
        - Creates methods with all parameters
    rmmethod [Class] [Method Name] :
        - Removes the method with name [Method Name] from [Class]
    chmethod [Class] [Old Method] [New Method]:
        - Changes the name of [Old Method] to [New Method] in [Class]
    mkparameter [Class] [Method] [Parameter Name] [Type] :
        - Adds [Parameter Name] to [Method] for [Class]
    rmparameter [Class] [Method] [Parameter Name] [Type]:
        - Removes [Parameter Name] to [Method] for [Class]
    chparameter [Class] [Method] [Old Param] [New Param] [Type]:
        - Changes the name of [Old Param] to [New Param] for [Method] in [Class]
    save : 
        - Save the current project 
    load [Name] :
        - Loads the project with [Name]
    lsclass :
        - List all classes and their attributes
    classinfo [Class] :
        - Provides information on the [Class] 
    lsrelationship:
        - List all relationships between classes
    undo:
        - Undo the last action
    redo:
        - Redo the last action
    help :
        - Displays this information
    exit :
        - Exits the interface'''

#####################   Functions  ######################

# Checks if the user provided more or less arguments than the number_required
def correct_amount_of_inputs_warning(command, number_required) -> bool:
    argument_met = True
    if len(command) < number_required :
        print("Incorrect number of arguments.\n\tUse \"help\" for information")
        argument_met = False 
    elif len(command) > number_required :
        print("Too many arguments.\n\tTip: Names must be one word.")
        argument_met = False 
    else:
        return argument_met

# Returns the project data for the given file_path
def get_file(file_path):
    try :
        project_data = db.json_read_file(file_path)
        r_file_path = file_path
        if project_data is None:
            raise FileNotFoundError
    except :
        print(file_path + " not a valid file path.")
        r_file_path = input("You must provide a project name (note this is a file path): ")
        return get_file(file_path)
    return (project_data, r_file_path)

def create_or_load_file() :
    print("Would you like to create or load a project?")
    user_input = input("Type \"load\" to open a project or \"create\" to make a new one: ")
    if user_input.lower() == "load":
        file_path = input("Please enter the file you wish to use: ")
        project_data = get_file(file_path)
        return project_data
    elif user_input.lower() == "create":
        file_path = input("Please enter the file you wish to use: ")
        project_data = uf.create_project_data_file(file_path)
        r_file_path = file_path
        return (project_data, r_file_path)
    else:
        return create_or_load_file()


##################  Main Execution Section  ##################


file_data = create_or_load_file()
project_data = file_data[0]
g_file_path = file_data[1]
print("Enter a command, \nUse \"help\" for information")
undo_stack = []
redo_stack = []
undo_clicked = False

# Prompts the user for input
#   DUML stands for Dude UML
user_input = input("DUML: ") # Prompts user for input
command = user_input.split()
# Checks for empty user input
if len(command) == 0:
    command = [" "]
# Continues to prompt user for input until the "exit" command is provided
while command[0] != "exit":
    match command[0]:
        case "mkclass":
            if correct_amount_of_inputs_warning(command, 2) is True:
                if (undo_clicked):
                    redo_stack.clear()
                    undo_clicked = False
                undo_stack.append(copy.deepcopy(project_data))
                project_data = uf.add_class(project_data, command[1])
        case "rmclass":
            if correct_amount_of_inputs_warning(command, 2) is True:
                if (undo_clicked):
                    redo_stack.clear()
                    undo_clicked = False
                undo_stack.append(copy.deepcopy(project_data))
                project_data = uf.delete_class(project_data, command[1])
        case "chclass":
            if correct_amount_of_inputs_warning(command, 3) is True:
                if (undo_clicked):
                    redo_stack.clear()
                    undo_clicked = False
                undo_stack.append(copy.deepcopy(project_data))
                project_data = uf.update_class_name(project_data, command[1], command[2])
        case "mkrel":
            if correct_amount_of_inputs_warning(command, 4) is True:
                type_list = {"Aggregation", "Composition", "Inheritance", "Realization"}
                if command[1] in type_list:
                    if (undo_clicked):
                        redo_stack.clear()
                        undo_clicked = False
                    undo_stack.append(copy.deepcopy(project_data))
                    project_data = uf.add_relationship(project_data, command[2], command[3], command[1])
                else :
                    print("Type must be one of: Aggregation, Composition, Inheritance, Realization")
        case "rmrel":
            if correct_amount_of_inputs_warning(command, 3) is True:
                if (undo_clicked):
                    redo_stack.clear()
                    undo_clicked = False
                undo_stack.append(copy.deepcopy(project_data))
                project_data = uf.delete_relationship(project_data, command[1], command[2])
        case "mkfield":
            if correct_amount_of_inputs_warning(command, 4) is True:
                if (undo_clicked):
                    redo_stack.clear()
                    undo_clicked = False
                undo_stack.append(copy.deepcopy(project_data))
                uf.add_field(project_data, command[1], command[2], command[3])
        case "rmfield":
            if correct_amount_of_inputs_warning(command, 3):
                if (undo_clicked):
                    redo_stack.clear()
                    undo_clicked = False
                undo_stack.append(copy.deepcopy(project_data))
                project_data = uf.delete_field(project_data, command[1], command[2])
        case "chfield":
            if correct_amount_of_inputs_warning(command, 4):
                if (undo_clicked):
                    redo_stack.clear()
                    undo_clicked = False
                undo_stack.append(copy.deepcopy(project_data))
                project_data = uf.update_field_name(project_data, command[1], command[2], command[3])
        case "mkmethod":
            if len(command) < 4:
                print("Incorrect number of arguments.\n\tUse \"help\" for information")
            elif len(command) % 2 == 0: 
                print("Must have return types for parameters")
            else:
                if (undo_clicked):
                    redo_stack.clear()
                    undo_clicked = False
                undo_stack.append(copy.deepcopy(project_data))
                parameter = []
                i = 4
                while i < len(command):
                    param = {
                        "name": command[i],
                        "type": command[i+1]
                    }
                    parameter.append(param)
                    i  = i + 2
                uf.add_method(project_data, command[1], command[2], parameter, command[3])
                
        case "rmmethod":
            if correct_amount_of_inputs_warning(command, 3):
                # Need to add a new function to display methods with a specific name.
                methods = db.json_get_method_with_same_name(project_data, command[1], command[2])
                count = 1
                for method in methods:
                    parameters = method["params"]
                    formatted_params = "("
                    for param in parameters:
                        formatted_params += param["name"] + ": " + param["type"] + ", "
                    if len(parameters) > 0:
                        formatted_params = formatted_params[:-2] + ")"
                    else:
                        formatted_params += ")"
                    print(str(count) + ".) Method: " + method["name"] + formatted_params + " Return Type: " + method["return_type"])
                    count += 1
                number_to_delete = input("Which number method would you like to delete?")
                if number_to_delete.isnumeric() and int(number_to_delete) <= count:
                    if (undo_clicked):
                        redo_stack.clear()
                        undo_clicked = False
                    undo_stack.append(copy.deepcopy(project_data))
                    project_data = uf.delete_method(project_data, command[1], command[2], number_to_delete)
                else:
                    print("Invalid input number input.") 
        case "chmethod":
            if correct_amount_of_inputs_warning(command, 4):
                # Need to add a new function to display methods with a specific name.
                methods = db.json_get_method_with_same_name(project_data, command[1], command[2])
                count = 1
                for method in methods:
                    parameters = method["params"]
                    formatted_params = "("
                    for param in parameters:
                        formatted_params += param["name"] + ": " + param["type"] + ", "
                    if len(parameters) > 0:
                        formatted_params = formatted_params[:-2] + ")"
                    else:
                        formatted_params += ")"
                    print(str(count) + ".) Method: " + method["name"] + formatted_params + " Return Type: " + method["return_type"])
                    count += 1
                number_to_change = input("Which number method would you like to rename?")
                if number_to_change.isnumeric() and int(number_to_change) <= count:
                    if (undo_clicked):
                        redo_stack.clear()
                        undo_clicked = False
                    undo_stack.append(copy.deepcopy(project_data))
                    project_data = uf.update_method_name(project_data, command[1], command[2], command[3], number_to_change)
                else:
                    print("Invalid input number input.")
        case "mkparameter":
            if correct_amount_of_inputs_warning(command, 5):
                methods = db.json_get_method_with_same_name(project_data, command[1], command[2])
                count = 1
                for method in methods:
                    parameters = method["params"]
                    formatted_params = "("
                    for param in parameters:
                        formatted_params += param["name"] + ": " + param["type"] + ", "
                    if len(parameters) > 0:
                        formatted_params = formatted_params[:-2] + ")"
                    else:
                        formatted_params += ")"
                    print(str(count) + ".) Method: " + method["name"] + formatted_params + " Return Type: " + method["return_type"])
                    count += 1
                number_to_change = input("Which number method would you like to add a parameter to?")
                if number_to_change.isnumeric() and int(number_to_change) <= count:
                    if (undo_clicked):
                        redo_stack.clear()
                        undo_clicked = False
                    undo_stack.append(copy.deepcopy(project_data))
                    project_data = uf.add_param(project_data, command[1], command[2], number_to_change, command[3], command[4])
                else:
                    print("Invalid input number input.")
        case "rmparameter":
            if correct_amount_of_inputs_warning(command, 5):
                methods = db.json_get_method_with_same_name(project_data, command[1], command[2])
                count = 1
                for method in methods:
                    parameters = method["params"]
                    formatted_params = "("
                    for param in parameters:
                        formatted_params += param["name"] + ": " + param["type"] + ", "
                    if len(parameters) > 0:
                        formatted_params = formatted_params[:-2] + ")"
                    else:
                        formatted_params += ")"
                    print(str(count) + ".) Method: " + method["name"] + formatted_params + " Return Type: " + method["return_type"])
                    count += 1
                number_to_delete = input("Which number method would you like to remove the parameter from?")
                if number_to_delete.isnumeric() and int(number_to_delete) <= count:
                    if (undo_clicked):
                        redo_stack.clear()
                        undo_clicked = False
                    undo_stack.append(copy.deepcopy(project_data))
                    project_data = uf.delete_param(project_data, command[1], command[2], number_to_delete, command[3], command[4])
                else:
                    print("Invalid input number input.")
        case "chparameter":
            if correct_amount_of_inputs_warning(command, 6):
                methods = db.json_get_method_with_same_name(project_data, command[1], command[2])
                count = 1
                for method in methods:
                    parameters = method["params"]
                    formatted_params = "("
                    for param in parameters:
                        formatted_params += param["name"] + ": " + param["type"] + ", "
                    if len(parameters) > 0:
                        formatted_params = formatted_params[:-2] + ")"
                    else:
                        formatted_params += ")"
                    print(str(count) + ".) Method: " + method["name"] + formatted_params + " Return Type: " + method["return_type"])
                    count += 1
                number_to_change = input("Which number method would you like to change the parameter in?")
                if number_to_change.isnumeric() and int(number_to_change) <= count:
                    if (undo_clicked):
                        redo_stack.clear()
                        undo_clicked = False
                    undo_stack.append(copy.deepcopy(project_data))
                    project_data = uf.update_param_name(project_data, command[1], command[2], command[3], command[4], command[5], number_to_change)
                else:
                    print("Invalid input number input.")
        case "save":
            db.json_write_file(g_file_path, project_data)
            print("Project Saved")
        case "load":
            if correct_amount_of_inputs_warning(command, 2) is True:
                # Checks if the user wants to save the file before loading another
                check_save = input("Would you like to save your current project? (N/y): ").lower()
                while check_save != "n" and check_save != "no" and check_save != "y" and check_save != "yes":
                        check_save = input("Type \"y/yes\" to save or \"n/no\" to exit: ").lower()
                # save the file
                if check_save == "y" or check_save == "yes":
                    db.json_write_file(g_file_path, project_data)
                # Loads the new file
                project_data = get_file(command[1]) 
        case "lsclass":
            uf.display_all_classes(project_data)
        case "classinfo":
            if correct_amount_of_inputs_warning(command, 2) is True:
                uf.display_class(project_data, command[1])
        case "lsrelationship":
            uf.display_all_relationships(project_data)
        case "undo":
            if len(undo_stack) > 0:
                print("Undoing last action")
                redo_stack.append(copy.deepcopy(project_data))
                project_data = undo_stack.pop()
                undo_clicked = True
        case "redo":
            if len(redo_stack) > 0:
                print("Redoing last action")
                undo_stack.append(copy.deepcopy(project_data))
                project_data = redo_stack.pop()
        case "help":
            print(options)
        case " ":
            print("Please provide a command\n\tUse \"help\" for a list of valid commands")
        case _: # Default case if others did not match
            print(command[0] + " is not a command\n\tUse \"help\" for a list of valid commands")

    user_input = input("DUML: ") # Prints the prompt again
    # Splits user input and checks for empty input
    command = user_input.split()
    if len(command) == 0:
        command = [" "]

# Exits the program
user_input = input("Would you like to save? (N/y): ").lower()
while user_input != "n" and user_input != "no" and user_input != "y" and user_input != "yes":
    user_input = input("Type \"y/yes\" to save or \"n/no\" to exit: ").lower()
if user_input == "y" or user_input == "yes":
    db.json_write_file(g_file_path, project_data)
    print(g_file_path + " project saved")
exit(0)
