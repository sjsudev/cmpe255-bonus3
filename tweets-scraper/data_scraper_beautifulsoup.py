#!/usr/bin/python
# -*- coding: utf-8 -*-

import twint
import pandas as pd

def getdata(requested_twitter_user, label):
    tweets = []

    c = twint.Config()
    c.Limit = 2000
    c.Username = requested_twitter_user

    c.Store_object = True
    c.Store_object_tweets_list = tweets

    twint.run.Search(c)

    # First get data for emergency training - @SJPD_PIO San Jose Police Department
    # This will be trained as emergency data. 
    # Manual review will correct any misclassified data in this automation.

    print(len(tweets))

    formatted_tweets = []
    for tweet in tweets:
        try:    
            data = [label, tweet.datetime, tweet.id, tweet.tweet, requested_twitter_user]
            data = tuple(data)
            formatted_tweets.append(data)
        except Exception as e:
            print('Exception Encountered')
            print(e)
            break

    return pd.DataFrame(formatted_tweets, columns = ['emergency_', 'created_at','tweet_id', 'tweet_text', 'screen_name'])


# Execution of scraping features here.
# df1 = getdata('SanMateoPD', 'emergency')
# df2 = getdata('SJPD_PIO', 'emergency')
# df3 = getdata('RentonpdWA', 'emergency')
# df4 = getdata('BPD_Operations', 'emergency')
# df5 = getdata('NBCNewYork', 'emergency')

df1 = getdata('dailystar', 'non-emergency')
df2 = getdata('elonmusk', 'non-emergency')
df3 = getdata('DonaldJTrumpJr', 'non-emergency')
df4 = getdata('thesundaytimes', 'non-emergency')
df5 = getdata('espn', 'non-emergency')

frames = [df1, df2, df3, df4, df5]
result = pd.concat(frames)

result.to_csv(path_or_buf = 'training-tweets-nonemergency.csv', index=False) 

result.value_counts()