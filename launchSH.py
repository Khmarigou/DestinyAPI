from api_calls.apiRequests import get
from api_calls.auth import getAuthentified
from config import API_KEY, AUTH_URL, CLIENT_ID, CLIENT_SECRET, BASE_URL

def getStrangeGearInventory(authRessources):
    return get(authRessources, "/Platform/Destiny2/3/Profile/4611686018483525509/Character/2305843009402947802/Vendors/3751514131/?components=402,400,101,401")


if __name__ == '__main__':
    authRessources = getAuthentified()
    strangeGearInventory = getStrangeGearInventory(authRessources)
    print(strangeGearInventory)
    
    # charRessouces = get(authRessources, "/Platform/Destiny2/3/Profile/4611686018483525509/?components=200,201,205")