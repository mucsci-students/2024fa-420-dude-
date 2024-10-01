# This is the file that will be used for programming the interface.
#maybe use argpars

#pyunit for testing

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
                # add_class(collection, project, command[1]) 
                print("Not implemented")
        case "rmcls":
            if wrong_amount_of_inputs_warning(command, 2) is False:
                #delete_class(collection, project, command[1])
                print("Not implemented")
        case "chngcls":
            if wrong_amount_of_inputs_warning(command, 3) is False:
                # rename_class(collection, project, command[1], command[2])
                print("Not implemented")
        case "mkrel":
            if wrong_amount_of_inputs_warning(command, 4) is False:
                print("Not implemented")
                #add_relationship(collection, project, command[1], command[2], command[3])
        case "rmrel":
            if wrong_amount_of_inputs_warning(command, 4) is False:
                print("Not implemented")
                #delete_relationship(collection, project, command[1], command[2], command[3])
        case "mkattr":
            if wrong_amount_of_inputs_warning(command, 5) is False:
                print("Not implemented")
                #add_attribute(collection, project, command[1], command[2], command[3], command[4])
        case "rmattr":
            if wrong_amount_of_inputs_warning(command, 5) is False:
                print("Not implemented")
                # delete_attribute(collection, project, command[1], command[2], command[3], command[4])
        case "chngattr":
            if wrong_amount_of_inputs_warning(command, 4) is False:
                print("Not implemented")
                #rename_attribute(collection, project, command[1], command[2], command[3])
        case "save":
            print("Not implemented")
        case "load":
            if wrong_amount_of_inputs_warning(command, 2) is False:
                if get_project(collection, command[1]) is None:
                    # print("Project does not exist\n\tContinuing with project " + project)
                    print("Not implemented")
                else :
                    print("Not implemented")
                    # project = command[1]
        case "lscls":
                print("Not implemented")
        case "clsinfo":
            if wrong_amount_of_inputs_warning(command, 2) is False:
                print("Not implemented")
        case "lsrel":
            print("Not implemented")
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
