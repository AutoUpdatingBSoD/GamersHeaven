######################################################
#                                                    #
#       Program name: model                          #
#           - Original Author:      Michael Hammond  #
#           - Edited by:            Michael Hammond  #
#           - Date Created:         2/22/21          #
#           - Date Last Updated:    4/13/21          #
#                                                    #
######################################################

# Import Statements

# The ones everyone uses:
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# File and Server Connection
from os import walk
import mysql.connector
import json

# Scikit-Learn Model Development:
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score, recall_score, accuracy_score

# XGBoost:
import xgboost
from xgboost import XGBClassifier





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
    # Walk over the outputted Review CSV Directory to once again get the CSV File names, this time for batch import into a DF for the Model.
    filepath, dir, files = next(walk(r""))
    # Create a MySQL connection object
    conn = mysql.connector.connect(user='', password='',
                                   host='',
                                   database='')
    # Create a connection cursor object.
    cursor = conn.cursor(buffered=True)
    # For all of the Table Names recorded by the CSV Import Process.
    for i in range(len(files)):
        # table name taken from the CSV list to import data from MySQL into Pandas DF in batch.
        table_name = files[i].strip(".csv")
        # SQL Query to select all fields from the current table in the loop which pertain to the ML Model being tested.
        query = ("SELECT "
        "DTO_Timestamp_Created,"
        "Price_Cut,"
        "Current_Price,"
        "Old_Price,"
        "Score,"
        "Reviewer_Game_Count,"
        "Review_Positive_Vote_Count,"
        "Review_Funny_Vote_Count,"
        "Owner_Playtime_Last_Two_Weeks,"
        "Recieved_For_Free,"
        "Review_Comment_Count,"
        "Purchased_On_Steam,"
        "Early_Access_Review from " + table_name + "")
        # Execute the Query and Commit it.
        cursor.execute(query)
        conn.commit()
        
        # Append each row retrieved to the DataFrame.
        for (DTO_Timestamp_Created, Price_Cut, Current_Price, Old_Price, Score, Reviewer_Game_Count, Review_Positive_Vote_Count, Review_Funny_Vote_Count, Owner_Playtime_Last_Two_Weeks, Recieved_For_Free, Review_Comment_Count, Purchased_On_Steam, Early_Access_Review) in cursor:
            df = df.append({"Price_Cut":Price_Cut, "Current_Price":Current_Price, "Old_Price":Old_Price, "Score":Score, "Reviewer_Game_Count":Reviewer_Game_Count, "Review_Positive_Vote_Count":Review_Positive_Vote_Count, "Review_Funny_Vote_Count":Review_Funny_Vote_Count, "Owner_Playtime_Last_Two_Weeks":Owner_Playtime_Last_Two_Weeks, "Recieved_For_Free":Recieved_For_Free, "Review_Comment_Count":Review_Comment_Count, "Purchased_On_Steam":Purchased_On_Steam, "Early_Access_Review":Early_Access_Review,"DTO_Timestamp_Created":DTO_Timestamp_Created}, ignore_index=True)
    # Close the cursor and connection for safety.
    cursor.close()
    conn.close()
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
    temp_df = pd.DataFrame(columns=results_df_cols)
    # create the results DataFrame Columns and an Empty DataFrame to go with it.

    # To ensure accuracy with the model, do the below steps n number of times...
    for j in range(0, n):
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
        # the review score as the dependent variable.

        # print(y.value_counts())
        # Sanity check performed to see how many Positive and Negative Reviews are in the entire set.
        # You should keep this here to see how closely your set is related, and adjust scale_pos_weight
        # based on this difference.


        correlation_types = ["Game Price", "Reviewer Interaction", "Community Involvement With Review"]
        # list of names to give each output metric when the Visual is created.

        # community_engagement_in_review_test = [4, 6, 7, 10]
        # test set I did to check to see how review score relates to community engagement w/o ML.


        # ...for every independent variable set
        for i in range(len(x_sets)):
            x = df_test.iloc[:, x_sets[i]]
            # independent variable set being tested on.
            X_train, X_test, y_train, y_test = train_test_split(x, y, train_size=0.7, test_size=0.3, random_state=11, shuffle=True)
            # Actually defining the model.S
            # Tree_method and gpu_id are designed to allow for GPU threading.
            # Booster was changed to gblinear once it became apparent that this was a logistic regression XGB problem.
            # Subsample is set to half for a documented reason I forget (as in it's literally in the Python XGBoost documentation).
            # scale_pos_weight is set to the weight of my dependent distribution. I.e. 36 True Downvotes/100 True Upvotes
            # max_depth is set to such a weight where I can start to push my machine to its limits. Reduce if needed.
            # max_bin was increased to account for more buckets in RAM, default is 256.

            # The reason this was all changed was because I was not getting very accurate results under gbtree and default,
            # non-GPU-boosted parameters.
            model = XGBClassifier(booster='gblinear', max_depth=26, subsample=0.5, objective="binary:logistic", scale_pos_weight=0.36,
             tree_method='gpu_hist', gpu_id=0, max_bin=512)
            
            #fit the XGB model to the X Train set and the Y Test Set.
            model.fit(X_train, y_train)

            # Below are some sanity checks I made for myself so that I know what my data's actually doing.
            # I recommend uncommenting some of these for yourself and playing around with them to get a feel
            # for what the data's actually doing

            # 
            #if (i == 2):
            #    x_2 = df_test.iloc[:, community_engagement_in_review_test]
            #    print(x_2.value_counts())


            #print(x.value_counts())
            #print(y.value_counts())
            
            # Confirming x and y initial sets are what they should be.


            #print(y_train.value_counts())
            #print(y_test.value_counts())
            
            # Confirming y train and test ratios are what they should be


            # print(X_train.value_counts())
            
            # Confirming X training ratio is what it should be, confirming the test ratio on X is redundant but can be done if you want.



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
            results_df = results_df.append({"correlation_type":correlation_types[i],"accuracy":accuracy*100}, ignore_index=True)
        if j != 0: 
            print(temp_df.head())
            print(results_df.head())
            # Average each item in the accuracy column of both DataFrames, and set each value as the result DataFrame accuracy values.
            for i in range(0,2):
                results_df['accuracy'][i] = (results_df['accuracy'][i]+temp_df['accuracy'][i])/2
        if j + 1 < n:    
            print(results_df.head())
            # set the temp DF to the current accuracy score DF.
            temp_df = results_df
            # create a new DF
            results_df = pd.DataFrame(columns=results_df_cols)
    
    write_to_mySQL(results_df)

#   write_to_mySQL : pandas DF -> MySQL Table with Content
#   
#   This function uses a MySQL Connection to import model accuracy results into a table that may or may not exist already.
#
#   params:
#           - df: Pandas DataFrame containing Accuracy Results
#
#   return: 
#           - RESULTS: A MySQL Table containing all of the column names and averaged accuracy scores over the N Trial runs
#                      performed for each Independent Variable Set
#
def write_to_mySQL(df):
    # Create MySQL Connection Object
    conn = mysql.connector.connect(user='', password='',
                                   host='',
                                   database='')
    # create a cursor object
    cursor = conn.cursor(buffered=True)
    # drop the results table if it exists, execute and commit
    query=("DROP TABLE IF EXISTS RESULTS")
    cursor.execute(query)
    conn.commit()
    # Create the results table, execute and commit
    query=("CREATE TABLE results (correlation_type varchar(255), accuracy INT)")
    cursor.execute(query)
    conn.commit()
    # insert every row into the results DataFrame, execute and commit
    for index, row in df.iterrows():
        query=("INSERT INTO RESULTS (correlation_type, accuracy) VALUES (%s, %s) ")
        cursor.execute(query, tuple(row))
        conn.commit()
    # close both the cursor and connection objects for safety.
    cursor.close()
    conn.close()

#   svemodeltodisk : String -> Pandas-Oriented Review Data CSV
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

# Main Method
def main():
    inname = "out.csv"
    #savemodeltodisk(inname)
    # Uncomment the immediate line above if you want to load the model into a CSV File
    # ---------------------------------------------------------------------------------------------------------------
    # Uncomment the immediate line below if you want to run the model, train the model, and save the results to MySQL.
    trainmodel(inname)
    
if __name__ == "__main__":
    main()