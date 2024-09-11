# This is the file that will be used for programming the interface.

# Command options printed if user inputs "help"
options = '''Options:
    lscls - List all classes and their attributes
    clsinfo [Class] - Provides information on the [Class] 
    lsrel - List all relationships between classes
    help - Displays this information
    exit - Exits the interface'''

# Warns the user that they have to manny arguments
def uneaded_argument_warning(command: list):
    if len(command) > 1: 
        print(command[0] + "does not have options")

print("Enter a command, \nUse \"help\" for information")

# Prompts the user for input
#   DUML stands for Dude UML
user_input = input("DUML:  ")
command = user_input.split()
while command[0] != "exit": # Continues to prompt the user for input until provided "exit"
    match command[0]:
        case "lscls":
            uneaded_argument_warning(command)   
            print("lscls is not yet implemented")
        case "clsinfo":
            if len(command <= 1):
                print("Please provide a valid class to display")
                break
            print("clsinfo is not yet implemented")
        case "lsrel":
            uneaded_argument_warning(command)
            print("lsrel is not yet implemented")
        case "help":
            uneaded_argument_warning(command)
            print(options)
        case _: # Default case if others did not match
            print(command[0] + " is not a command\n\tUse \"help\" for a list of valid commands")
    user_input = input("DUML:  ") 
    command = user_input.split()

# Exits the program
exit(0)
