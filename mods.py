import requests, json, time
from utils import *

database_list = []
try:
    with open("vdatabase.json", "r", encoding = "UTF-8") as f:
        database_list = json.load(f)
except:
    print("meow")
mods = set()
database = {}
for mod in database_list:
    mod["game_amount"] = 0
    mods.add(mod["id"])
    database[mod["id"]] = mod
database_list = None
offset = 0
size = 50
while True:
    try:
        games = doARequest(f"games?offset={offset}&max={size}&embed=moderators", mute_exceptions=False)
        games = games.get("data",[])
        for game in games:
            game_id = game.get("id","")
            print(f"Games fetched: {offset}")
            json.dump(game, open(f"outputs/games/{game_id}.json", "w"))
            for mod in game.get("moderators",{}).get("data",[]):
                modID = mod.get("id","")
                if not modID: continue
                if modID in mods:
                    database[modID]["game_amount"] += 1
                    continue
                mods.add(modID)
                json.dump(mod, open(f"outputs/mods/{modID}.json", "w"))
                if mod["location"] == None:
                    flag = ":united_nations:"
                else:
                    flag = f':flag_{mod["location"]["country"]["code"][:2]}:'
                name = mod["names"]["international"]
                print(f'{modID} : {name}, {flag}, 1', offset)
                database[modID] = {
                    "id": modID,
                    "name": name,
                    "flag": flag,
                    "game_amount": 1
                }
        offset += size
        if len(games) < size:
            break
    except Exception as e:
        print(e)
        continue

database_list = list(database.values())

with open("vdatabase.json", "w", encoding="UTF-8") as vd:
    vd.truncate(0)
    vd.writelines(json.dumps(database_list))
