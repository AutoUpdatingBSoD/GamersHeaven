import json
import csv
import pandas as pd
import requests
from pathlib import Path
import os
import pymysql
icounter = 0
path = "C:/users/unrea/Desktop/"
SteamAppDB = pd.read_json(r""+path+"SteamApps.json")
dirlist = os.listdir()

resetIndex = 83
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
                newdatabasename             = "ReviewsDataNo"+10
                cursorType                  = pymysql.cursors.DictCursor
                connectioninstance = pymysql.connect(host=databaseserverhostname, user=databaseusername, password=databaseuserpass, cursorclass=cursortype)
                cursorinstance = connectioninstance.cursor()                                    
                sqlStatement = "CREATE DATABASE "+newdatabasename
                cursorInsatnce.execute(sqlQuery)
                while (truth):
                    f = open(r""+path+"/reviewresponses/"+name+'/ResponseNo'+str(counter)+'.json', "w+"):
                    data = json.load(f)
                    f.close()
            except:
                print ("\n\n")
                resetIndex = icounter + 1
                catchExceptionLoop(resetIndex, 0, path, SteamAppDB)
        icounter = icounter + 1

catchExceptionLoop(resetIndex, icounter, path, SteamAppDB)