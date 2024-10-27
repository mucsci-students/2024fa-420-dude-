# 2024fa-420-dude$
Senior Capstone Project for fall 24 CSCI 420 by Hunter Weaver, Derrick Boyer, and Ty Reynolds. UML Editor

### Using the Dudes UML Editor
The editor uses a files formated with json to store data for each project. When launching the program, the user can use "python3 duml --cli" to use the command line interface or can run it without the --cli flag to use the graphical user interface. When launching a program you can either load a prexisting project or create a new one. Either way you though you must supply a file path that you wish to use for the project. 

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

    Relationship Data:
    Source: Tire
    Destination: Car
    Type: Composition
    ```

### Testing 
All unit and integration tests are run using the pytest python testing framework. There are unit tests for the backend database functions in the Model folder and unit/integration tests for the API in the Control folder. The files can be run separately using:
```pytest <filename>```
They can also be run simultaneously using the more broad TestFile.py that sits above the rest of the project filesystem. That program takes a command argument and runs both test files and displays corresponding output for each. It can be run using:
```Windows:
        python TestFile.py --test
   Linix:
        python3 TestFile.py --test```
There is also a known bug where the database tests fail on the first run of the broad test file but work on every subsequent run.

### Requirements
The only necessary libraries are the standard python json library which is usually included with initial python installation, and the pytest library which is used for all unit/integration tests. They can be installed using the following commands:
```pip install json```
```pip install pytest```
