import json
import requests
import base64
from ResponseAuthClass import authResponse

api_key = "d4b0c71ac32747ce85ab0e7001d5d51a"
auth_url = "https://www.bungie.net/en/OAuth/Authorize"
client_id = "41287"
client_secret = "b.d54tT0NMIAO2dUVRuKlBITgC24hMVj2oEvFH1GJsQ"

def authentication() :
    url = auth_url + "?client_id=" + client_id + "&response_type=code"
    print(url)

    code = input("code : ")
    token_url = "https://www.bungie.net/platform/app/oauth/token/"
    data = {
        "grant_type": "authorization_code",
        "code": code
    }
    base64client = base64.b64encode(bytes(client_id + ":" + client_secret, "utf-8"))
    header = {
        "Authorization": "Basic " + str(base64client, "utf-8"),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post(token_url, data=data, headers=header)
    return authResponse(r.json())

def refresh_token(auth) :
    token = auth.refresh_token
    token_url = "https://www.bungie.net/platform/app/oauth/token/"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": token
    }
    base64client = base64.b64encode(bytes(client_id + ":" + client_secret, "utf-8"))
    header = {
        "Authorization": "Basic " + str(base64client, "utf-8"),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post(token_url, data=data, headers=header)
    return authResponse(r.json())


def write_data(auth):
    with open("authResponse.json", "w") as outfile:
        outfile.write(auth.toJson())

def read_data():
    with open("authResponse.json", "r") as openfile:
        json_object = json.load(openfile)
    return json_object