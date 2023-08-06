
### Step class ###
The Step class consists of common functions that can be inherited by other classes : setTaskID, setUUID, setTaskExecutionID ,startRedisConn ,setLogger ,loadParams ,connectToAPIForKey , create and GetResponseFromURL, getLogger, exceptionTraceback, getRelativeFile.

### Extract class###
The extract class includes an init method that sets all Parameters and log files, as well as a superclass startup that can be defined from the client extract.

### ML class ###
The ML class is made up of an init method that sets all parameters and the log file, as well as a startMLSubscriber method that subscribes to incoming data.

### Transform class ###
The Transform class has an init method that sets all Parameters and the log file. a startTRSubscriber method that subscribes to incoming data.

### Load Class ###
Load class consists of an init method that sets all parameters and the log file, load subscribers to subscribe to incoming data from Redis queue, and client logic; to load final data, it needs to be added to the client load file;

### Connectors Added ###
AzBlob Read (Azure Blob) 
Using this connector, you can read files from AzBlob.
For an Azure Blob Read connection ,create a source folder inside params, and add spec.json with connection configs.

AzBlob Write (Azure Blob)
Using this connector, you can write a file to an AzBlob.
For an Azure Blob Write connection, create a destination folder inside params, and add spec.json with connection configs.

SFTP Read 
This connector is used to read files from an SFTP server.
For an SFTP connection, create a source folder inside params and add spec.json with connection configs.

SFTP Write 
Using this connector, you can read files to an SFTP server for an SFTP write connection,
Create a destination folder inside params and add spec.json with connection configs.

Postgres Read 
This is the Source connector for PostgreSQL databases using SQLAlchemy,
It includes the check() method, which validates the connection to the Postgres database.
The read() method takes an optional query parameter and executes the query on the connected database. discover(): This discover() function is used to discover the tables in the database.

Postgres Write 
Using this connector, you can read files into a Postgres database, consisting of check(),
read() In addition to this, it contains the create_table() function that is used to create a new table in the database.
It compiles the table object provided into a SQL; the alter_table() function is used to alter a table in the database, and the write() function is used to write data to the database.
It takes in the table object and a list of dictionaries.

IPFS source 
You can use this connector to read file from any IPFS http url.
This connector includes a check() function for validating the connection and a read() function for returning data in bytes format.

IPFS destination 
This connector helps you upload any file to a custom IPFS node.
The write() function in this connector uses file and target location as input and will return JSON consisting of contentId, name, and size of the file.
