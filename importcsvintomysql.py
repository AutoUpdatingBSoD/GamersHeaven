######################################################
#                                                    #
#       Program Name: importcsvtomysql               #
#           - Original Author:      Michael Hammond  #
#           - Edited by:            Michael Hammond  #
#           - Date Created:         4/04/21          #
#           - Date Last Updated:    4/12/21          #
#                                                    #
######################################################
#imports

from os import walk
import mysql.connector
import pandas as pd

# Get CSV filenames so that we can easily import them all into MySQL as a batch process.
# This directory is whatever your output CSV Directory is from convertjsonreviewstocsv.py
filepath, dir, files = next(walk(r""))
# Create a MySQL Connection, removed references to database connections for security.
conn = mysql.connector.connect(user='', password='',
                               host='',
                               database='')
# create a cursor object, which is entirely necessary for SQL Statements.
cursor = conn.cursor(buffered=True)

# For every CSV in the CSV directory
for i in range(len(files)):
    cursor.execute("Show Tables")
    filename = files[i].strip(".csv")
    print(filename)
    
    query=("DROP TABLE IF EXISTS "+filename)
    cursor.execute(query)
    conn.commit()
    query=("CREATE TABLE "+filename+" ( Last_Price_Change INT, Price_Cut INT, Current_Price INT, Old_Price INT, Score INT, Reviewer_Game_Count INT, Review_Positive_Vote_Count INT, Review_Funny_Vote_Count INT, Owner_Playtime_Last_Two_Weeks INT, Recieved_For_Free INT, Review_Comment_Count INT, Purchased_On_Steam INT, Early_Access_Review INT, DTO_Timestamp_Created DATETIME, DTO_Timestamp_Updated DATETIME, Unix_TImestamp_Created INT, Unix_Timestamp_Updated INT, Day_Created_Int SMALLINT, Hour_Created_Int SMALLINT, Month_Created_Int SMALLINT, Second_Created_Int SMALLINT, Year_Created_Int SMALLINT, Minute_Created_Int SMALLINT, Day_Updated_Int SMALLINT, Hour_Updated_Int SMALLINT, Month_Updated_Int SMALLINT, Second_Updated_Int SMALLINT, Year_Updated_Int SMALLINT, Minute_Updated_Int SMALLINT)")
    cursor.execute(query)
    conn.commit()
    df = pd.read_csv(filepath+"/"+files[i], index_col=False)
    for index, row in df.iterrows():
        sql = "INSERT INTO " + filename+ " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, tuple(row))
        conn.commit()
cursor.close()
conn.close()
