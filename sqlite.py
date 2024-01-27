import json
import sqlite3
import requests
import os.path
import glob
from zipfile import ZipFile

test = False
endpointManifest = "https://www.bungie.net/Platform/Destiny2/Manifest/"
api_key = "d4b0c71ac32747ce85ab0e7001d5d51a"


def hashToId(hash):
    id = int(hash)
    if (id & (1 << (32 - 1))) != 0:
        id = id - (1 << 32)
    return id


def getManifest():
    manifest = requests.get(endpointManifest, headers={'X-API-Key': api_key}).json()
    return manifest


def getWorldContent(manifest, lang):
    try:
        mobileWorldContentPaths = manifest['Response']['mobileWorldContentPaths'][lang]
        mobileWorldContentPathsName = mobileWorldContentPaths.split("/")[-1]
        test = os.path.isfile(mobileWorldContentPathsName)
        if not test:
            for f in glob.glob("*.content"):
                os.remove(f)
            print(f"Getting the DataBase in {lang}...")
            database = requests.get("https://www.bungie.net" + mobileWorldContentPaths, headers={'X-API-Key': api_key},
                                    allow_redirects=True)
            open("database.zip", "wb").write(database.content)
            with ZipFile("database.zip", "r") as zipObj:
                # Extract all the contents of zip file in current directory
                zipObj.extractall()
            print("Done !")
            os.remove("database.zip")
        return mobileWorldContentPathsName
    except KeyError:
        print("The language you entered is not available.")
        return None


def connectToDataBase(mobileWorldContentPathsName):
    # Connect to the database
    con = sqlite3.connect(mobileWorldContentPathsName)

    # Get the cursor, which is used to traverse the database, line by line
    cur = con.cursor()
    return cur


def getDataBase(lang):
    manifest = getManifest()
    mobileWorldContentPathsName = getWorldContent(manifest, lang)
    if mobileWorldContentPathsName != None:
        cur = connectToDataBase(mobileWorldContentPathsName)
        return cur
    else:
        return None


def getTableNames(cur):
    res = []
    tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = tables.fetchall()
    for table in tables:
        res.append(table[0])
    return res


def getItem(hash, cur):
    id = hashToId(hash)
    item = cur.execute(f"SELECT json FROM DestinyInventoryItemDefinition WHERE id = {id};")
    return json.loads(item.fetchone()[0])