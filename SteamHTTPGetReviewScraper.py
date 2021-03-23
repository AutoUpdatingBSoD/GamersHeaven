import json
import csv
import pandas as pd
import requests
from pathlib import Path
import os
icounter = 0
path = ""
#Root Directory
SteamAppDB = pd.read_json(r""+path+"SteamApps.json") 
#List of Every App ID and Game Name on Steam
dirlist = os.listdir()

resetIndex = 935 
# the index at which the program actually starts doing API Calls
# this cursor is useful whenever API calls, python, or the JSON triggers
# some weird exception and you're not really concerned about having every last
# record possible. (typically triggered when the AppID doesn't exist in the servers
# of the IsThereAnyDeal ServerJapanhowh)

def catchExceptionLoop(resetIndex, icounter, path, SteamAppDB):
    for index, row in SteamAppDB.iterrows():
        if icounter >= resetIndex:
            try:
                truth = True
                name = str(index).strip("app")
                counter = 0
                cursor = ""
                lastcursor = ""
                os.mkdir(""+path+"/reviewresponses/"+name)
                while (truth):
                   
                    base_url = "https://store.steampowered.com/appreviews/"+name+"?json=1"
                    if counter != 0:
                        base_url = base_url+"&cursor="+cursor
                    response = requests.get(base_url)
                    json_file = response.json()
                    counter = counter + 1
                    lastcursor = cursor
                    cursor = json_file['cursor']
                    f = open(r""+path+"/reviewresponses/"+name+'/ResponseNo'+str(counter)+'.json', "w+")
                    json.dump(json_file, f)
                    f.close()
                    if cursor == lastcursor:
                        truth = False
                        print ("End of data source. Doing the next one now!")
            except:
                print ("Oops! Either I can't find the Steam server, or there's exactly 20 or less reviews for this game in total!\n It's recommended that you download this page for ID No. "+name+"yourself, or run this loop for this ID if you believe there's more than 20 reviews.\nResetting the loop now...")
                resetIndex = icounter + 1
                catchExceptionLoop(resetIndex, 0, path, SteamAppDB)
        icounter = icounter + 1
        if icounter == 15000:
            break

catchExceptionLoop(resetIndex, icounter, path, SteamAppDB)