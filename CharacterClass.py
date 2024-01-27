

class Character ():
    def __init__(self, charRessouces, number):
        self.id = list(charRessouces.get("Response").get("characters").get("data").keys())[number]
        self.light = charRessouces.get("Response").get("characters").get("data").get(self.id).get("light")
        self.classHash = charRessouces.get("Response").get("characters").get("data").get(self.id).get("classHash")
        self.emblemPath = charRessouces.get("Response").get("characters").get("data").get(self.id).get("emblemPath")
        self.emblemBackgroundPath = charRessouces.get("Response").get("characters").get("data").get(self.id).get("emblemBackgroundPath")
        self.dateLastPlayed = charRessouces.get("Response").get("characters").get("data").get(self.id).get("dateLastPlayed")
        self.minutesPlayedThisSession = charRessouces.get("Response").get("characters").get("data").get(self.id).get("minutesPlayedThisSession")
        self.inventory = charRessouces.get("Response").get("characterInventories").get("data").get(self.id)
        self.equipement = charRessouces.get("Response").get("characterEquipment").get("data").get(self.id)

    def __getitem__(self, item):
        if item == "id":
            return self.id
        elif item == "light":
            return self.light
        elif item == "classHash":
            return self.classHash
        elif item == "emblemPath":
            return self.emblemPath
        elif item == "emblemBackgroundPath":
            return self.emblemBackgroundPath
        elif item == "dateLastPlayed":
            return self.dateLastPlayed
        elif item == "minutesPlayedThisSession":
            return self.minutesPlayedThisSession
        elif item == "inventory":
            return self.inventory
        elif item == "equipement":
            return self.equipement

    def getItems (self):
        return self.inventory.get("items")

    def getEquipement (self):
        return self.equipement.get("items")
