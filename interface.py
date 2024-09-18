#!/bin/python3
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
    rmrel [Class 1] [Class 2] : 
        - Delete a relationship between [Class 1] and [Class 2]
    mkattr [Class] [Name] [Type] : 
        - Creat an attribute for [Class] with [Name]
    rmattr [Class] [Name] [Type] : 
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
        collection = connect()
        if collection is None:
            print("Invalid login credentials")
            return login_user()
    elif user_input == "2":
        collection = create_collection()
        if  collection is None:
            print("That username already exist")
            return collection
    else :
        login_user()

def load_or_create_project(collection):
    user_input = input("Type load [Project] to open a project or create [Project] to make a new one: ")
    command = user_input.split()
    if len(command) > 2:
        print("Too many arguments, \n\tHint names can't have spaces")
        return load_or_create_project(collection)
    if command[0] == "load":
        return get_project(collection, command[1])
    elif command[0] == "create":
        return add_project(collection, command[0])
    else: 
        return load_or_create_project()



##################  Main Execution Section  ##################

collection = login_user()
data = collection.find_one({"username": "testUser", "password": "testPassword"})
print(data)
# Load or Create Project
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
            if len(command) <= 1:
                print("Must provide a valid name\n\tplease use command: \"help\" for proper use.")
                continue
            add_class(collection, project, command[1]) 
        case "rmcls":
            if len(command) <= 1:
                print("Must provide a valid class name \n\tplease use command: \"help\" for proper use.")
                continue
            delete_class(collection, project, command[1])
        case "chngcls":
            if len(command) <= 2:
                print("Must provide a new name and valid class \n\tplease use command: \"help\" for proper use.")
                continue
            rename_class(collection, project, command[1], command[2])
        case "mkrel":
            if len(command) <= 2:
                print("Must provide two classes \n\tplease use command: \"help\" for proper use.")
                continue
            add_relationship(collection, project, command[1], command[2], command[3])
        case "rmrel":
            if len(command) <= 2:
                print("Must provide two classes \n\tplease use command: \"help\" for proper use.")
                continue
            delete_relationship(collection, project, command[1], command[2], command[3])
        case "mkattr":
            if len(command) <= 2:
                print("Must provide a name and class\n\tplease use command: \"help\" for proper use.")
                continue
            create_attribute(collection, project, command[1], command[2], command[3])
        case "rmattr":
            if len(command) <= 2:
                print("Must provide a name and class\n\tplease use command: \"help\" for proper use.")
                continue
            delete_attribute(collection, project, command[1], command[2], command[3])
        case "save":
            print("save is not yet implemented")
        case "load":
            get_project(command[1], project)
        case "lscls":
            print("lscls is not yet implemented")
        case "clsinfo":
            if len(command) <= 1:
                print("Must provide a valid class to display\n\tplease use command: \"help\" for proper use.")
                continue
            print("clsinfo is not yet implemented")
        case "lsrel":
            print("lsrel is not yet implemented")
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
