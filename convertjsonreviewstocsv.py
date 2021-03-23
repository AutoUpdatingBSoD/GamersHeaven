import json
import csv
import pandas as pd
import requests
from pathlib import Path
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
icounter = 0
path = "C:/users/unrea/Desktop/"
SteamAppDB = pd.read_json(r""+path+"SteamApps.json")
dirlist = os.listdir()

resetIndex = 545
reviewpath = "C:/users/unrea/Desktop/"

def catchExceptionLoop(resetIndex, icounter, path, SteamAppDB):
    for index, row in SteamAppDB.iterrows():
        if icounter >= resetIndex:
            truth = True
            name = str(index).strip("app")
            counter = 0
            cursor = ""
            lastcursor = ""
            file_count = len(os.listdir(""+path+"/reviewresponses/"+name))
            print(file_count)
            Path(reviewpath+'ReviewCSVs/ReviewGameID'+name+'.csv').touch()
            print("yes")
            with open(reviewpath+'ReviewCSVs/ReviewGameID'+name+'.csv', 'w', encoding= 'utf-8', newline='') as csvfile:
                reviewwriter = csv.writer(csvfile, delimiter='[', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i in range(file_count):
                    print(i)
                    counter = file_count - i
                    print(str(name)+''+str(counter))
                    with open(r''+reviewpath+"reviewresponses/"+str(name)+'/ResponseNo'+str(counter)+'.json') as f:
                        json_file = json.load(f)
                    reviews_count_for_page = json_file['query_summary']['num_reviews']
                    reviews_count_for_page = int(reviews_count_for_page)
                    for j in range(reviews_count_for_page):
                        inside_file_counter = reviews_count_for_page - j - 1
                        data_cell = json_file['reviews'][inside_file_counter]
                        id = counter
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


                        review_language = data_cell['language']
                        timestamp_created = data_cell['timestamp_created']
                        timestamp_updated = data_cell['timestamp_updated']
                        review = data_cell['review']
                        weighted_vote_score = data_cell['weighted_vote_score']
                        comment_count = data_cell['comment_count']
                        steam_purchase = data_cell['steam_purchase']
                        received_for_free = data_cell['received_for_free']
                        if received_for_free == True:
                            received_for_free == 1
                        elif received_for_free == False:
                            received_for_free == -1
                        written_during_early_access = data_cell['written_during_early_access']
                        timestamp_created_2 = time.strftime("%Y%m%d:%H%M%S", time.localtime(timestamp_created))
                        timestamp_updated_2 = time.strftime("%Y%m%d:%H%M%S", time.localtime(timestamp_updated))

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


                        reviewwriter.writerow([str(counter), str(review), str(review_language), str(voted_up), str(owned_games), str(votes_up), str(votes_funny), str(owner_playtime_in_past_two_weeks), str(received_for_free), str(comment_count), str(steam_purchase), str(written_during_early_access), str(timestamp_created_dto), str(timestamp_updated_dto), str(timestamp_created), str(timestamp_updated), str(created_day), str(created_hour), str(created_month), str(created_second), str(created_year), str(created_minute), str(updated_day), str(updated_hour), str(updated_minute), str(updated_month), str(updated_second), str(updated_year)])
                        counter = counter + 1
        icounter = icounter + 1
        print("Done")

catchExceptionLoop(resetIndex, icounter, path, SteamAppDB)