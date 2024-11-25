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
pip install readline (linux)
pip install pyreadline (windows)
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

Null:
    We use the python version of a Null object (aka None) when querying the backend for
certain data. If there is some type of error in doing so or the object does not exists,
the backend functions will return the None object and the control and view can handle
that as necessary.

Command:
    We use the command design pattern in both versions of the view. For the CLI, it
takes the command and turns it into an array object with each token. The CLI then parses
that array to run each command. The GUI breaks each command into buttons that invoke a
callback function when clicked, which then goes through each step to get data from the
user and execute the command the user enacted.
```

