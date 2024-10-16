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
In order to run the testing functions you must use pytest in each of the directories. Pytest can be installed with pip/pip3(on linux) pytest. These test files refer to the sprint format. These test file modify and/or create new files so make sure these changes are reversed before re-running the test files.

### Requirements
pip/pip3(Linux) PyQt5
