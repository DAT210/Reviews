# Reviews
Welcome to the Reviews API by Group 3.

## Table of Contents:
1. [Introduction](#introduction)
2. [Setup and Run](#setup-and-run)
	* [Build Repository](#build-repository)
	* [Add Config](#add-config)
	* [Run Flask App](#run-flask-app)
	* [Run in Docker](#run-in-docker)
3. [API Uses](#api-uses)
    * [API GET](#api-get)
         * [Standard](#standard): Return all available ratings using standard API call with GET method.
         * [Specific](#specific): Return a specific rating with GET method.
    * [API POST](#api-post)
    * [API PATCH](#api-patch)
    * [API DELETE](#api-delete)
    * [API ERROR](#api-error)


## Introduction:

## Setup and Run:
The API can be run both locally and in a docker container, though locally requires MySQL installed. It also requires a couple of files which must be manually added for security reasons, like a python configuration file called config.py and an environmental file with secrets.

#### Build Repository:
First of all the repository must be cloned, this can be achived by moving into a workspace with command line and use the following command with git installed:
```git
git clone https://github.com/DAT210/Reviews.git
```
When the repository is successfully cloned it's time to add a couple of configuration files. 

#### Add Config:
The structure of the repository will look almost like this:
```
/Reviews/
	reviews/
		__init__.py
		api.py
		app.py
		review.py
		db.py
		exceptions.py
	test/
		some test files...
	db/
		init.sql
	Dockerfiles...
	requirements.txt
	setup.py
	.env <-- must be added
	instance/ <-- must be added
		config.py <-- must be added
```
As one can see the *instance* folder with its content is missing, the folder will be automatically created the first time one starts the API, but the _config.py_ file must be added manually.
The _config.py_ file has the following structure:
```python
APP_NAME = 'Review API'
DB_CONFIG = {
    'host': 'mysql',
    'port': 3306,
    'db': 'reviews_db',
    'user': '<DB_USER_TO_BE_USED>',
    'pswrd': '<DB_USER_PASSWORD_TO_BE_USED>'
}
DEBUG = False
SECRET_KEY = <A_BYTE_STRING>
```
Where _<DB_USER_TO_BE_USED>_ is the username the API uses to connect to the MySQL server, and _<DB_USER_PASSWORD_TO_BE_USED>_ is the password. The *SECRET_KEY* is a string of bytes which can be generated by writing the following python script in a command window:
```python
python -c
import os; print(os.urandom(16));
b'_5#y2L"F4Q8z\n\xec]/'
```
Which will print a byte string, copy that and replace _<A_BYTE_STRING>_ with it.
The _.env_ file contains environmental variables for the _docker-compose.yml_ and is easy to add and write the following lines:
```
# Database set-up:
DB_DATABASE=reviews_db
DB_USER=<db_user_to_be_used>
DB_PSWRD=<db_password_to_be_used>
```
Just replace _<db_user_to_be_used>_ and _<db_password_to_be_used>_ with the same values used in the _config.py_ file.

#### Run Flask App:
To run the service locally on ones own computer one has to set a couple of environmentals, and have MySQL installed on the machine. **Be aware that this is for development only!** To set the required environmentals on Windows, open the command line and write the following:
```
set FLASK_APP=reviews:create_app({'DB_CONFIG':{'host':'localhost','user':'root','pswrd':'root','db':'reviews_db','port':3306}})
set FLASK_ENV=development
```
For UNIX and MacOS the following commands are used:
```
export FLASK_APP=reviews:create_app({'DB_CONFIG':{'host':'localhost','user':'root','pswrd':'root','db':'reviews_db','port':3306}})
export FLASK_ENV=development
```
The values of _host_, _user_, _pswrd_, _db_, and _port_ may be changed if other values are required or desired.\
To have the database initialized the following command must be run in python:
```
flask init-db --user <user> --pswrd <password> --host <host>
```
The command arguments can be ignored for the default values, which are ```root``` for user and password, and ```localhost``` for the host.

After initializing the database the local development server can be run by using the following command in python:
```
flask run
```

#### Run in Docker:
To run the API server in Docker is fairly easy as long as one have Docker installed. Just change directory into the _Reviews_ directory and use the following command there:
```
docker-compose up --build
```
This will build a Python and a MySQL image and run them in two different containers, and the database will be initialized on the first build.

## API Uses:
The Reviews API can be reached by sending various request methods to the host of the API server.
To access or send data through the Reviews API one could make calls in the format:
```
	http://<host>/api/1.0/reviews/
```
Where _\<host\>_ is the host address of the API server. e.g. ``` localhost:3000 ``` or ``` 192.168.99.100:3000 ```.

#### API GET:
The GET method of the API request could return two different results depending on the format of the call, but will always return a HTTP status code of 200 on a successful request.

###### Standard:
The standard format will pull all available reviews from the server in the following json format:
```
{
  'status': 'success',
  'data':{
    'reviews':[{
      'id': <id_of_the_object>(str),
      'rating': <rating_of_the_object>(float),
      'description': <description>(str)
    }]
  }
}
```
If the request was successful the ```'status'``` field of the json reply will be 'success', and the ```'reviews'``` field will contain an array of smaller jsons which contains the ID of the object as a string, the rating of the object as a float, and a description of the object as a string.

###### Specific:
The specific format will only get the rating of a specified ID, and to do this the following call is made with a GET method:
```
	http://<host>/api/1.0/reviews/<ID>/
```
Where _\<ID\>_ is the ID of the object one wants the rating of. This will return a json in the following format:

```
{
  'status': 'success',
  'data': {
    'review': {
      'id': <id_of_the_object>(str),
      'rating': <rating_of_the_object>(float),
      'description': <description>(str)
    }
  }
}
```

#### API POST:
The POST method of the API request is used for adding a new ID, on a successful request the API will return a HTTP status code of 201. The request must contain a json in the following format:
```
{
  'data': [
    <id_1>,
    <id_2>,
    <id_3>,
    ...,
    <id_n>
  ]
}
```
Where the ```'data'``` field contains an array of ID's to be added, if one fail none will be added.\
Returns the following json format on success:
```
{
  'status': 'success',
  'data': null
}
```

#### API PATCH:
The PATCH method of the API request is used for updating the rating of an ID, on a successful request the API will return a HTTP status code of 200. The request must contain a json in the following format:
```
{
  'data': {
    'id': <id_of_the_object>(str),
    'rating': <rating_of_the_object>(int)
  }
}
```
Where _\<id_of_the_object\>_ is the ID of the object being updated, and _\<rating_of_the_object\>_ is the rating being set. Be aware that the rating must be an integer.\
On a successful execution the following json format will be returned:
```
{
  'status': 'success',
  'data': null
}
```

#### API DELETE:
The DELETE method of the API request is used for removing an object and it's rating, on a successful deletion the API will return a HTTP status code of 200. It has the same call format as the [specific](#specific) GET call, but with a DELETE method:
```
	http://<host>/api/1.0/reviews/<ID>/
```
Where _\<ID\>_ is the ID of the object being removed.\
On a successful execution the following json format will be returned:
```
{
  'status': 'success',
  'data': null
}
```

#### API ERROR:
Whenever a failure or error occour an API Error will be raised, this can easily be detected by checking the ```'status'``` field of the json response, if the field is 'error' instead of 'success' this will be the format of the json response:
```
{
  'status': 'error',
  'data': {
    'error': {
      'code': <error_code>,
      'message': <error_message>,
      'type': <error_type>
    }
  }
}
```
The _\<error_code\>_ will be the same code as the HTTP status code, which will either be 400 if it's a 'Bad Request', 404 if it's 'Not Found', and a 409 if there's a 'Conflict'.
