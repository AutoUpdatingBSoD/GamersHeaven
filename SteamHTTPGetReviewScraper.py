######################################################
#                                                    #
#       Program Name: steamhttpgetreviewscraper      #
#           - Original Author:      Michael Hammond  #
#           - Edited by:            Michael Hammond  #
#           - Date Created:         3/22/21          #
#           - Date Last Updated:    4/12/21          #
#                                                    #
#        Additional Info                             #
#           - API Website: store.steampowered.com    #
#                                                    #
######################################################


import json
import csv
import pandas as pd
import requests
from pathlib import Path
import os

#List of Every App ID and Game app_id on Steam
dirlist = os.listdir()

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

#   retrievereviewjson : int, int, string, Pandas Dataframe -> csv list
#   
#   This function takes a web HTTP Get call and returns a JSON file, and does so in a batch.
#
#   params:
#           - pointer_to_begin_loop:         The root pointer for your index.
#           - positional_reindexing_pointer: The index you want your pointer to loop to to start your program.
#           - path:                          The root directory of the file structure.
#           - steam_app_df:                  The IsThereAnyDeal SteamApp ID Database, loaded into pandas.
#
#   return: 
#           - app_id+'/ResponseNo*.json' : Multiple JSON Databases which contain dumped review history for each App ID, separated by each folder app_idd by the game's App ID.
#
def retrievereviewjson(pointer_to_begin_loop, positional_reindexing_pointer, path, SteamAppDB):
    # For every game in the Steam AppID df
    for index, row in SteamAppDB.iterrows():
        # if your reindex pointer matches the pointer to begin your loop.
        # Why does this exist?
        # This is a solution which prevents redundant records.
        if positional_reindexing_pointer >= pointer_to_begin_loop:
            try:
                # loop check to confirm JSON is being continually read for each page Steam will allow to be shared for each App ID in batch.
                is_reading_json_reviews = True
                # App ID obtained from the looped AppID Database at the current index
                app_id = str(index).strip("app")
                # pointer to confirm JSON URL only has a cursor when it actually gets one.
                # also used to distinguish different JSON results from one another.AttributeError()
                json_loop_pointer = 0
                # Initialize the cursor.
                cursor = ""
                # Actually initialize the output App ID directory.
                os.mkdir(""+path+"reviewresponses/"+app_id)
                # list of different cursors returned, since steam likes to reuse cursors in its review data,
                # just checking the last cursor produces a confused pipeline with thousands of repeated results.
                cursor_list= []
                # While you haven't reached a new cursor when looping.
                while (is_reading_json_reviews):
                    # concatenate the front URL to the app id to the first part of the tail
                    base_url = "https://store.steampowered.com/appreviews/"+app_id+"?json=1"
                    if json_loop_pointer != 0:
                        # add a second tail to read from the page indicated by the previous page's cursor
                        # if a cursor is available.
                        base_url = base_url+"&cursor="+cursor
                    # make the HTTP GET call.
                    response = requests.get(base_url)
                    # save the JSON in memory.
                    json_file = response.json()
                    # Inrement the Loop Pointer early so as not to confuse beginner programmers on indexes which start at 0.
                    json_loop_pointer = json_loop_pointer + 1
                    # get the cursor from the JSON file in memory.
                    cursor = json_file['cursor']
                    # Open the file in write mode, for some reason I don't need to touch it first here. I don't know why.
                    f = open(r""+path+"reviewresponses/"+app_id+'/ResponseNo'+str(json_loop_pointer)+'.json', "w+")
                    # dump the JSON.
                    json.dump(json_file, f)
                    # Close the JSON so that progress actually happens.
                    f.close()
                    # Given the newly obtained cursor, did we already see this cursor or is it new?
                    if cursor in cursor_list:
                        # This cursor exists in our list. Starting a new game.
                        is_reading_json_reviews = False
                        print ("End of data source. Doing the next one now!")
                        cursor_list=[]
                    # Append the cursor *after* the check, because the check checks if we've seen it before.
                    # The append below just adds if it doesn't exist.
                    cursor_list.append(cursor)
            except:
                # In case there's any exception with the code, networking or otherwise.
                # Just go to the next set of records.
                # Particularly useful with the HTTP Scraper, since it's possible to raise an exception
                # before you've retrieved all the review data you can for that game.
                print ("Oops! Something went wrong here! Possible Network Exception or Some other Error. Retrying now!")
                # Reposition the index to account for this bug, so you don't read the same potentially buggy
                # records again.
                pointer_to_begin_loop = positional_reindexing_pointer + 1
                # I remember a reason I reset the cursor list here? I'm not entirely sure. This line might be junk.
                cursor_list=[]
                # Restart the loop, with the new start-of-loop pointer set one index position after this loop rose an exception.
                retrievereviewjson(pointer_to_begin_loop, 0, path, SteamAppDB)
        positional_reindexing_pointer = positional_reindexing_pointer + 1

retrievereviewjson(pointer_to_begin_loop, positional_reindexing_pointer, path, SteamAppDB)