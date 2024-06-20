import json
import requests
import base64
import webbrowser
from api_calls.AuthResponseClass import AuthResponse
from config import AUTH_URL, CLIENT_ID, CLIENT_SECRET
from api_calls.apiRequests import get

def authentication() :
    '''
    This function is used to authenticate the user and get the access token.
    Open the browser to authenticate the user and get the code.
    Then, use the code to get the access token.
    Return the authResponse from the server.
    '''
    url = AUTH_URL + "?client_id=" + CLIENT_ID + "&response_type=code"
    print("Open the browser to authenticate the user : " + url)
    webbrowser.open(url)

    code = input("code : ")
    token_url = "https://www.bungie.net/platform/app/oauth/token/"
    data = {
        "grant_type": "authorization_code",
        "code": code
    }
    base64client = base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, "utf-8"))
    header = {
        "Authorization": "Basic " + str(base64client, "utf-8"),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post(token_url, data=data, headers=header)
    return AuthResponse(r.json())

def getAuthentified():
    '''
    This function is used to get the authentification.
    If the authentification is already done, read the authResponse from the file.
    If the authentification is not done, do the authentification.
    If the authentification is expired, refresh the token.
    Return the authResponse.
    '''
    try:
        auth_data_json = read_data_auth()
        # Create an object AuthResponse from the json object
        auth = AuthResponse(auth_data_json)
        print("Authentification already done")
    except:
        print("Authentification needed")
        auth = authentication()
        write_data_auth(auth)
    if auth.isRereshExpired():
        print("Refresh token expired")
        auth = authentication()
        write_data_auth(auth)
    elif auth.isExpired():
        print("Token expired")
        auth = refresh_token(auth)
        write_data_auth(auth)
    gettingUserInfo(auth)
    return auth

def gettingUserInfo(auth):
    '''
    This function is used to get the user info like membershipId, membershipType displayName...
    '''
    userInfo = get(auth, "/Platform/User/GetMembershipsForCurrentUser/")
    destinyinfo = userInfo["Response"]["destinyMemberships"][0]
    auth.membership_id = destinyinfo["membershipId"]
    auth.membership_type = destinyinfo["membershipType"]
    auth.display_name = destinyinfo["displayName"]
    auth.bungieGlobalDisplayNameCode = destinyinfo["bungieGlobalDisplayNameCode"]


def refresh_token(auth) :
    token = auth.refresh_token
    token_url = "https://www.bungie.net/platform/app/oauth/token/"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": token
    }
    base64client = base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, "utf-8"))
    header = {
        "Authorization": "Basic " + str(base64client, "utf-8"),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post(token_url, data=data, headers=header)
    return AuthResponse(r.json())


def write_data_auth(auth):
    '''
    Write the authResponse in the file authResponse.json.
    '''
    with open("authResponse.json", "w") as outfile:
        outfile.write(auth.toJson())

def read_data_auth():
    '''
    Read the datas from the file authResponse.json to see if we need to do an authentification or not.
    Return the json object.
    '''
    with open("authResponse.json", "r") as openfile:
        json_object = json.load(openfile)
    return json_object