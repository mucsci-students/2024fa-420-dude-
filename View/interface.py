# This file controls the CLI.
import sys
from pathlib import Path

# Add the project root to sys.path dynamically
project_root = Path(__file__).resolve().parent.parent
print(project_root)
sys.path.append(str(project_root))

# Now import Utility_Functions from the Control package
from Control import Utility_Functions as uf
from Model import DBFunctions as db

#TODO:add param function

global g_file_path; g_file_path = ""

# Command options printed if user inputs "help"
options = '''Commmands:
    mkcls [Name] : 
        - Create a new class with [Name]
    rmcls [Class] : 
        - Deletes [Class] 
    chngcls [Class] [New Name] :
        - Rename [Class] with [New Name] 
    mkrel [Type] [Class 1] [Class 2] : 
        - Create a new relationship between [Class 1] and [Class 2]
        - Type must be of Aggregation, Composition, Inheritance, or Realization
    rmrel [Class 1] [Class 2] : 
        - Delete a relationship between [Class 1] and [Class 2]
        - Type must be of Aggregation, Composition, Inheritance, or Realization
    mkfld [Class] :
        - Adds fields to the specified [Class]
    rmfld [Class] [Name] :
        - Removes the field [Name] from the class with name [Class]
    mkmthd [Class] [Method Name] :
        - Creates methods until "done" is input
    rmmthd [Class] [Method Name] :
        - Removes parameters from [Method Name] from [Class]
    mkpram [Class] [Method] [Parameter Name] :
        - Adds [Parameter Name] to [Method] for [Class]
    rmpram [Class] [Method] [Parameter Name] :
        - Removes [Parameter Name] to [Method] for [Class]
    chngpram [Class] [Method] [Old Param] [New Param] :
        - Changes the name of [Old Param] to [New Param] for [Method] in [Class]
    save : 
        - Save the current project 
    load [Name] :
        - Loads the project with [Name]
    lscls :
        - List all classes and their attributes
    clsinfo [Class] :
        - Provides information on the [Class] 
    lsrel :
        - List all relationships between classes
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
        case "mkcls":
            if correct_amount_of_inputs_warning(command, 2) is True:
                project_data = uf.add_class(project_data, command[1])
        case "rmcls":
            if correct_amount_of_inputs_warning(command, 2) is True:
                project_data = uf.delete_class(project_data, command[1])
        case "chngcls":
            if correct_amount_of_inputs_warning(command, 3) is True:
                project_data = uf.update_class_name(project_data, command[1], command[2])
        case "mkrel":
            if correct_amount_of_inputs_warning(command, 4) is True:
                type_list = {"Aggregation", "Composition", "Inheritance", "Realization"}
                if command[1] in type_list:
                    project_data = uf.add_relationship(project_data, command[2], command[3], command[1])
                else :
                    print("Type must be one of: Aggregation, Composition, Inheritance, Realization")
        case "rmrel":
            if correct_amount_of_inputs_warning(command, 3) is True:
                project_data = uf.delete_relationship(project_data, command[1], command[2])
        case "mkfld":
            if correct_amount_of_inputs_warning(command, 2) is True:
                print("Provide a field, type \"done\" when finished.")
                field = input("AddField: ")
                while field.lower() != "done":
                    if field == "":
                        while field == "":
                            print("Must provide a field name")
                            field = input("AddField: ")
                    uf.add_field(project_data, command[1], field)
                    field = input("AddField: ")
        case "rmfld":
            if correct_amount_of_inputs_warning(command, 3):
                project_data = uf.delete_field(project_data, command[1], command[2])
        case "mkmthd":
            if correct_amount_of_inputs_warning(command, 3):
                print("Provide parameter, type \"done\" when finished.")
                parameter =  input("AddParam: ")
                parameter_list = []
                while parameter != "done":
                    if parameter == "":
                        while field == "":
                            print("Must provide a field name")
                            parameter = input("AddField: ")
                    parameter_list.append(parameter)
                    parameter = input("AddParam: ")
                uf.add_method(project_data, command[1], command[2], parameter_list)
        case "rmmthd":
            if correct_amount_of_inputs_warning(command, 3):
                uf.delete_method(project_data, command[1], command[2])
        case "mkpram":
            if correct_amount_of_inputs_warning(command, 4):
                uf.add_param(project_data, command[1], command[2], command[3])
        case "rmpram":
            if correct_amount_of_inputs_warning(command, 4):
                uf.delete_param(project_data, command[1], command[2], command[3])
        case "chngpram":
            if correct_amount_of_inputs_warning(command, 5):
                uf.update_param_name(project_data, command[1], command[2], command[3], command[4])
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
        case "lscls":
            uf.display_all_classes(project_data)
        case "clsinfo":
            if correct_amount_of_inputs_warning(command, 2) is True:
                uf.display_class(project_data, command[1])
        case "lsrel":
            uf.display_all_relationships(project_data)
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
