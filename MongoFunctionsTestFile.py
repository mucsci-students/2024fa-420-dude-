import MongoFunctions

# Test connecting to the database
collection = MongoFunctions.connect()
if collection is None:
    print("Incorrect username or password.")
    exit()
else:
    print("Welcome to the UML Editor!")

exit = False
while not exit:
      print("What would you like to do?\nCreate a new class => C\nCreate a new relationship => R\nCreate a new attribute\nQuit => Q")
      choice = input()
      match choice:
            case "C":
                MongoFunctions.create_class(collection, class_data)
            case "R":
                MongoFunctions.create_relationship(collection, relationship_data)
            case "A":
                MongoFunctions.create_attribute(collection, attribute_data)
            case "Q":
                exit = True
 


    



