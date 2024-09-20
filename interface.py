# This is the file that will be used for programming the interface.
#maybe use argpars

import pymongo
from MongoFunctions import * 
from Utility_Functions import *

#pyunit

# Command options printed if user inputs "help"
options = '''Commmands:
    mkcls [Name] : 
        - Creat a new class with [Name]
    rmcls [Class] : 
        - Deletes [Class] 
    chngcls [Class] [New Name] :
        - Rename [Class] with [New Name] 
    mkrel [Type] [Class 1] [Class 2] : 
        - Creat a new relationship between [Class 1] and [Class 2]
        - Type must be of Aggregation or Composition
    rmrel [Type] [Class 1] [Class 2] : 
        - Delete a relationship between [Class 1] and [Class 2]
        - Type must be of Aggregation or Composition
    mkattr [Class] [Name] [Type] [Value] : 
        - Creat an attribute for [Class] with [Name]
    rmattr [Class] [Name] [Type] [Value] : 
        - Delete an attribute with [Name] from [Class]
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

def load_or_create_project(collection, command):
    # Make sure to add checks to other parts too.
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
            user_input = input("Type load [Project] to open a project or create [Project] to make a new one: ")
            command = user_input.split()
            return load_or_create_project(collection, command)
        else :
            return command[1]
    elif command[0] == "create":
        data = add_project(collection, command[1])
        return command[1]
    else: 
        user_input = input("Type load [Project] to open a project or create [Project] to make a new one: ")
        command = user_input.split()
        return load_or_create_project(collection, command)

def display_class(string_data) :
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
        paird_beggining_chunks = split_on_attributes[1].split(",")
        print("{") 
        amount_of_chuncks = len(paird_beggining_chunks)
        for i in range(amount_of_chuncks):
            if i == amount_of_chuncks - 1:
                print(paird_beggining_chunks[i])
            else :
                print(paird_beggining_chunks[i] + ",")

        # Prints everything after the attributes
        paired_end_chunks = split_on_attributes[2].split(",")
        print("    {")
        amount_of_chuncks = len(paired_end_chunks)
        for i in range(amount_of_chuncks):
            if i != amount_of_chuncks -1:
                print("\t" + paired_end_chunks[i] + ",")
            else:
                print("\t" + paired_end_chunks[i]) # Prints the last attribute
                print("    }")
                print("  ]\n}")



##################  Main Execution Section  ##################

collection = login_user()

user_input = input("Type load [Project] to open a project or create [Project] to make a new one: ")
command = user_input.split()
project = load_or_create_project(collection, command)

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
            if len(command) <= 1:
                print("Must provide a valid name\n\tplease use command: \"help\" for proper use.")
            else: 
                add_class(collection, project, command[1]) 
        case "rmcls":
            if len(command) <= 1:
                print("Must provide a valid class name \n\tplease use command: \"help\" for proper use.")
            else:
                delete_class(collection, project, command[1])
        case "chngcls":
            if len(command) <= 2:
                print("Must provide a new name and valid class \n\tplease use command: \"help\" for proper use.")
            else: 
                rename_class(collection, project, command[1], command[2])
        case "mkrel":
            if len(command) <= 2:
                print("Must provide two classes \n\tplease use command: \"help\" for proper use.")
            else:
                add_relationship(collection, project, command[1], command[2], command[3])
        case "rmrel":
            if len(command) <= 2:
                print("Must provide two classes \n\tplease use command: \"help\" for proper use.")
            else: 
                delete_relationship(collection, project, command[1], command[2], command[3])
        case "mkattr":
            if len(command) <= 2:
                print("Must provide a name and class\n\tplease use command: \"help\" for proper use.")
            else:
                add_attribute(collection, project, command[1], command[2], command[3], command[4])
        case "rmattr":
            if len(command) <= 2:
                print("Must provide a name and class\n\tplease use command: \"help\" for proper use.")
            else: 
                delete_attribute(collection, project, command[1], command[2], command[3], command[4])
        case "save":
            print("Project is saved")
        case "load":
            project = get_project(collection, command[1])
        case "lscls":
            data = list_classes(collection, project)
            for objects in data:
                string_data = str(objects)
                display_class(string_data)
                
        case "clsinfo":
            if len(command) <= 1:
                print("Must provide a valid class to display\n\tplease use command: \"help\" for proper use.")
            else:
                data = list_classes(collection, project)
                string_data = str(data)
                display_class(string_data)
        case "lsrel":
            data = list_relationships(collection, project)
            for objects in data:
                print("\t\t" + str(objects))
        case "help":
            print(options)
        case " ":
            print("Please provide a command")
        case _: # Default case if others did not match
            print(command[0] + " is not a command\n\tUse \"help\" for a list of valid commands")

    user_input = input("DUML: ") # Prints the prompt again
    # Splits user input and checks for empty input
    command = user_input.split()
    if len(command) == 0:
        command = [" "]

# Exits the program
exit(0)
