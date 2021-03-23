import json
import csv
import pandas as pd
import requests
from pathlib import Path
import os
start_of_loop_index = 0
# The index of the start of the loop. This is useful for recursion calls
# Whenever an exception causes the current process to abruptly quit,
# thereby continuing to get data even though there was some technical
# difficulties (useful when combined with reset_ndex)
path = ""
#Root Directory
SteamAppDB = pd.read_json(r""+path+"SteamApps.json") 
#List of Every App ID and Game Name on Steam

url_front = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=HAHAHAHEATITHACKERS&format=json&plain="
url_tail = "shop=steam&region=us"
# the front-end and the back-end of the URLs separated by the name of each game.

resetIndex = 20000
# the index at which the program actually starts doing API Calls
# this cursor is useful whenever API calls, python, or the JSON triggers
# some weird exception and you're not really concerned about having every last
# record possible. (typically triggered when the AppID doesn't exist in the servers
# of the IsThereAnyDeal ServerJapanhowh)

def catchExceptionLoop(resetIndex, start_of_loop_index, path, SteamAppDB):
    for index, row in SteamAppDB.iterrows():
        if start_of_loop_index >= resetIndex:
            truth = True
            name = str(index).strip("app")
            file_counter = 1
            # the exact numbered file the loop is at at the present moment.
            url = url_front+row.data+url_tail
            # concatenate the beginning of the URL with the name of the game with the end of the URL
            response = requests.get(url)
            json_file = response.json()
            # call the URL and store the JSON in main memory
            file_counter = file_counter + 1

            f = open(r""+path+"/HTTP Responses/app"+name+"SteamStoreSalesData.json", "w+")
            json.dump(json_file, f)
            f.close()
            # Open a JSON file, dump the contents, close it.
        start_of_loop_index = start_of_loop_index + 1
        if start_of_loop_index == 20001: # Index at which to quit getting data, so that you don't exceed daily API calls. You need to keep a mental note of this limit yourself.
            break

catchExceptionLoop(resetIndex, start_of_loop_index, path, SteamAppDB)
#conn = Connection(url_front)