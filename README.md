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
The API can be run both locally and in a docker container, though locally requires MySQL installed. It also requires an environmental file which must be manually added for security reasons.

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
	config.py
	.env <-- must be added
```
The _.env_ file must be added manually and contains environmental variables for the _docker-compose.yml_ and _config.py_. It's easy to add, just create a new file in the repository and call it _.env_, and then add the follwing lines to it:
```
# Database set-up:
DB_DATABASE=reviews_db
DB_USER=<db_user_to_be_used>
DB_PSWRD=<db_password_to_be_used>
SECRET_KEY=<your_top_secret_key>
```
Just replace _<db_user_to_be_used>_, _<db_password_to_be_used>_, and _<your_top_secret_key>_ with desired username and password for the first two, and some random long string for the ```SECRET_KEY```.

#### Run Flask App:
To run the service locally on ones own computer one has to set a couple of environmentals, and have MySQL installed on the machine. **Be aware that this is for development only!** To set the required environmentals on Windows, open the command line and write the following:
```
set FLASK_APP=reviews:create_app('default')
set FLASK_ENV=development
```
For UNIX and MacOS the following commands are used:
```
export FLASK_APP=reviews:create_app('default')
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
      'description': <description>(str),
      'comments': []
    }]
  }
}
```
If the request was successful the ```'status'``` field of the json reply will be 'success', and the ```'reviews'``` field will contain an array of smaller jsons which contains the ID of the object as a string, the rating of the object as a float, and a description of the object as a string. It will also contain an array of comments if one or more is found, or else will be ```null```.

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
      'name': <name_of_the_object>(str),
      'rating': <rating_of_the_object>(float),
      'review_rating_count': {
      	'1': <nr_of_1_ratings>,
	'2': <nr_of_2_ratings>,
	'3': <nr_of_3_ratings>,
	'4': <nr_of_4_ratings>,
	'5': <nr_of_5_ratings>
      }
      'description': <description>(str),
	'comments_count': <amount_of_comments>,
      'comments': []
    }
  }
}
```
Like the standard the _comments_ field will contain an array if comments are found, elsewise it will be ```null```.
The comments can be ordered by newest and oldest, specify an offset to start at, and the number of comment using the url keys: _sort_, _offset_, and _limit_. Each of the keys have a default value which will be used if none is given, or if wrong type is given. For _sort_ it is ```DESC```, which means descending (newest first); for _offset_ it's ```0```, which means it starts at the first value found; and for _limit_ it's ```10```, which gives the ten first comments found from the offset. The _offset_ and _limit_ keys only take integers, if anything else is given it will use the default value, while _sort_ only takes ```ASC``` or ```DESC``` strings, ```DESC``` will be used if anything else is given.\
Adding a key to the url is simple, just type ```?key=value``` following the _\<ID\>_, and to add multiple keys add a _&_ like: ```?key=value&key2=value2&key3=value3```. For example:
```
http://<host>/api/1.0/reviews/<ID>?sort=ASC&offset=4&limit=14
```
This will sort the comments in ascending order (oldest comments first), and will list 14 comments starting at the 5th (offset+1) found.

#### API POST:
The POST method of the API request is used for adding a new ID, on a successful request the API will return a HTTP status code of 201. The request must contain a json in the following format:
```
{
  'data': [
    {'id':<id_1>, 'name':<name_1>},
    {'id':<id_2>, 'name':<name_2>},
    {'id':<id_3>, 'name':<name_3>},
    ...,
    {'id':<id_n>, 'name':<name_n>},
  ]
}
```
Where the ```'data'``` field contains an array of dictionaries with the ID and name of the objects to be added, if one fail none will be added.\
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
    'rating': <rating_of_the_object>(int),
    'comment': <comment_of_the_rating>
  }
}
```
Where _\<id_of_the_object\>_ is the ID of the object being updated, and _\<rating_of_the_object\>_ is the rating being set. Be aware that the rating **must be an integer**. The _\<comment_of_the_rating\>_ is just a string of maxiumum 50 characters.
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
