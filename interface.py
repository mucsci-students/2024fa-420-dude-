# This is the file that will be used for programming the interface.

#pyunit

# Command options printed if user inputs "help"
options = '''Commmands:
    mkcls [Name] : 
        - Creat a new class with [Name]
    rmcls [Class] : 
        - Deletes [Class] 
    chngcls [New Name] [Class] :
        - Rename [Class] with [New Name] 
    mkrel [Class 1] [Class 2] : 
        - Creat a new relationship between [Class 1] and [Class 2]
    rmrel [Class 1] [Class 2] : 
        - Delete a relationship between [Class 1] and [Class 2]
    mkattr [Name] [Class] : 
        - Creat an attribute for [Class] with [Name]
    rmattr [Name] [Class] : 
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

# Warns the user that they have to manny arguments
def uneaded_argument_warning(command: list):
    if len(command) > 1: 
        print(command[0] + " does not have options")

print("Enter a command, \nUse \"help\" for information")

# Prompts the user for input
#   DUML stands for Dude UML
user_input = input("DUML:  ") # Prompts user for input
command = user_input.split()
# Checks for empty user input
if len(command) == 0:
    command = [" "]
# Continues to prompt user for input until the "exit" command is provided
while command[0] != "exit":
    match command[0]:
        case "lscls":
            uneaded_argument_warning(command)   
            print("lscls is not yet implemented")
        case "clsinfo":
            if len(command) <= 1:
                print("Must provide a valid class to display\n\tplease use command: \"help\" for proper use.")
                # Need to implement a print statement if the class provided is not a valid class
                continue
            print("clsinfo is not yet implemented")
        case "lsrel":
            uneaded_argument_warning(command)
            print("lsrel is not yet implemented")
        case "help":
            uneaded_argument_warning(command)
            print(options)
        case "mkcls":
            if len(command) <= 1:
                print("Must provide a valid name\n\tplease use command: \"help\" for proper use.")
                # Need to implement a print statement if the class provided is not a valid class
                continue
            print("mkcls is not yet implemented")
        case "rmcls":
            if len(command) <= 1:
                print("Must provide a valid class name \n\tplease use command: \"help\" for proper use.")
                # Need to implement a print statement if the class provided is not a valid class
                continue
            print("rmcls is not yet implemented")
        case "chngcls":
            if len(command) <= 2:
                print("Must provide a new name and a valid class \n\tplease use command: \"help\" for proper use.")
                # Need to implement a print statement if the class provided is not a valid class
                continue
            print("chngcls is not yet implemented")
        case "mkrel":
            if len(command) <= 2:
                print("Must provide two classes \n\tplease use command: \"help\" for proper use.")
                # Need to implement a print statement if the class provided is not a valid class
                continue
            print("mkrel is not yet implemented")
        case "rmrel":
            if len(command) <= 2:
                print("Must provide two classes \n\tplease use command: \"help\" for proper use.")
                # Need to implement a print statement if the class provided is not a valid class
                continue
            print("rmrel is not yet implemented")
        case "mkattr":
            if len(command) <= 2:
                print("Must provide a name and class\n\tplease use command: \"help\" for proper use.")
                # Need to implement a print statement if the class provided is not a valid class
                continue
            print("mkattr is not yet implemented")
        case "rmattr":
            if len(command) <= 2:
                print("Must provide a name and class\n\tplease use command: \"help\" for proper use.")
                # Need to implement a print statement if the class provided is not a valid class
                continue
            print("rmattr is not yet implemented")
        case "save":
            print("save is not yet implemented")
        case "load":
            print("load is not yet implemented")
        case " ":
            print("Please provide a command")
        case _: # Default case if others did not match
            print(command[0] + " is not a command\n\tUse \"help\" for a list of valid commands")

    user_input = input("DUML:  ") # Prints the prompt again
    # Splits user input and checks for empty input
    command = user_input.split()
    if len(command) == 0:
        command = [" "]

# Exits the program
exit(0)
