# 2024fa-420-dude$
Senior Capstone Project for fall 24 CSCI 420 by Hunter Weaver, Derrick Boyer, and Ty Reynolds. UML Editor

### Using the Dudes UML Editor
The editor uses a files formated with json to store data for each project. When launching the program, the user can use "python3 View/dude.py --cli" to use the command line interface or can run it without the --cli flag to use the graphical user interface. When launching a program you can either load a prexisting project or create a new one. Either way you though you must supply a file path that you wish to use for the project. 

A project consist of classes which have fields and parameters as well as relationships that connect classes.

In the CLI a Class will be structured like the following:
    ```
    Class Name: 
    Tire
    Fields:
    diameter
    psi
    brand
    Methods:
    setPSI(new_psi)
    ```
    ```
    Relationship Data:
    Source: Tire
    Destination: Car
    Type: Composition
    ```

### Testing 
All unit and integration tests are run using the pytest python testing framework. There are unit tests for the backend database functions in the Model folder and unit/integration tests for the API in the Control folder. The files can be run separately using:
```pytest <filename>```
They can also be run simultaneously using the more broad TestFile.py that sits above the rest of the project filesystem. That program takes a command argument and runs both test files and displays corresponding output for each. It can be run using:
```
Windows:
    python TestFile.py --test
Linux:
    python3 TestFile.py --test
```
There is also a known bug where the database tests fail on the first run of the broad test file but work on every subsequent run.

### Requirements/Dependencies
The only necessary libraries are the standard python json library which is usually included with initial python installation, the pytest library which is used for all unit/integration tests, PyQt5 for the GUI, and the readline library for tab completion in the CLI. They can be installed using the following commands:
```
pip install json
```
```
pip install pytest
```
```
pip install PyQt5
```
```
pip install readline (Linux)
pip install pyreadline3 (Windows)  
```

### Design Patterns
Below are the design patterns we used for this project:
```
Model, View, Controller (MVC):
    We use the MVC design pattern to organize our project into the 3 distinct aspects:
The model, which deals directly with the backend and handles reading and writing data,
the view, which deals with presenting the data to the user and allowing the user to
interact with the data, and the controller/API that works as a middleman to format the
inputs and outputs for both ends.

Memento:
    We use memento to implement to undo and redo functions for the CLI and GUI. By
using memento, we are able to save previous program states in and undo and redo stack
and push and pop those states as necessary.

Observer:
    We use the observer design pattern for updating when a class box is moved in the
GUI. We created an observer to watch for when a class box is moved so it can update the
relationship line accordingly.

Command:
    We use the command design pattern in both versions of the view. For the CLI, it
takes the command and turns it into an array object with each token. The CLI then parses
that array to run each command. The GUI breaks each command into buttons that invoke a
callback function when clicked, which then goes through each step to get data from the
user and execute the command the user enacted.

Iterator:
    We use the iterator design pattern to iterate through all of relationship data
whenever we need to print out the relationships for the CLI. We created an
iterator object that has a next function and something that allows you to access 
the data that it is currently pointing at. Doing so allows us to abstract the access
and iteration through the data.

Chain of Responsibility:
    We use the chain of responsibility design pattern for essentially every function
our program offers. The view will take in the request and do some processing, where it
will then pass the main project data to the appropriate API function, along with any
necessary data, where the API will do the checks for edge cases and errors that may occur,
which then passes the request and data to the appropriate backend function, where the
command is processed/fails and an appropriate return value is passed back up the chain.
This allows the different parts of the "chain" to have a different responsibility depending on
the state of the program, and each part handles something that the others don't The view
handles command processing and data input/output, the controller handles edge/error cases and
communication between the view and model, and the model handles basic format checks and data
reading/writing. By dividing up these responsibilities into different parts, we can better
diagnose/pinpoint bugs in our program.
```

