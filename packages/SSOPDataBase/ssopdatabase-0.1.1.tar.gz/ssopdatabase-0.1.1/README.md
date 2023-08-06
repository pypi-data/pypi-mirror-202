Read Me File


How does this library works?

#
In the library there are 3 types of folders:

- The "g" type
- The "s" type
- The "w" type

#
Brief Explanation:


    The "g" files are files that are the gateway to the database itself. These files helps us to make use of the database as simple as possible. These type of files include one file which is the "gCentralCompenent" and, as the name suggests, is the center of all of the operation in the database and access to it.
    
    The "s" files are the struture and architecture of each of the tables of the database, for example, sMeasure and sService arbitrage. In these files, there are fucntions to access the small tables for each "dataType".

    The "w" files, the last type, is for web files. These type of files are the gateway to access and write in the database through the help of the Flask library. With these files, we can write, read and manipulate data from the database using the application layer protocol (get, post, put, delete, ...).





#
The "g" files:

    gBaseDB:

    This file has the code to implement and create the database. Its only funtion is to create the data base and the architecture

    gCentralComponent:

    This is the cerebro or the brain of all of the action. This file is the most important file of all.

    This file is compost out of 5 blocks:

        1- The imports and data types
        2- The Strucutre of the main table (this table have the information of all tables) 
        3- The List functions
        4- The manipulate functions
        5- And the new Information funtions


    1) First, it is imported the files to have access to the other tables and the functions to use it. The it has a list of dataTypes that are available to use. 

    2) Second tge declaration of tha main table. It has the follwing data

        id = Column(Integer, primary_key=True)
        topic = Column(String)
        iotDeviceID = Column(String)
        dataType = Column(String)

        id - Every record or row in the table has its id. This is how the table controls all the flow of information

        topic - this information should be blank if it was sent throught the internet protocol but it is automatically filled if it was recived through mqtt because every information is sent linked to a topic

        iotDeviceID - this is the id of the "person" or device who is sending the information. It should be unique for every person

        dataType -  is the the name of the table that the information should be write on

        dataTypesAvailable = [
            "bessMeasurementData",
            "bessSetPointDataDB",
            "measurementData",
            "pVGeneratorData",
            "pVGeneratorSetPoint",
            "serviceArbitrage",
            "ServicePeakShaving",
            "serviceSelfConsumption",
            "inverterData",
                   ]

    3) The list functions, includes to gather all information by ID, by topic or all the information 

    4) These block has 3 main functions:

        - deleteEntryByID which deletes rows, giving an ID
        - Tranforms the entry/row into a dictionary form
        - Tranforms a group of rows into a dictionary form
        
        WARNING: If it is more than one row or a list of one element, IT HAS to be used the table2dict fucntion instead of the row2dict function

    5) This function is used to create a new entry in the main table and this fucntion is in charge of forward the information to the correct table. 
    It has to be given a topic (even if there is blank), and ID, a dataType that is in the dataTypes availables and the data in the correct format.

    This format is decrbied in  another document

#
The "s" files:

This files are not to be used directly.

They store and manipulate the information of each table that is related to the each table

#
The "w" files:

As mentioned above this files are the gateway of the database. It can be access through the internet.

To run the the server thorught the RESTFul, we need to run the funciton launchDataBase()

To run throught MQTT, we need to run the laucnhMQTT()

Then, everytime someone publishes a message, it automatically saves in the server's database. 

Everytime someone POST or GET thourght an URL available, it saves info in the database or retrieve data from the database (so far):


URL's Available:

GATEDATASERVICE = "http://localhost:8000" is the Base URL

then we add /info/example to get have access to the funtions
we get

http://localhost:8000/info/example




routes available:



/API/data
Methods: [GET,POST] 

Description: If Get, ir returns all the information in the central database
If POST, reads the information in the body and creates a record of that data (creates a row in the database) 


/API/data/ID/<path:dataID>
Methods: [GET] 

Description: Gets a specific row with that id

Example: /API/data/ID/4 gives the data realted to the entry with 4 as an ID



/API/data/dataType/<path:dataType>
Methods: [GET] 

Description: Gets all the records within that dataType. It returns a dictionary with all the information
