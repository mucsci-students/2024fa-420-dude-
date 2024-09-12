# 2024fa-420-dude$
    Senior Capstone Project for fall 24 CSCI 420 by Hunter Weaver, Derrick Boyer, and Ty Reynolds. UML Editor

    # Database Configuration and Setup
        The editor uses a MongoDB cloud cluster database to store data for each user. Each user has their own collection within the main UML Database. The user will be given login credentials that are used when the program is launched to connect to their specific collection of data. Each collection is made up of 5 various JSON objects:
            1. Project Objects for saving/loading specific projects
            2. Class Objects for storing info on specific classes
            3. Relationship Objects for storing relationships between classes
            4. Attribute Objects that are stored within class objects to store attribute data for classes
            5. 1 Authorization Object per collection to ensure that the correct username/password combination was used to login to the program.
        The only thing database specific thing needed to run the program is the MongoDB Python library which can be installed with the following shell script:
            pip install pymongo