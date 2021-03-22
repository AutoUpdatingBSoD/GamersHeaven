import json
import csv
import pandas as pd
import requests
from pathlib import Path
import os
icounter = 0

path = "C:/users/unrea/Desktop/"
SteamAppDB = pd.read_json(r""+path+"SteamApps.json")
base_url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=HAHAHAHEATITHACKERS&format=json&plain="
dirlist = os.listdir()
urltail="shop=steam&region=us"
resetIndex = 20000
def catchExceptionLoop(resetIndex, icounter, path, SteamAppDB):
    for index, row in SteamAppDB.iterrows():
        if icounter >= resetIndex:
            truth = True
            name = str(index).strip("app")
            counter = 0
            cursor = ""
            lastcursor = ""
            os.mkdir(""+path+"/reviewresponses/"+name)
            url = base_url+row.data+urltail
            response = requests.get(url)
            json_file = response.json()
            counter = counter + 1
            f = open(r""+path+"/reviewresponses/"+name+'/ResponseNo'+str(counter)+'.json', "w+")
            json.dump(json_file, f)
            f.close()
        icounter = icounter + 1
        if icounter == 20001:
            break

catchExceptionLoop(resetIndex, icounter, path, SteamAppDB)
#conn = Connection(base_url)