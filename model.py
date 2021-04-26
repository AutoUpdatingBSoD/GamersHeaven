######################################################
#                                                    #
#       Program name: model                          #
#           - Original Author:      Michael Hammond  #
#           - Edited by:            Michael Hammond  #
#           - Date Created:         2/22/21          #
#           - Date Last Updated:    4/26/21          #
#                                                    #
######################################################

# Import Statements

# The ones everyone uses:
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from random import seed
from random import randint
# File and Server Connection
from os import walk
import mysql.connector
import json
import csv

# Scikit-Learn Model Development:
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score, recall_score, accuracy_score

# XGBoost:
import xgboost
from xgboost import XGBClassifier
import warnings




#   createreviewdf : MySql Connection -> Pandas DF
#   
#   This function uses a MySQL Connection to load Steam Review Data Separated by Sale Occurence (see convertjsonreviewstocsv)
#   and import them into a Pandas DataFrame
#
#   params:
#           - None, but you will need a MySQL Connection with data already loaded
#
#   return: 
#           - df : Pnadas DataFrame Containing Data Ready to be Trained.
#
def createreviewdf():
    # Root File Directory
    path = ""
    # Pandas DataFrame Column Names For Model DataFrame
    dfcols = ["Price_Cut",
    "Current_Price",
    "Old_Price",
    "Score",
    "Reviewer_Game_Count",
    "Review_Positive_Vote_Count",
    "Review_Funny_Vote_Count",
    "Owner_Playtime_Last_Two_Weeks",
    "Recieved_For_Free",
    "Review_Comment_Count",
    "Purchased_On_Steam",
    "Early_Access_Review"]
    # Create an empty dataframe, when complete this is what's returned.
    df = pd.DataFrame(columns=dfcols)
    conn, cursor = createMySQLConnection()
    # table name
    table_name = "modelset"
    #SQL Query
    query = "SELECT DTO_Timestamp_Created,Price_Cut,Current_Price,Old_Price,Score,Reviewer_Game_Count,Review_Positive_Vote_Count,Review_Funny_Vote_Count,Owner_Playtime_Last_Two_Weeks,Recieved_For_Free,Review_Comment_Count,Purchased_On_Steam,Early_Access_Review from " + table_name + ""
    #execute the query
    conn, cursor = executesimplequery(query_text, conn, cursor)
    
    # Append each row retrieved to the DataFrame.
    for (DTO_Timestamp_Created, Price_Cut, Current_Price, Old_Price, Score, Reviewer_Game_Count, Review_Positive_Vote_Count, Review_Funny_Vote_Count, Owner_Playtime_Last_Two_Weeks, Recieved_For_Free, Review_Comment_Count, Purchased_On_Steam, Early_Access_Review) in cursor:
        df = df.append({"Price_Cut":Price_Cut, "Current_Price":Current_Price, "Old_Price":Old_Price, "Score":Score, "Reviewer_Game_Count":Reviewer_Game_Count, "Review_Positive_Vote_Count":Review_Positive_Vote_Count, "Review_Funny_Vote_Count":Review_Funny_Vote_Count, "Owner_Playtime_Last_Two_Weeks":Owner_Playtime_Last_Two_Weeks, "Recieved_For_Free":Recieved_For_Free, "Review_Comment_Count":Review_Comment_Count, "Purchased_On_Steam":Purchased_On_Steam, "Early_Access_Review":Early_Access_Review,"DTO_Timestamp_Created":DTO_Timestamp_Created}, ignore_index=True)
    # Close the cursor and connection for safety.
    closeconnections(conn, cursor)
    # print df.head(), since this is a lengthy import, as a sanity check.
    print(df.head())
    # return the newly created DataFrame.
    return df

#   trainmodel : MySql Connection -> Pandas DF
#   
#   This function uses a MySQL Connection to load Steam Review Data Separated by Sale Occurence (see convertjsonreviewstocsv)
#   and import them into a Pandas DataFrame
#
#   params:
#           - inname : Exported Pandas DataFrame representing restructured review data in CSV Format.
#
#   return: 
#           - results_df : a pandas DataFrame containing the 
#
def trainmodel(inname):
    df_test = pd.read_csv(inname)
    # Load Data Set from CSV to Memory
    n = 100
    # The amount of times to run the model for each independent variable set.


    results_df_cols = ["correlation_type", "accuracy"]
    results_df = pd.DataFrame(columns=results_df_cols)
    trained_results_df = pd.DataFrame(columns=results_df_cols)
    temp_df = pd.DataFrame(columns=results_df_cols)
    # create the results DataFrame Columns and an Empty DataFrame to go with it.

    # To ensure accuracy with the model, do the below steps n number of times...
    #for j in range(0, n):
    df_test = df_test.sample(frac = 1)
    # Rearrange the DataFrame just in case there's a problem.

    stats_on_current_game_price = [1, 2, 3]
    # All Variables relating fo how much tbr game costs right now.
    reviewer_engagement_for_game = [5, 8, 9, 11, 12]
    # All variables relating to the reviewers engagement on Steam related to the game.
    community_engagement_in_review = [6, 7, 10]
    # All variables relating to the Steam Community's engagement in a review.AttributeError() 

    x_sets = [stats_on_current_game_price, reviewer_engagement_for_game, community_engagement_in_review]
    # each variable set in a List.
    y = df_test.iloc[:, 4]
    # the review score as t-he dependent variable.

    # print(y.value_counts())
    # Sanity check performed to see how many Positive and Negative Reviews are in the entire set.
    # You should keep this here to see how closely your set is related, and adjust scale_pos_weight
    # based on this difference.


    correlation_types = ["Game Price", "Reviewer Interaction", "Community Involvement With Review"]
    # list of names to give each output metric when the Visual is created.

    # community_engagement_in_review_test = [4, 6, 7, 10]
    # test set I did to check to see how review score relates to community engagement w/o ML.

    #number of times to retrain model
    n = 99
    # keeping accuracy in memory
    inmemaccuracy = 0
    currentaccuracy = 0
    # ...for every independent variable set

    for i in range(len(x_sets)):
        x = df_test.iloc[:, x_sets[i]]
        # independent variable set being tested on.
        X_train, X_test, y_train, y_test = train_test_split(x, y, train_size=0.7, test_size=0.3, random_state=11, shuffle=True)
        model = XGBClassifier(booster='gblinear', max_depth=26, subsample=0.5, objective="binary:logistic", scale_pos_weight=0.36,
        tree_method='gpu_hist', gpu_id=0, max_bin=512)
        # Actually defining the model.
        # Tree_method and gpu_id are designed to allow for GPU threading.
        # Booster was changed to gblinear once it became apparent that this was a logistic regression XGB problem.
        # Subsample is set to half for a documented reason I forget (as in it's literally in the Python XGBoost documentation).
        # scale_pos_weight is set to the weight of my dependent distribution. I.e. 36 True Downvotes/100 True Upvotes
        # max_depth is set to such a weight where I can start to push my machine to its limits. Reduce if needed.
        # max_bin was increased to account for more buckets in RAM, default is 256.
        # The reason this was all changed was because I was not getting very accurate results under gbtree and default,
        # non-GPU-boosted parameters.
        # retrieve first accuracy score to keep in memory to be written at the end of all model passes.
        inmemaccuracy, model = runmodel(model, X_train, X_test, y_train, y_test)
        currentaccuracy = inmemaccuracy
        # initialize python random seed variable for first random model shuffle pass.
        seed(1)
        print("Initial " + correlation_types[i] + " score : " + str(inmemaccuracy))
        for j in range(0,n):
            # get a random int for the train test split seed
            randseed = randint(0, n)
            # reshuffle data semi-randomly with seed.
            # semi-random seeds are good enough due to how many times the model is being run.
            X_train, X_test, y_train, y_test = train_test_split(x, y, train_size=0.7, test_size=0.3, random_state=randseed, shuffle=True)
            # get an accuracy score to store in temporary memory.
            tempaccuracy, model = runmodel(model, X_train, X_test, y_train, y_test)
            currentaccuracy = tempaccuracy
            w=1/(j+1)
            # Average each item in the accuracy column of both DataFrames, and set each value as the result DataFrame accuracy values.    
            inmemaccuracy = inmemaccuracy*(1-w)+tempaccuracy*w
            if (j >= n-1):
                # Below are some sanity checks I made for myself so that I know what my data's actually doing.
                # I recommend uncommenting some of these for yourself and playing around with them to get a feel
                # for what the data's actually doing
                #
                if (i == 0): 
                    metrics = [4, 1, 2, 3]
                    controlled_set = ["Score", "Price_Cut", "Current_Price", "Old_Price"]
                    write_supporting_evidence(df_test, metrics, controlled_set, "PRICE")
                if (i == 1):
                    metrics = [4, 5, 8, 9, 11, 12]
                    controlled_set= ["Score", "Reviewer_Game_Count", "Owner_Playtime_Last_Two_Weeks", "Recieved_For_Free", "Purchased_On_Steam", "Early_Access_Review"]                    
                    write_supporting_evidence(df_test, metrics, controlled_set, "REVIEWER")
                if (i == 2):
                    metrics = [4, 6, 7, 10]
                    controlled_set = ["Score", "Review_Positive_Vote_Count","Review_Funny_Vote_Count","Review_Comment_Count"]
                    write_supporting_evidence(df_test, metrics, controlled_set, "community")
     
                # #Confirming X training ratio is what it should be, confirming the test ratio on X is redundant but can be done if you want.
            randseed = seed(randseed)
        inmemaccuracy = int(round(inmemaccuracy*100))
        currentaccuracy = int(round(currentaccuracy*100))
        results_df = results_df.append({"correlation_type":correlation_types[i],"accuracy":inmemaccuracy}, ignore_index=True)  
        trained_results_df = trained_results_df.append({"correlation_type":correlation_types[i],"accuracy":currentaccuracy}, ignore_index=True)    
    print(results_df.head())  
    print(trained_results_df.head())
    write_results_to_mySQL(results_df, "results", results_df_cols)
    write_results_to_mySQL(trained_results_df, "trainedresults", results_df_cols)
#   write_supporting_evidence : DataFrame, string, string -> MySQL Table with Content
#   
#   This function writes model accuracy results to MySQL
#
#   params:
#           - df           : results dataframe
#           - table_name   : MySQL Table name to Write
#           - column_names : list of column names
#
#   return: 
#           - RESULTS: A MySQL Table containing all of the column names and averaged accuracy scores over the N Trial runs
#                      performed for each Independent Variable Set
#
def write_supporting_evidence(df, metrics, controlled_set, measuring):
    data_proof = df.iloc[:, metrics]
    data_counts = data_proof.value_counts()
    df_counts = pd.DataFrame(data_counts)
    write_counts_to_mySQL(data_proof,measuring, controlled_set)
    print(df_counts.head())
#   runmodel : XGBoost Model, X Training Dataset, X Testing Dataset, Y Training Dataset, Y Testing Dataset -> XGBoost Model, float
#   
#   This function writes model accuracy results to MySQL
#
#   params:
#           - model     : XGBoost Model
#           - X_train   : X Training Set
#           - X_test    : X Testing Set
#           - y_train   : Y Training Set
#           - y_test    : Y Testing Set
#
#   return: 
#           - accuracy: The score determining if the results are right
#           - model:    The model to be retrained in future iterations
#
def runmodel(model, X_train, X_test, y_train, y_test):
    # Suppress annoying XGB model warnings. 
    # fit the model to the dataset
    model.fit(X_train, y_train)
    # Make predictions with Independent Variable Test Set  
    y_pred = model.predict(X_test)
    # Round the values in the prediction set
    predictions = [round(value) for value in y_pred]
    # Retrieve metrics on prediction data,
    precision=precision_score(y_test, predictions, average='macro')
    recall=recall_score(y_test, predictions, average='macro')
    accuracy=accuracy_score(y_test, predictions)
    print("Precision = "+str(precision))
    print("Recall = "+str(recall))
    print("Accuracy = "+str(accuracy*100))
    print(classification_report(predictions,y_test))
    # Since the only one of these that truly matters most is accuracy score, append that to the out DF to write.

    return accuracy, model

#   write_counts_to_mySQL : array, string, list -> MySQL Table with Content
#   
#   This function writes model independent variable counts as they relate to the dependent variables to MySQL
#
#   params:
#           - df           : results dataframe
#           - table_name   : MySQL Table name to Write
#           - column_names : list of column names
#
#   return: 
#           - table of name table_name: a table which contains how many times each item occurence
#             of a dependent/independent variable set
#
def write_counts_to_mySQL(df, table_name, column_names):
    table_columns, export_columns, column_inserts = formatColumnsForMySQLWrite(column_names, "INT")
    conn, cursor = databaseconnection(table_name, table_columns)
    # insert every row into the results DataFrame, execute and commit
    conn, cursor = write_df_to_MySQL(df, table_name, export_columns, column_inserts, conn, cursor)
    closeconnections(conn, cursor)

#   write_results_to_mySQL : DataFrame, string, string -> MySQL Table with Content
#   
#   This function writes model accuracy results to MySQL
#
#   params:
#           - df           : results dataframe
#           - table_name   : MySQL Table name to Write
#           - column_names : list of column names
#
#   return: 
#           - RESULTS: A MySQL Table containing all of the column names and averaged accuracy scores over the N Trial runs
#                      performed for each Independent Variable Set
#
def write_results_to_mySQL(df, table_name, column_names):
    table_columns, export_columns, column_inserts = formatColumnsForMySQLWrite(column_names, "VARcHAR(255)")
    conn, cursor = databaseconnection(table_name, table_columns)
    # insert every row into the results DataFrame, execute and commit
    conn, cursor = write_df_to_MySQL(df, table_name, export_columns, column_inserts, conn, cursor)
    closeconnections(conn, cursor)

#   databaseconnection : table_name, table_columns -> MySQL Connection, MySQL Cursor
#   
#   This function takes a table name and its formatted table columns for SQL Syntax
#   and reinitializes the default table object.
#
#   param:
#           - table_name:       the name of the table being written
#           - table_columns:    the columns to be used in the table reinitialization. 
#
#
#   return: 
#           - conn:   MySQL Connection Object
#           - cursor: MySQL Cursor Object
#
def databaseconnection(table_name, table_columns):
    conn, cursor = createMySQLConnection()
    conn, cursor = reinitMySQLTable(table_name, table_columns, conn, cursor)
    return conn, cursor
#   formatColumnsForMySQLWrite : list -> string, string, string
#   
#   This function takes a table columns structure array and its formatted table columns for SQL Syntax
#   and reinitializes the default table object.
#
#   param:
#           - column_names: A list of column names to be used in MySQL data operations
#
#   return: 
#           - table_columns:    a formatted string of columns to be used for creating a MySQL Table
#           - export_columns:   a formatted string of columns to be used for defining what columns to write to MySQL
#           - column_inserts:   a formatted string of columns to be used for defining what values get inserted in MySQL inserts.
#
def formatColumnsForMySQLWrite(column_names, data_type):
    table_columns = ""
    export_columns = ""
    column_inserts = "("
    for i in range (0,len(column_names)):
        column_inserts = column_inserts+"%s"
        if (i == 0):
            table_columns = table_columns+column_names[i]+" "+data_type
        else:
            table_columns = table_columns+column_names[i]+" INT"
        export_columns = export_columns + column_names[i]
        if (i < len(column_names) - 1):
            table_columns = table_columns + " , "
            export_columns = export_columns + " , "
            column_inserts = column_inserts + " , "

    column_inserts = column_inserts+")"
    #print(table_columns+"\n"+export_columns+"\n"+column_inserts)
    return table_columns, export_columns, column_inserts

#   write_df_to_mySQL : string, row, string, MySQL Connection, MySQL Cursor -> MySQL Content, MySQL Connection, MySQL Cursor
#   
#   This function uses a MySQL Database to load data into a table.
#
#   params:
#           - df                : Pandas dataframe object to write to db
#           - table_name        : MySQL Table name to Write
#           - columns           : string of formatted column names for easy SQL Writing
#           - column_inserts    : string of formatted SQL injection-protected characters separated by commas
#                                 of the same item length as the amount of columns being written.
#           - conn              : DB connection object
#           - cursor            : connection cursor object
#
#   return: 
#           - conn:   MySQL Connection Object
#           - cursor: MySQL Cursor Object
#
def write_df_to_MySQL(df, table_name, columns, column_inserts, conn, cursor):
    for index, row in df.iterrows():
        query="INSERT INTO "+table_name+ " ( "+columns+" )  VALUES "+column_inserts
        conn, cursor = executerowinsert(query, tuple(row), conn, cursor)
    return conn, cursor

#   closeconnections : MySQL Connection, MySQL Cursor -> null
#   
#   This function closes one each of an opened MySQL Connection and Cursor Object
#
#   param: 
#           - conn:   MySQL Connection Object
#           - cursor: MySQL Cursor Object
#
def closeconnections(conn, cursor):
    # close both the cursor and connection objects for safety.
    cursor.close()
    conn.close()

#   createMySQLConnection : null -> MySQL Connection, MySQL Cursor
#   
#   This function creates a MySQL Connection and Cursor Object and returns them
#
#   return: 
#           - conn:   MySQL Connection Object
#           - cursor: MySQL Cursor Object
#
def createMySQLConnection():
    # Define Variables For Database Object Connectivity so they won't be null when loaded.
    name=""
    host=""
    database=""
    password=""
    # Open a CSV with the Database Connection Information Inside of it.
    with open(r'', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name=row[0]
            host=row[1]
            database=row[2]
            password=row[3]
    # Create MySQL Connection Object
    conn = mysql.connector.connect(user=name, password=password,
                                   host=host,
                                   database=database)
    # create a cursor object
    cursor = conn.cursor(buffered=True)
    return conn, cursor

#   createMySQLConnection : String, MySQL Connection, MySQL Cursor -> query execution, MySQL Connection, MySQL Cursor
#   
#   This function takes a query string, a MySQL Connection, and a Cursor object and writes the query
#   to the MySQL Database
#
#   param:
#           - query_text:   actual SQL query in text form
#           - conn:         MySQL Connection Object
#           - cursor:       MySQL Cursor Object
#
#   return: 
#           - conn:   MySQL Connection Object
#           - cursor: MySQL Cursor Object
#
def executesimplequery(query_text, conn, cursor):
    query=(query_text)
    cursor.execute(query)
    conn.commit()
    return conn, cursor
#   createMySQLConnection : String, tuple, MySQL Connection, MySQL Cursor -> query execution, MySQL Connection, MySQL Cursor
#   
#   This function takes a query string, a tuple, a MySQL Connection, and a Cursor object
#   and writes the query to the MySQL Database
#
#   param:
#           - query_text:   actual SQL query in text form
#           - row:          tuple of items to be written to MySQL
#           - conn:         MySQL Connection Object
#           - cursor:       MySQL Cursor Object
#
#   return: 
#           - conn:   MySQL Connection Object
#           - cursor: MySQL Cursor Object
#
def executerowinsert(query_text, row, conn, cursor):
    query=(query_text)
    cursor.execute(query, row)
    conn.commit()
    return conn, cursor

#   reinitMySQLTable : String, String, MySQL Connection, MySQL Cursor -> query execution, MySQL Connection, MySQL Cursor
#   
#   This function takes the name of the table, the formatted table columns for SQL statements,
#   a MySQL connection, and a MySQL cursor, and writes the query to the MySQL Database
#
#   param:
#           - query_text:   actual SQL query in text form
#           - row:          tuple of items to be written to MySQL
#           - conn:         MySQL Connection Object
#           - cursor:       MySQL Cursor Object
#
#   return: 
#           - conn:   MySQL Connection Object
#           - cursor: MySQL Cursor Object
#   
def reinitMySQLTable(table_name, table_columns, conn, cursor):
    # drop the results table if it exists, execute and commit
    conn, cursor = executesimplequery("DROP TABLE IF EXISTS " + table_name, conn, cursor)
    # Create the results table, execute and commit
    conn, cursor = executesimplequery("CREATE TABLE "+ table_name + " (" + table_columns + ")", conn, cursor)
    return conn, cursor

#   savemodeltodisk : String -> Pandas-Oriented Review Data CSV
#   
#   This function takes the parsed Review Data in MySQL and stores it in a Pandas-Usable CSV.
#
#   params:
#           - outname: Filename to write the Pandas DataFrame to CSV.
#
#   return: 
#           - outname: A Pandas-Oriented CSV to be Loaded into the XGB Model.
#
def savemodeltodisk(outname):
    # Actually Create the DF
    reviewDF = createreviewdf()
    # Once Again Print the DF as a sanity check.
    print(reviewDF.head())
    # Write to CSV.
    reviewDF.to_csv(outname)

# Main Driver Method
def main():
    inname = "out.csv"
    #savemodeltodisk(inname)
    # Uncomment the immediate line above if you want to load the model into a CSV File
    # ---------------------------------------------------------------------------------------------------------------
    # Uncomment the immediate line below if you want to run the model, train the model, and save the results to MySQL.
    trainmodel(inname)
    
if __name__ == "__main__":
    main()