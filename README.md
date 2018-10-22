# Reviews
Welcome to the Reviews API by Group 3.

## Table of Contents:
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [API Uses](#api-uses)
    * [API GET](#api-get)
         * [Standard](#standard): Return all available ratings using standard API call with GET method.
         * [Specific](#specific): Return a specific rating with GET method.
    * [API POST](#api-post)
    * [API PATCH](#api-patch)
    * [API DELETE](#api-delete)
    * [API ERROR](#api-error)


## Introduction:

## Setup:
The API can be run both locally and in a docker container, though locally requires MySQL installed. It also requires a couple of files which must be manually added for security reasons, like a python configuration file called config.py and an environmental file with secrets.

First of all the repository must be cloned, this can be achived by moving into a workspace with command line and use the following command with git installed:
```git
git clone https://github.com/DAT210/Reviews.git
```
When the repository is successfully cloned it's time to add a couple of configuration files. The structure of the repository will look almost like this:
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
	instance/ <-- must be added
		config.py <-- must be added
```
As one could see the *instance* folder with its content is missing, but could be added manually or else it will be added if one starts the API server.\
The _config.py_ file has the following structure:
```
APP_NAME = 'Review API'
DB_CONFIG = {
    'host': 'mysql',
    'port': 3306,
    'db': 'reviews_db',
    'user': <DB_USER_TO_BE_USED>,
    'pswrd': <DB_USER_PASSWORD_TO_BE_USED>
}
DEBUG = False
SECRET_KEY = <A_BYTE_STRING>
```

## API Uses:
The Reviews API can be reached by sending various request methods to the host of the API server.
To access or send data through the Reviews API one could make calls in the format:
```
	http://host/api/1.0/reviews/
```
Where 'host' is the host address of the API server.

#### API GET:
The GET method of the API request could return two different results depending on the format of the call.

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
	http://host/api/1.0/reviews/<ID>/
```
Where \<ID\> is the ID of the object one wants the rating of. This will return a json in the following format:

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
The POST method of the API request is used for adding a new ID. The request must contain a json in the following format:
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
The PATCH method of the API request is used for updating the rating of an ID. The request must contain a json in the following format:
```
{
  'data': {
    'id': <id_of_the_object>(str),
    'rating': <rating_of_the_object>(int)
  }
}
```
Where \<id_of_the_object\> is the ID of the object being updated, and \<rating_of_the_object\> is the rating being set. Be aware that the rating must be an integer.\
On a successful execution the following json format will be returned:
```
{
  'status': 'success',
  'data': null
}
```

#### API DELETE:
The DELETE method of the API request is used for removing an object and it's rating. It has the same call format as the [specific](#specific) GET call, but with a DELETE method:
```
	http://host/api/1.0/reviews/<ID>/
```
Where \<ID\> is the ID of the object being removed.\
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
