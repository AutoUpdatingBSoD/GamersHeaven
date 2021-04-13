######################################################
#                                                    #
#       Program Name: convertjsonreviewstocsv        #
#           - Original Author:      Michael Hammond  #
#           - Edited by:            Michael Hammond  #
#           - Date Created:         3/25/21          #
#           - Date Last Updated:    3/30/21          #
#                                                    #
######################################################

#imports

import json
import csv
import pandas as pd
# data manipulation

import time
from datetime import datetime, timedelta
# time functions

import os
import os.path
from pathlib import Path
# operating systems file literacy.


path = "C:/Users/Unrea/Desktop"
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



#   parsesalesandreviewjson : int, int, string, Pandas Dataframe -> csv list
#   
#   This function takes Steam Review Data and IsTnereAnyDeal API Sales Data and converts them
#   to combined csvs based on what point the review record is recorded in time.
#
#   params:
#           - pointer_to_begin_loop:         The root pointer for your index.
#           - positional_reindexing_pointer: The index you want your pointer to loop to to start your program.
#           - path:                          The root directory of the file structure.
#           - steam_app_df:                  The IsThereAnyDeal SteamApp ID Database, loaded into pandas.
#
#   return: 
#           - ReviewGameID'+AppID+'RangeIs'+rangeID+'.csv' : Multiple CSVs which contains parsed results.
#
def parsesalesandreviewjson(pointer_to_begin_loop, positional_reindexing_pointer, path, steam_app_df):
    reviewpath = path+"reviewresponses/"
    # Review data directory.
    outpath = path+"ReviewCSVs/"
    # Output file directory.
    for index, row in steam_app_df.iterrows(): # For every game in the Steam AppID df
        # if your reindex pointer matches the pointer to begin your loop.
        # Why does this exist?
        # This is a solution which prevents redundant records.
        if positional_reindexing_pointer >= pointer_to_begin_loop:
            # Steam App ID pulled from the cell header name.
            app_id = str(index).strip("app")
            # the total amount of JSON files in the reviews directory.
            file_count = len(os.listdir(reviewpath+app_id))
            # Load sales JSON data for an AppID into memory.
            # This is being obtained now to reduce memory overhead.
            with open(r''+path+"HTTP Responses/app"+str(app_id)+'SteamStoreSalesData.json') as file:
                json_sales = json.load(file)
            # redefine sales JSON in memory to match structure.
            sale_object = json_sales['data']
            # Obtain the amount of sales changes in the Sales JSON data.
            # If we load the JSON data and get the sales size any later,
            # these two operations will be called exactly n times,
            # n being either the number of JSON files or the number of records
            # of the review data for the AppID, depending on where you put it. 
            #
            # This is being called prematurely, yes, but it's being done so as a
            # specific code optimization strategy to reduce processor calls in the Pipeline.
            sales_size = len(sale_object)
            # for every file in the GameIDs recorded review data JSON files list
            for i in range(file_count):

                # Start by opening a ReviewJSON file.
                with open(r''+reviewpath+str(app_id)+'/ResponseNo'+str(i+1)+'.json') as f:
                    json_file = json.load(f)
                # Get the total amount of reviews on the page.
                reviews_count_for_page = json_file['query_summary']['num_reviews']
                # Typecast reviews to int, default is string.
                reviews_count_for_page = int(reviews_count_for_page)
                # For all the reviews on the page.
                for j in range(reviews_count_for_page):
                    # get the actual jth review body for parsing individually.
                    data_cell = json_file['reviews'][j]
                    author = data_cell['author']
                    # user review score, either positive or negative.
                    voted_up = data_cell['voted_up']
                    # how many positive votes a review has recieved.
                    votes_up = data_cell['votes_up']
                    # how many times users have voted a review funny.
                    votes_funny = data_cell['votes_funny']
                    # The amount of playtime the review author has on the game in Integer format.
                    owner_total_playtime_in_hours = author['playtime_forever']
                    # The amount of playtime the review author has on the game in the past two weeks in Integer format.
                    owner_playtime_in_past_two_weeks = author['playtime_last_two_weeks']
                    # The total number of games the review author owns.
                    num_games_owned = author['num_games_owned']
                    # The total number of reviews the author has made.
                    num_reviews = author['num_reviews']
                    # The Unix Timestamp the author last played the game.
                    time_last_played = author['last_played']
                    # The number of games the review author owns.
                    owned_games = author['num_games_owned']
                    # The Unix timestamp the review was created.
                    timestamp_created = data_cell['timestamp_created']
                    # The Unix timestamp the review was last updated.
                    timestamp_updated = data_cell['timestamp_updated']
                    # The average vote score for the game to the point of data log creation,
                    # although this isn't utilized in the Machine Learning Model.
                    weighted_vote_score = data_cell['weighted_vote_score']
                    # The total number of comments that have been left on a user review.
                    comment_count = data_cell['comment_count']

                    # Whether or not the game was purchased on Steam.
                    steam_purchase = data_cell['steam_purchase']
                    # Whether or not the review author recieved the game for free.
                    received_for_free = data_cell['received_for_free']
                    # Whether or not the review was written during early access.
                    written_during_early_access = data_cell['written_during_early_access']

                    # reclassifying boolean values for machine learning purposes.
                    # I.E. using True and False won't work for ML.
                    # so we reclassify the variables as 1 for True and -1 for False                    
                    if voted_up == True:
                        voted_up == 1
                    elif voted_up == False:
                        voted_up == -1
                        
                    if steam_purchase == True:
                        steam_purchase == 1
                    elif steam_purchase == False:
                        steam_purchase == -1

                    if received_for_free == True:
                        received_for_free == 1
                    elif received_for_free == False:
                        received_for_free == -1

                    if written_during_early_access == True:
                        written_during_early_access == 1
                    elif written_during_early_access == False:
                        written_during_early_access == -1

                    # split the two review timestamps into years, months, days, hours, minutes, and seconds for records.
                    created_year = int(time.strftime("%y", time.localtime(timestamp_created)))
                    updated_year = int(time.strftime("%y", time.localtime(timestamp_updated)))
                    created_month = int(time.strftime("%m", time.localtime(timestamp_created)))
                    updated_month = int(time.strftime("%m", time.localtime(timestamp_updated)))
                    created_day = int(time.strftime("%d", time.localtime(timestamp_created)))
                    updated_day = int(time.strftime("%d", time.localtime(timestamp_updated)))
                    created_hour = int(time.strftime("%H", time.localtime(timestamp_created)))
                    updated_hour = int(time.strftime("%H", time.localtime(timestamp_updated)))
                    created_minute = int(time.strftime("%M", time.localtime(timestamp_created)))
                    updated_minute = int(time.strftime("%M", time.localtime(timestamp_updated)))
                    created_second = int(time.strftime("%S", time.localtime(timestamp_created)))
                    updated_second = int(time.strftime("%S", time.localtime(timestamp_updated)))

                    #create Date Time Objects (DTOs) for Database Records
                    timestamp_created_dto = datetime(year=created_year, month=created_month, day=created_day, hour=created_hour, minute=created_minute, second=created_second)
                    timestamp_updated_dto = datetime(year=updated_year, month=updated_month, day=updated_day, hour=updated_hour, minute=updated_minute, second=updated_second)

                    for k in range(sales_size):
                        # how much the game is selling for regular price.
                        sales_previous_price = sale_object[k]['old'][0]
                        # how much the game is going on sale.                       
                        sales_current_price = sale_object[k]['new'][0]
                        # percentage discount.
                        sales_cut = sale_object[k]['cut']
                        # unix timestamp of price change.
                        sales_current_date = sale_object[k]['at']
                    
                        #defining header row app_ids.
                        headerrow=["Last_Price_Change", "Price_Cut", "Current_Price", "Old_Price", "Score", "Reviewer_Game_Count", "Review_Positive_Vote_Count", "Review_Funny_Vote_Count", "Owner_Playtime_Last_Two_Weeks", "Recieved_For_Free", "Review_Comment_Count", "Purchased_On_Steam", "Early_Access_Review", "DTO_Timestamp_Created", "DTO_Timestamp_Updated","Unix_TImestamp_Created", "Unix_Timestamp_Updated", "Day_Created_Int", "Hour_Created_Int", "Month_Created_Int", "Second_Created_Int", "Year_Created_Int", "Minute_Cre ated_Int", "Day_Updated_Int", "Hour_Updated_Int", "Month_Updated_Int", "Second_Updated_Int", "Year_Updated_Int", "Minute_Updated_Int"]
                        #adding sales and review attributes for the point in time the review occured to the list.
                        rowcontents=[str(sales_current_date), str(sales_cut), str(sales_current_price), str(sales_previous_price), str(voted_up), str(owned_games), str(votes_up), str(votes_funny), str(owner_playtime_in_past_two_weeks), str(received_for_free), str(comment_count), str(steam_purchase), str(written_during_early_access), str(timestamp_created_dto), str(timestamp_updated_dto), str(timestamp_created), str(timestamp_updated), str(created_day), str(created_hour), str(created_month), str(created_second), str(created_year), str(created_minute), str(updated_day), str(updated_hour), str(updated_minute), str(updated_month), str(updated_second), str(updated_year)]
                        outfilename = outpath+'/ReviewGameID'+app_id+'RangeIs'+str(k)+'.csv'
                        # Doing a nested if statement to proactively prevent a pointer issue.
                        if k != sales_size - 1:
                            # Checking to see if the timestamp a review was created falls within the lth range of
                            # a period of sales deltas for this game.
                            # That is: From the starting point of a sales change to the next sales change,
                            # this if statement checks whether the creation review timestamp falls within that range and
                            # calls the CSV writing method based on what range it falls in.
                            if sales_current_date <= timestamp_created < sale_object[k+1]['at']:
                                reaffirmjsondatematch(outfilename, headerrow, rowcontents)
                                break
                        else:
                            # Doing effectively the same thing as described in the above nested if, just checking for the
                            # last sales change in the Sales time series data for the specified game
                            if sales_current_date <= timestamp_created:
                                reaffirmjsondatematch(outfilename, headerrow, rowcontents)
                                break
        # increment the positional pointer.
        positional_reindexing_pointer = positional_reindexing_pointer + 1

#   reaffirmjsondatematch : string, list, list -> output csv
#   
#   This function takes the output file name, a CSV header, and row contents and writes them all to CSV
#   NOTE: the header row is only written if the method detects the output file does not exist.
#
#   params:
#           - outfilename:          name of the output CSV file name
#           - headerrow:            header row
#           - rowcontents:          contents of row to be written out to CSV
#
#   return: 
#           - CSV with at least the row contents (and the header if a new file).
#
def reaffirmjsondatematch(outfilename, headerrow, rowcontents):
    # check if the output csv is not on disk
    if not os.path.exists(outfilename):
        # create a blank output csv with the filename
        Path(outfilename).touch()
        # write the header row to the newly created csv
        writetocsv(headerrow, outfilename)
    # write the row contents to the output csv
    writetocsv(rowcontents, outfilename)
#   writetocsv : list, string -> output csv
#   
#   This function takes row contents and an output file name and writes them to CSV
#
#   params:
#           - outfilename:          name of the output CSV file name
#           - rowcontents:          contents of row to be written out to CSV
#
#   return: 
#           - csv with the file named outfilename and a new line
#
def writetocsv(rowcontents, outfilename):
    with open(outfilename, 'a', encoding= 'utf-8', newline='') as csvfile:
        reviewwriter = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        reviewwriter.writerow(rowcontents)
parsesalesandreviewjson(pointer_to_begin_loop, positional_reindexing_pointer, path, steam_app_df)