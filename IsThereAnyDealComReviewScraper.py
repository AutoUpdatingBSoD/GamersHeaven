######################################################
#                                                    #
#       Program Name: IsThereAnyDealComReviewScraper #
#           - Original Author:      Michael Hammond  #
#           - Edited by:            Michael Hammond  #
#           - Date Created:         3/22/21          #
#           - Date Last Updated:    4/12/21          #
#                                                    #
#        Additional Info                             #
#           - API Website: IsThereAnyDeal.com        #
#           - API Holder: Tomáš Fedor                #
#                                                    #
#     Recreation of Code Destroyed as a result of    #
#       Changing Server OS from Linux to Windows     #
#                                                    #
######################################################






#Import Statements
import json
import csv
import pandas as pd
import requests
from pathlib import Path
import os


path = ""
# The root directory of the file structure.
steam_app_df = pd.read_json(r""+path+"SteamApps.json")
# The IsThereAnyDeal SteamApp ID Database, loaded into pandas.

positional_reindexing_pointer = 0
# The index of the start of the loop. This is useful for recursion calls
# Whenever an exception causes the current process to abruptly quit,
# thereby continuing to get data even though there was some technical
# difficulties (useful when combined with pointer_to_begin_loop)
pointer_to_begin_loop = 0
# the index at which the program actually starts doing API Calls
# this cursor is useful whenever API calls, python, or the JSON triggers
# some weird exception and you're not really concerned about having every last
# record possible, or you've already parsed some of those records and you don't 
# want to redo them.

#   retrievesalesjson : int, int, string, Pandas Dataframe -> csv list
#   
#   This function takes a web API call and returns a JSON file, and does so in a batch.
#
#   params:
#           - pointer_to_begin_loop:         The root pointer for your index.
#           - positional_reindexing_pointer: The index you want your pointer to loop to to start your program.
#           - path:                          The root directory of the file structure.
#           - steam_app_df:                  The IsThereAnyDeal SteamApp ID Database, loaded into pandas.
#
#   return: 
#           - 'app'+app_id+'SteamStoreSalesData.json' : Multiple JSON Databases which contain dumped sales history.
#
def retrievesalesjson(pointer_to_begin_loop, positional_reindexing_pointer, path, steam_app_df):
    # For every game in the Steam AppID df
    for index, row in steam_app_df.iterrows():
        # if your reindex pointer matches the pointer to begin your loop.
        # Why does this exist?
        # This is a solution which prevents redundant records.
        if positional_reindexing_pointer >= pointer_to_begin_loop:
            try:
                # App ID obtained from the looped AppID Database at the current index
                app_id = str(index).strip("app")          
                # concatenate the App ID to the front-end and rear-ends of the API call.
                # You're not getting my API key that easy social engineers >:)
                base_url = "https://api.isthereanydeal.com/v01/game/history/?key=HAHAHAHAEATITHACKERS&plain="+app_id+"&shop=steam&region=us"
                # retrieve the json file
                json_file = requests.post(base_url)
                # create a temporary file to write the JSON to, as python doesn't write to empty files.
                Path(""+path+"HTTP Responses/app"+app_id+'SteamStoreSalesData.json').touch
                # open the new file
                f = open(r""+path+"HTTP Responses/app"+app_id+'SteamStoreSalesData.json', "w+")
                # append the newly retrieved JSON to the newly created file.
                json.dump(json_file, f)
                # close the file out of write mode to prevent errors.
                f.close()
            except:
                # In case there's any exception with the code, networking or otherwise.
                # Just go to the next set of records.
                print ("Oops! Something went wrong here! Possible Network Exception or Some other Error. Retrying now!")
                # Reposition the index to account for this bug, so you don't read the same potentially buggy
                # records again.
                pointer_to_begin_loop = positional_reindexing_pointer + 1
                # Restart the loop, with the new start-of-loop pointer set one index position after this loop rose an exception.
                retrievesalesjson(pointer_to_begin_loop, 0, path, steam_app_df)
        positional_reindexing_pointer = positional_reindexing_pointer + 1
        # Manual check to ensure max API call count (20k) is not exceeded
        if positional_reindexing_pointer == 15000:
            break

retrievesalesjson(pointer_to_begin_loop, positional_reindexing_pointer, path, steam_app_df)