import requests
from config import API_KEY
from api_calls.AuthResponseClass import AuthResponse

URL="https://www.bungie.net"

def get(authRessources: AuthResponse, url) :
    header = {
        "X-API-Key": API_KEY,
        "Authorization": authRessources.token_type +" " + authRessources.access_token
    }
    r = requests.get(URL + url, headers=header)
    return r.json()