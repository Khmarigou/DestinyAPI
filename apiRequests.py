import requests
from auth import api_key, auth_url, client_id, client_secret
from ResponseAuthClass import authResponse

URL="https://www.bungie.net"

def get(authRessources: authResponse, url) :
    header = {
        "X-API-Key": api_key,
        "Authorization": authRessources.token_type +" " + authRessources.access_token
    }
    r = requests.get(URL + url, headers=header)
    return r.json()