import json
import csv
import pandas as pd
import requests
from pathlib import Path
import os
import pymysql
import time
from datetime import datetime, timedelta
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
            counter = 0
            cursor = ""
            lastcursor = ""
            os.mkdir(""+path+"/reviewresponses/"+name)
            try:
                # Create a connection object
                databaseserverhostname = "localhost"
                databaseusername = "root"  
                databaseuserpass = ""
                newdatabasename = "ReviewsDataNo"+10
                cursorType = pymysql.cursors.DictCursor
                connectioninstance = pymysql.connect(host=databaseserverhostname, user=databaseusername, password=databaseuserpass, cursorclass=cursortype)
                cursorinstance = connectioninstance.cursor()                                    
                sqlStatement = "CREATE TABLE "+newdatabasename+ "(id INT PRIMARY KEY, Voted_Up Boolean, Review TEXT, Games_Owned_By_Reviewer int, Created_On DATE, language TEXT, Updated_On DATE, Votes_Up INT, Votes_Funny INT, Created_On_Int INT, Updated_On_Int INT, Recent_Playtime Int, All_Time_Playtime Int, Last_Time_Played int, recieved_for_free Boolean, comment_count Int, steam_purchase Boolean, Written_During_Early_Access Boolean, created_day int, created_hour int, created_month int, created_second int, created_year int, created_minute int, updated_day int, updated_hour int, updated_minute  int, updated_month int, updated_second  int, updated_year int)"
                cursorInsatnce.execute(sqlStatement)
                path, dirs, files = next(os.walk(""+path+"/reviewresponses/"+name))
                file_count = len(files) - 1
                for i in range(file_count):
                    counter = file_count - i
                    f = open(r""+path+"/reviewresponses/"+name+'/ResponseNo'+str(counter)+'.json', "w+")
                    data = json.load(f)  
                    f.close()
                    reviews_count_for_page = ['query_summary']['num_reviews']
                    reviews_count_for_page = int(reviews_count_for_page)
                    for j in range(reviews_count_for_page):
                        inside_file_counter = reviews_count_for_page - j - 1
                        data_cell = json_file['reviews'][str(inside_file_counter)]
                        id = counter
                        author = data_cell['author']
                        voted_up = data_cell['voted_up']
                        votes_up = data_cell['votes_up']
                        votes_funny = data_cell['votes_funny']
                        owner_total_playtime_in_hours = data_cell['playtime_forever']
                        owner_playtime_in_past_two_weeks = data_cell['playtime_last_two_weeks']
                        num_games_owned = author['num_games_owned']
                        num_reviews = author['num_reviews']
                        time_last_played = author['last_played']
                        owned_games = author['num_games_owned']

                        review_language = data_cell['english']
                        timestamp_created = data_cell['timestamp_created']
                        timestamp_updated = data_cell['timestamp_updated']
                        review = data_cell['review']
                        weighted_vote_score = data_cell['weighted_vote_score']
                        comment_count = data_cell['comment_count']
                        steam_purchase = data_cell['steam_purchase']
                        recieved_for_free = data_cell['recieved_for_free']
                        written_during_early_access = data_cell['written_during_early_access']


                        created_year = 2000+int(timestamp_created[0:2])
                        updated_year = 2000+int(timestamp_updated[0:2])
                        created_month = int(timestamp_created[2:4])
                        updated_month = int(timestamp_updated[2:4])
                        created_day = int(timestamp_created[4:6])
                        updated_day = int(timestamp_updated[4:6])
                        created_hour = int(timestamp_created[6:7])
                        updated_hour = int(timestamp_updated[6:7])
                        created_minute = int(timestamp_created[7:8])
                        updated_minute = int(timestamp_updated[7:8])
                        created_second = int(timestamp_created[8:10])
                        updated_second = int(timestamp_updated[8:10])

                        timestamp_created_dto = datetime(year=created_year, month=created_month, day=created_day, hour=created_hour, minute=created_minute, second=created_second)
                        timestamp_updated_dto = datetime(year=updated_year, month=updated_month, day=updated_day, hour=updated_hour, minute=updated_minute, second=updated_second)

                        values = str(counter)+","+str(voted_up)+","+str(review)+","+str(owned_games)+","+str(timestamp_created_dto)+","+str(review_language)+","+str(timestamp_updated_dto)+","+str(votes_up)+","+str(votes_funny)+","+str(timestamp_created)+","+str(timestamp_updated)+","+str(owner_playtime_in_past_two_weeks)+","+str(received_for_free)+","+str(comment_count)+","+str(steam_purchase)+","+str(written_during_early_access)
                        values = values+","+str(created_day)+","+str(created_hour)+","+str(created_month)+","+str(created_second)+","+str(created_year)+","+str(created_minute)+","+str(updated_day)+","+str(updated_hour+","+str(updated_minute)+","+str(updated_month)+","+str(updated_second)+","+str(updated_year)
                        sqlStatement = "INSERT INTO" + newdatabasename + "(id, Voted_Up, Review, Games_Owned_By_Reviewer, Created_On, language, Updated_On, Votes_Up, Votes_Funny, Created_On_Int, Updated_On_Int, Recent_Playtime, All_Time_Playtime, Last_Time_Played, received_for_free, comment_count, steam_purchase, Written_During_Early_Access"
                        sqlStatement = sqlStatement + "created_day,created_hour, created_month, created_second, created_year, created_minute, updated_day, updated_hour, updated_minute, updated_month, updated_second, updated_year)"
                        sqlStatement = sqlStatement + " values ("+values+")"
                        cursorInsatnce.execute(sqlStatement)
                        counter = counter + 1
            except:
                print ("\n\n")
                resetIndex = icounter + 1
                catchExceptionLoop(resetIndex, 0, path, SteamAppDB)
        icounter = icounter + 1

catchExceptionLoop(resetIndex, icounter, path, SteamAppDB)