import matplotlib.pyplot as plt
import numpy as np
from keras.callbacks import Callback
from keras.datasets import mnist
from keras.layers import Dense, LSTM
from keras.models import Sequential
from keras.utils import np_utils
import pandas as pd
from phased_lstm_keras.PhasedLSTM import PhasedLSTM as PLSTM
# PLEASE, FOR YOUR OWN GOOD, RUN THIS PROJECT WITH ANACONDA WITH KERAS 2.1.5 AND PYTHON <= 3.7!!!!!!
from sklearn.model_selection import train_test_split         
import os
import json
import time
from datetime import datetime
import datetime
from sklearn.preprocessing import StandardScaler
def createReviewDF():
    path = "C:/users/unrea/Desktop/"
    dfcols = ["Voted_Up", "Review","Games_Owned_By_Reviewer", "Review_Count", "Votes_Up", "Votes_Funny",  "Recent_Playtime", "All_Time_Playtime", "received_for_free", "comment_count", "steam_purchase", "Written_During_Early_Access", "Created_On", "Updated_On", "created_day", "created_hour", "created_month", "created_second", "created_year", "created_minute", "updated_day", "updated_hour", "updated_minute", "updated_month", "updated_second", "updated_year"]
    df = pd.DataFrame(columns = dfcols)
    icounter = 0
    resetIndex = 1
    #for index, row in SteamAppDB.iterrows():
    #    if icounter >= resetIndex:
    #        break
    #truth = True
    name = 10 #str(index).strip("app")
    counter = 1
    cursor = ""
    lastcursor = "" 
    paths, dirs, files = next(os.walk(""+path+"/reviewresponses/"+str(name)))
    file_count = len(files) - 1
    print("nyess")
    for i in range(file_count - 1):
        print(str(i)+"th")
        counter = file_count - i - 1
        with open(r''+path+"/reviewresponses/"+str(name)+'/ResponseNo'+str(counter)+'.json') as f:
            json_file = json.load(f) 
        reviews_count_for_page = json_file['query_summary']['num_reviews']
        reviews_count_for_page = int(reviews_count_for_page)
        for j in range(reviews_count_for_page):
            inside_file_counter = reviews_count_for_page - j - 1
            ifc = str(inside_file_counter)
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
            df = df.append({"Voted_Up":voted_up, "Review":review,"Games_Owned_By_Reviewer":num_games_owned, "Review_Count":num_reviews,    "Votes_Up":votes_up, "Votes_Funny":votes_funny, "Recent_Playtime":owner_playtime_in_past_two_weeks, "All_Time_Playtime":owner_total_playtime_in_hours, "received_for_free":received_for_free, "comment_count":comment_count, "steam_purchase":steam_purchase, "Written_During_Early_Access":written_during_early_access, "Created_On":timestamp_created, "Updated_On":timestamp_updated, "created_day":created_day, "created_hour":created_hour, "created_month":created_month, "created_second":created_second, "created_year":created_year, "created_minute":created_minute, "updated_day":updated_day, "updated_hour":updated_hour, "updated_minute":updated_minute, "updated_month":updated_month, "updated_second":updated_second, "updated_year":updated_year}, ignore_index=True)
        counter = counter + 1
        #icounter = icounter + 1
        #break
    return df

class AccHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('acc'))


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))


def main():
    #SteamAppDB = pd.read_csv("C:/users/unrea/Desktop/AppIDDB.json")
    #print(SteamAppDB.head())
    print("yes")
    reviewDF = createReviewDF()
    print("nooo")
    print(reviewDF.head())
    # input image dimensions
    x = reviewDF.iloc[:, range(2,26)]
    y = reviewDF.iloc[:, 0]
    z = reviewDF.iloc[:, 1]
    X_train, X_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2, random_state=42, shuffle=True)

    # the data, shuffled and split between train and test sets
    sc_x = StandardScaler()
    X_train = sc_x.fit_transform(X_train)
    X_test = sc_x.transform(X_test)
    # convert class vectors to binary class matrices
    Y_train = np_utils.to_categorical(y_train, nb_classes)
    Y_test = np_utils.to_categorical(y_test, nb_classes)
    print('Y_train shape:', Y_train.shape)
    print('Y_test shape:', Y_test.shape)

    # LSTM with timegate
    model_PLSTM = Sequential()
    model_PLSTM.add(PLSTM(32, input_shape=(28 * 28, 1), implementation=2))
    model_PLSTM.add(Dense(10, activation='softmax'))
    model_PLSTM.compile(optimizer='rmsprop', loss='categorical_crossentropy',
                        metrics=['accuracy'])
    model_PLSTM.summary()
    acc_PLSTM = AccHistory()
    loss_PLSTM = LossHistory()
    model_PLSTM.fit(X_train, Y_train, epochs=nb_epoch, batch_size=batch_size, callbacks=[acc_PLSTM, loss_PLSTM])
    score_PLSTM = model_PLSTM.evaluate(X_test, Y_test, verbose=0)

    # Vanilla LSTM
    model_LSTM = Sequential()
    model_LSTM.add(LSTM(32, input_shape=(28 * 28, 1), implementation=2))
    model_LSTM.add(Dense(10, activation='softmax'))
    model_LSTM.compile(optimizer='rmsprop', loss='categorical_crossentropy',
                       metrics=['accuracy'])
    model_LSTM.summary()
    acc_LSTM = AccHistory()
    loss_LSTM = LossHistory()
    model_LSTM.fit(X_train, Y_train, epochs=nb_epoch, batch_size=batch_size,
                   callbacks=[acc_LSTM, loss_LSTM])
    score_LSTM = model_LSTM.evaluate(X_test, Y_test, verbose=0)

    # plot results
    plt.figure(1, figsize=(10, 10))
    plt.title('Accuracy on MNIST training dataset')
    plt.xlabel('Iterations, batch size ' + str(batch_size))
    plt.ylabel('Classification accuracy')
    plt.plot(acc_LSTM.losses, color='k', label='LSTM')
    plt.hold(True)
    plt.plot(acc_PLSTM.losses, color='r', label='PLSTM')
    plt.savefig('mnist_plstm_lstm_comparison_acc.png', dpi=100)

    plt.figure(2, figsize=(10, 10))
    plt.title('Loss on MNIST training dataset')
    plt.xlabel('Iterations, batch size ' + str(batch_size))
    plt.ylabel('Categorical cross-entropy')
    plt.plot(loss_LSTM.losses, color='k', label='LSTM')
    plt.hold(True)
    plt.plot(loss_PLSTM.losses, color='r', label='PLSTM')
    plt.savefig('mnist_plstm_lstm_comparison_loss.png', dpi=100)

    # Compare test performance
    print('Test score LSTM:', score_LSTM[0])
    print('Test score Phased LSTM:', score_PLSTM[0])
    #def review_test_pred():




if __name__ == "__main__":
    main()


#def read_reviews(SteamAppDB
