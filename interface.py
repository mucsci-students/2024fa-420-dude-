# This is the file that will be used for programming the interface.
#maybe use argpars

# import pymongo
from MongoFunctions import * 
from Utility_Functions import *

#pyunit

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
    rmrel [Type] [Class 1] [Class 2] : 
        - Delete a relationship between [Class 1] and [Class 2]
        - Type must be of Aggregation or Composition
    mkattr [Class] [Name] [Type] [Value] : 
        - Create an attribute for [Class] with [Name]
    rmattr [Class] [Name] [Type] [Value] : 
        - Delete an attribute with [Name] from [Class]
    chngattr [Class] [Attribute Name] [New Attribute Name] :
        - Rename the attribute with [Attribute Name] from [Class] with [New Attribute Name]
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

def login_user():
    print("Use \"1\" to sign in or \"2\" to create an account.")
    user_input = input("DUML: ")
    if user_input == "1":
        collection = MongoFunctions.connect()
        if collection is None:
            print("Invalid login credentials")
            return login_user()
        return collection
    elif user_input == "2":
        collection = MongoFunctions.create_collection()
        if  collection is None:
            print("That username already exist")
            return collection
    else :
        return login_user()

def load_or_create_project(collection):
    user_input = input("Type load [Project] to open a project or create [Project] to make a new one: ")
    command = user_input.split()
    if command == None:
        return load_or_create_project(collection)
    if len(command) > 2:
        print("Too many arguments, \n\tHint names can't have spaces")
        return load_or_create_project(collection)
    if len(command) < 2:
        print("You must provide a name for the project you wish to load or creat.")
        return load_or_create_project(collection)
    if command[0] == "load":
        data = get_project(collection, command[1])
        if data == None:
            print("Project does not exist")
            return load_or_create_project(collection)
        else :
            return command[1]
    elif command[0] == "create":
        data = add_project(collection, command[1])
        return command[1]
    else: 
        return load_or_create_project(collection)

def list_object(string_data) :
    split_on_attributes = string_data.split("{") # Checks if the class has attributes
    if len(split_on_attributes) == 2: # If it does not do this section
        chuncks = string_data.split(",") # Splits the object into its peices
        # Prints each peice of the object on its own line
        for i in range(len(chuncks)) :
        # Removes the "}" from the end so it can be printed on its on line
            if i == len(chuncks) - 1: 
                remaining_string = chuncks[i]
                print(remaining_string[:-1])
                print("}")
            elif i == 0:
                # Removes the "{" from the beggining so that it can be printed on its own line
                beggining_string = chuncks[i] 
                print("{")
                print(beggining_string[1:])
            else :
                print(chuncks[i] + ",") # Prints each section with a comma at the end.
    else : # If there are attributes do this section
        # Prints everything before the attributes
        paired_beggining_chunks = split_on_attributes[1].split(",")
        print("{") 
        amount_of_chuncks = len(paired_beggining_chunks)
        for i in range(amount_of_chuncks):
            if i == amount_of_chuncks - 1:
                print(paired_beggining_chunks[i])
            else :
                print(paired_beggining_chunks[i] + ",")

        # Prints everything after the attributes
        for i in range(len(split_on_attributes) - 2):

            paired_end_chunks = split_on_attributes[i + 2].split(",")
            print("    {")
            amount_of_chuncks = len(paired_end_chunks)
            for i in range(amount_of_chuncks):
                if i != amount_of_chuncks -1:
                    print("\t" + paired_end_chunks[i] + ",")
                    if i is len(split_on_attributes) - 1:
                        string_of_last_chunk = paired_end_chunks[i]
                        print("\t" + string_of_last_chunk[:-3])
                else:
                    print("\t" + paired_end_chunks[i]) # Prints the last attribute
                    print("    }")
        print("  ]\n}")
    
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

collection = login_user()

project = load_or_create_project(collection)

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
                add_class(collection, project, command[1]) 
        case "rmcls":
            if wrong_amount_of_inputs_warning(command, 2) is False:
                delete_class(collection, project, command[1])
        case "chngcls":
            if wrong_amount_of_inputs_warning(command, 3) is False:
                rename_class(collection, project, command[1], command[2])
        case "mkrel":
            if wrong_amount_of_inputs_warning(command, 4) is False:
                add_relationship(collection, project, command[1], command[2], command[3])
        case "rmrel":
            if wrong_amount_of_inputs_warning(command, 4) is False:
                delete_relationship(collection, project, command[1], command[2], command[3])
        case "mkattr":
            if wrong_amount_of_inputs_warning(command, 5) is False:
                add_attribute(collection, project, command[1], command[2], command[3], command[4])
        case "rmattr":
            if wrong_amount_of_inputs_warning(command, 5) is False:
                delete_attribute(collection, project, command[1], command[2], command[3], command[4])
        case "chngattr":
            if wrong_amount_of_inputs_warning(command, 4) is False:
                rename_attribute(collection, project, command[1], command[2], command[3])
        case "save":
            print("Project is saved")
        case "load":
            if wrong_amount_of_inputs_warning(command, 2) is False:
                if get_project(collection, command[1]) is None:
                    print("Project does not exist\n\tContinuing with project " + project)
                else :
                    project = command[1]
        case "lscls":
            data = list_classes(collection, project)
            for objects in data:
                string_data = str(objects)
                # print(string_data)
                list_object(string_data)
        case "clsinfo":
            if wrong_amount_of_inputs_warning(command, 2) is False:
                data = get_class(collection, project, command[1])
                string_data = str(data)
                # print(string_data)
                list_object(string_data)
        case "lsrel":
            data = list_relationships(collection, project)
            for objects in data:
                string_data = str(objects)
                list_object(string_data)
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