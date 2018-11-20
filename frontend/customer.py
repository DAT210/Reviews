import requests
from flask import request

def get_headers():
    return {"Authorization": request.headers.get("Authorization")}


def get_cid():

    # Sending the get-request with header required
    r = requests.get("192.168.99.100:5052/v1/customer/cid", headers=get_headers())
    
    # If the status code is 500, an error on our part occured
    if r.status() == 500:
        return r.json() # Contains "message" and "error" which tell you what happened

    #If the status code is 4xx, there is no logged in customer or the jwt sent is invalid
    elif r.status() >= 400 and r.status() < 500:
        return "Not logged in or Invalid authentication"
    
    # The message is recieved with every request and tell you what happened
    print(r.json()["message"])
    
    # The cid from the response is gotten like this
    cid = r.json()["cid"]
    return cid