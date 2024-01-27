from ResponseAuthClass import authResponse
from apiRequests import get
from auth import authentication, refresh_token, write_data, read_data
from CharacterClass import Character
from window import App
from sqlite import *

api_key = "d4b0c71ac32747ce85ab0e7001d5d51a"
auth_url = "https://www.bungie.net/en/OAuth/Authorize"
client_id = "41287"
client_secret = "b.d54tT0NMIAO2dUVRuKlBITgC24hMVj2oEvFH1GJsQ"
URL="https://www.bungie.net"

def getAuthentified():
    try:
        json_object = read_data()
        auth = authResponse(json_object)
    except:
        auth = authentication()
        write_data(auth)
    if auth.isExpired():
        auth = refresh_token(auth)
        write_data(auth)
    return auth

if __name__ == '__main__':
    authRessources = getAuthentified()

    charRessouces = get(authRessources, "/Platform/Destiny2/3/Profile/4611686018483525509/?components=200,201,205")
    character0 = Character(charRessouces, 0)
    character1 = Character(charRessouces, 1)
    character2 = Character(charRessouces, 2)

    app = App()
    app.addCharacter(character0)
    app.addCharacter(character1)
    app.addCharacter(character2)
    app.mainloop()