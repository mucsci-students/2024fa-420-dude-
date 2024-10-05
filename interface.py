# This file controls the CLI.
#maybe use argpars

#pyunit for testing

from DBFunctions import json_get_classes, json_get_relationships, json_get_class, json_read_file, json_write_file
from Utility_Functions import *

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
        - Type must be of Aggregation or Composition
    rmrel [Class 1] [Class 2] : 
        - Delete a relationship between [Class 1] and [Class 2]
        - Type must be of Aggregation or Composition
    mkfld [Class] [Name] ...
    mkmthd [Class] [Name] ...
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

def wrong_amount_of_inputs_warning(command, number_required) -> bool:
    argument_not_met = False
    if len(command) < number_required :
        print("Incorrect number of arguments.\n\tUse \"help\" for information")
        argument_not_met = True
    elif len(command) > number_required :
        print("Too many arguments.\n\tTip: Names must be one word.")
        argument_not_met = True
    else:
        return argument_not_met

##################  Main Execution Section  ##################


file_path = input("What project would you like to work on (note this is a file path for now): ")
while file_path == "":
    file_path = input("You must provide a project name (note this is a file path for now): ")
# I must include a check if the file_path is valid.
project_data = json_read_file(file_path)
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
            if wrong_amount_of_inputs_warning(command, 2) is False:
                add_class(project_data, command[1])
                print("Added class " + command[1]) # Should add the ability to add fields and methods on class creation.
        case "rmcls":
            if wrong_amount_of_inputs_warning(command, 2) is False:
                delete_class(project_data, command[1])
                print("Removed class " + command[1])
        case "chngcls":
            if wrong_amount_of_inputs_warning(command, 3) is False:
                update_class_name(project_data, command[1], command[2])
                print("Changed class " + command[1] + " to " + command[2])
        case "mkrel":
            if wrong_amount_of_inputs_warning(command, 4) is False:
                add_relationship(project_data, command[1], command[2], command[3])
                print("Created relationship between " +  command[1] + " and " + command[2] + " with type " + command[3])
        case "rmrel":
            if wrong_amount_of_inputs_warning(command, 3) is False:
                delete_relationship(project_data, command[1], command[2])
                print("Removed relationship between class " + command[1] + " and " + command[2])
        case "mkfld":
            print("Not yet implemented")
        case "mkmthd":
            print("Not yet implemented")
        case "save":
            json_write_file(file_path, project_data)
            print("Project Saved")
        case "load":
            if wrong_amount_of_inputs_warning(command, 2) is False:
                print("Not implemented")
            else :
                print("Not implemented")
        case "lscls":
            classes = json_get_classes(project_data) 
            print(classes)
        case "clsinfo":
            if wrong_amount_of_inputs_warning(command, 2) is False:
                class_info = json_get_class(project_data, command[1])
                print(class_info)
        case "lsrel":
            relationship = json_get_relationships(project_data)
            print(relationship)
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
exit(0)
