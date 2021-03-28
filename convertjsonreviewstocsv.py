import json
import csv
import pandas as pd
import requests
from pathlib import Path
import os
import time
from datetime import datetime, timedelta
import os.path
from pathlib import Path
import os.path
icounter = 0
path = "C:/users/unrea/Desktop/"
SteamAppDB = pd.read_json(r""+path+"SteamApps.json")
dirlist = os.listdir()

resetIndex = 0
reviewpath = "C:/users/unrea/Desktop/"

def catchExceptionLoop(resetIndex, icounter, path, SteamAppDB):
    for index, row in SteamAppDB.iterrows():
        if icounter >= resetIndex:
            truth = True
            name = str(index).strip("app")
            cursor = ""
            lastcursor = ""
            file_count = len(os.listdir(""+path+"/reviewresponses/"+name))
            with open(r''+path+"HTTP Responses/app"+str(name)+'SteamStoreSalesData.json') as file:
                json_sales = json.load(file)
            sale_object = json_sales['data']
            sales_size = len(sale_object)
            print(file_count)

            #print("yes")
            for i in range(file_count):
                with open(r''+reviewpath+"reviewresponses/"+str(name)+'/ResponseNo'+str(i+1)+'.json') as f:
                    json_file = json.load(f)
                reviews_count_for_page = json_file['query_summary']['num_reviews']
                reviews_count_for_page = int(reviews_count_for_page)
                for j in range(reviews_count_for_page):
                    inside_file_counter = reviews_count_for_page - j - 1
                    data_cell = json_file['reviews'][inside_file_counter]
                    author = data_cell['author']
                    voted_up = data_cell['voted_up']
                    votes_up = data_cell['votes_up']
                    votes_funny = data_cell['votes_funny']
                    owner_total_playtime_in_hours = author['playtime_forever']
                    owner_playtime_in_past_two_weeks = author['playtime_last_two_weeks']
                    num_games_owned = author['num_games_owned']
                    num_reviews = author['num_reviews']
                    time_last_played = author['last_played']
                    owned_games = author['num_games_owned']
                    #review_language = data_cell['language']
                    timestamp_created = data_cell['timestamp_created']
                    timestamp_updated = data_cell['timestamp_updated']
                    #review = data_cell['review']
                    weighted_vote_score = data_cell['weighted_vote_score']
                    comment_count = data_cell['comment_count']
                    steam_purchase = data_cell['steam_purchase']
                    received_for_free = data_cell['received_for_free']
                    if received_for_free == True:
                        received_for_free == 1
                    elif received_for_free == False:
                        received_for_free == -1
                    written_during_early_access = data_cell['written_during_early_access']
                    #timestamp_created_2 = time.strftime("%Y%m%d:%H%M%S", time.localtime(timestamp_created))
                    #timestamp_updated_2 = time.strftime("%Y%m%d:%H%M%S", time.localtime(timestamp_updated))
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
                    timestamp_created_dto = datetime(year=created_year, month=created_month, day=created_day, hour=created_hour, minute=created_minute, second=created_second)
                    timestamp_updated_dto = datetime(year=updated_year, month=updated_month, day=updated_day, hour=updated_hour, minute=updated_minute, second=updated_second)
                    for l in range(sales_size - 1):
                        sales_previous_price = sale_object[l]['old'][0]
                        sales_current_price = sale_object[l]['new'][0]
                        sales_cut = sale_object[l]['cut']
                        sales_current_date = sale_object[l]['at']
                        headerrow=["Last_Price_Change", "Price_Cut", "Current_Price", "Old_Price", "Score", "Reviewer_Game_Count", "Review_Positive_Vote_Count", "Review_Funny_Vote_Count", "Owner_Playtime_Last_Two_Weeks", "Recieved_For_Free", "Review_Comment_Cou", "Purchased_On_Steam", "Early_Access_Review", "Unix_TImestamp_Created", "Unix_Timestamp_Updated", "DTO_Timestamp_Created", "DTO_Timestamp_Updated", "Day_Created_Int", "Hour_Created_Int", "Month_Created_Int", "Second_Created_Int", "Year_Created_Int", "Minute_Cre ated_Int", "Day_Updated_Int", "Hour_Updated_Int", "Month_Updated_Int", "Second_Updated_Int", "Year_Updated_Int", "Minute_Updated_Int"]
                        rowcontents=[str(sales_current_date), str(sales_cut), str(sales_current_price), str(sales_previous_price), str(voted_up), str(owned_games), str(votes_up), str(votes_funny), str(owner_playtime_in_past_two_weeks), str(received_for_free), str(comment_count), str(steam_purchase), str(written_during_early_access), str(timestamp_created_dto), str(timestamp_updated_dto), str(timestamp_created), str(timestamp_updated), str(created_day), str(created_hour), str(created_month), str(created_second), str(created_year), str(created_minute), str(updated_day), str(updated_hour), str(updated_minute), str(updated_month), str(updated_second), str(updated_year)]
                        if l != sales_size - 1:
                            if sales_current_date <= timestamp_created < sale_object[l+1]['at']:
                                reaffirmjsondatematch(reviewpath+'ReviewCSVs/ReviewGameID'+name+'RangeIs'+str(l)+'.csv', headerrow, rowcontents)
                                break
                        else:
                            if sales_current_date <= timestamp_created:
                                reaffirmjsondatematch(reviewpath+'ReviewCSVs/ReviewGameID'+name+'RangeIs'+str(l)+'.csv', headerrow, rowcontents)
                                break
        icounter = icounter + 1
def reaffirmjsondatematch(outname, headerrow, rowcontents):
    if not os.path.exists(outname):
        Path(outname).touch()
        writetocsv(headerrow, outname)
    writetocsv(rowcontents, outname)
def writetocsv(rowcontents, outname):
    with open(outname, 'a', encoding= 'utf-8', newline='') as csvfile:
        reviewwriter = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        reviewwriter.writerow(rowcontents)
catchExceptionLoop(resetIndex, icounter, path, SteamAppDB)