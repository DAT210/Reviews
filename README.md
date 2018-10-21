# Reviews
Welcome to the Reviews API by Group 3.

## Table of Contents:
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [API Uses](#api-uses)
    * [API GET](#api-get)
    * [API POST](#api-post)
    * [API PATCH](#api-patch)
    * [API DELETE](#api-delete)
    * [API ERROR](#api-error)


## Introduction:

## Setup:

## API Uses:
The Reviews API can be reached by sending various request methods to the host of the API server.
To access or send data through the Reviews API one could make calls in the format:
```
http://host/api/1.0/reviews/
```
Where 'host' is the host address of the API server.

#### API GET:
The GET method of the API request could return two different results depending on the format of the call.

Standard:\
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

Specific:\
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

#### API PATCH:

#### API DELETE:

#### API ERROR:
