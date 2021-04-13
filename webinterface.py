######################################################
#                                                    #
#       Program app_id: webinterface                 #
#           - Original Author:      Michael Hammond  #
#           - Edited by:            Michael Hammond  #
#           - Date Created:         4/04/21          #
#           - Date Last Updated:    4/12/21          #
#                                                    #
######################################################

# Import Statements
import plotly.express as px
import pandas as pd
import mysql.connector
import csv

def createresultsdf():
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
    # Define Result DataFrame Column Structure
    result_df_cols = ["Categories", "Accuracy"]
    # Connection Object Creation
    conn = mysql.connector.connect(user=name, password=password,
                                   host=host,
                                   database=database)
    # Cursor Object Creation
    cursor = conn.cursor(buffered=True)
    # Empty Result DataFrame Creation
    result_df = pd.DataFrame(columns=result_df_cols)
    
    n = 30
    # The amount of times to run the model for each independent variable set.

    # To ensure accuracy with the model, do the below steps n number of times
    for i in range(0, n):
        
        # Query the ith results table, execute and commit.
        query = ("SELECT "
        "correlation_type,"
        "accuracy from results"+str(i)+" "
        "ORDER BY accuracy DESC")
        cursor.execute(query)
        conn.commit()
        # if this is the first table being queried:
        if (i == 0):
            # Add each item queried to the dataframe.
            for (correlation_type, accuracy) in cursor:
                df = df.append({'Categories':correlation_type,"Accuracy":accuracy}, ignore_index=True)
        # if this is not the first table being queried:
        else:
            # create a temporary dataframe with the same column structure as before.
            temp_df = pd.DataFrame(columns=result_df_cols)
            # Append the new items to the temporary DataFrame
            for (correlation_type, accuracy) in cursor:
                temp_df = temp_df.append(
                    {'Categories':correlation_type,"Accuracy":accuracy}, ignore_index=True)
            # Average each item in the accuracy column of both DataFrames, and set each value as the result DataFrame accuracy values.
            for j in range(0,2):
                result_df['Accuracy'][j] = (result_df['Accuracy'][j]+temp_df['Accuracy'][j])/2
    # close the cursor and connection for safety 
    cursor.close()
    conn.close()
    # return the averaged result DataFrame.
    return result_df
def main():
    results_df = createresultsdf()
    # Print the Results DataFrame in case there's a Front-End issue later on.
    print(results_df.head())
    

    # Easy Plotly Bar Chart, X Axis is Each Individual Category, Y Axis is the total Averaged Accuracy.
    fig = px.bar(data_frame=results_df, x='Categories', y="Accuracy", title="What Actually has an Effect on Steam User Review Score?")
    # Actually show the figure because that's how python is.
    fig.show()
# Run the Main Method in Python.
if __name__ == "__main__":
    main()