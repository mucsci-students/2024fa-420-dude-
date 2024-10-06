# This file controls the CLI.
#maybe use argpars

#pyunit for testing

from DBFunctions import json_get_classes, json_get_relationships, json_get_class, json_read_file, json_write_file
import Utility_Functions as uf

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

# Checks if the user provided more or less arguments than the number_required
def correct_amount_of_inputs_warning(command, number_required) -> bool:
    argument_not_met = False
    if len(command) < number_required :
        print("Incorrect number of arguments.\n\tUse \"help\" for information")
        argument_not_met = True
    elif len(command) > number_required :
        print("Too many arguments.\n\tTip: Names must be one word.")
        argument_not_met = True
    else:
        return argument_not_met

# Returns the project data for the given file_path
def get_file(file_path):
    try :
        project_data = json_read_file(file_path)
        if project_data is None:
            raise FileNotFoundError
    except :
        print(file_path + " not a valid file path.")
        file_path = input("You must provide a project name (note this is a file path): ")
        return get_file(file_path)
    return project_data

##################  Main Execution Section  ##################

file_path = input("Please enter the file you wish to use: ")
project_data = get_file(file_path)
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
                print("Added class " + command[1]) #TODO: Should add the ability to add fields and methods on class creation.
        case "rmcls":
            if correct_amount_of_inputs_warning(command, 2) is True:
                project_data = uf.delete_class(project_data, command[1])
                print("Removed class " + command[1])
        case "chngcls":
            if correct_amount_of_inputs_warning(command, 3) is True:
                project_data = uf.update_class_name(project_data, command[1], command[2])
                print("Changed class " + command[1] + " to " + command[2])
        case "mkrel":
            if correct_amount_of_inputs_warning(command, 4) is True:
                project_data = uf.add_relationship(project_data, command[1], command[2], command[3])
                print("Created relationship between " +  command[1] + " and " + command[2] + " with type " + command[3])
        case "rmrel":
            if correct_amount_of_inputs_warning(command, 3) is True:
                project_data = uf.delete_relationship(project_data, command[1], command[2])
                print("Removed relationship between class " + command[1] + " and " + command[2])
        case "mkfld":
            #TODO: 
            print("Not yet implemented")
        case "mkmthd":
            #TODO:
            print("Not yet implemented")
        case "save":
            json_write_file(file_path, project_data)
            print("Project Saved")
        case "load":
            if correct_amount_of_inputs_warning(command, 2) is True:
                check_save= input("Would you like to save your current project? (N/y): ")
                check_save.lower()
                if check_save == "y" or check_save == "yes":
                    json_write_file(file_path, project_data)
                project_data = check_file_path(command[1])
        case "lscls":
            classes = json_get_classes(project_data) 
            print(classes)
        case "clsinfo":
            if correct_amount_of_inputs_warning(command, 2) is True:
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
