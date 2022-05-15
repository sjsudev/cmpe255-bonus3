#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
from tweepy import OAuthHandler
import pandas as pd

access_token = '72854806-zqMsDeuXfNpFfBzLSug2tN519Hp1GUiqHzNF05ILC'
access_token_secret = '0sVeL3WgKS4UoJu3sNPI63Nk85BpzQanu1wlAGKwxtPAl'
consumer_key = '4P8vukHtLSAPOcERLJo8cA8lI'
consumer_secret = 'ypZYxqPLVlKKshRaPYxEhq1UrXsVxO21LDrRZb0O4BUSWmuWot'


requested_twitter_user = 'SJPD_PIO'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# First get data for emergency training - @SJPD_PIO San Jose Police Department
# This will be trained as emergency data. 
# Manual review will correct any misclassified data in this automation.

tweets = []

# initial last 200 tweets
initial_tweets = api.user_timeline(screen_name=requested_twitter_user, 
                           count=200,
                           include_rts = False,
                           tweet_mode = 'extended'
                           )

for tweet in initial_tweets:
    try: 
        last_date = tweet.created_at

        # stop compiling tweets if too old.
        if tweet.created_at < 'Fri May 29 07:33:37 PDT 2020':
            break
            
        data = ['emergency', tweet.created_at, tweet.id, tweet.text, tweet.user._json['screen_name'], tweet.user._json['name'], tweet.user._json['created_at'], tweet.entities['urls']]
        data = tuple(data)
        tweets.append(data)
    except tweepy.TweepError as e:
        print(e.reason)
        continue
    except StopIteration:
        break

# Continue getting more tweets from the user
#
all_tweets = []
all_tweets.extend(tweets)
oldest_id = tweets[-1].id
last_date = 'Fri May 29 07:33:37 PDT 2050'

# while True:
#     if last_date < 'Fri May 29 07:33:37 PDT 2020':
#         break

#     tweets_scraped = api.user_timeline(screen_name=requested_twitter_user, 
#                            count = 200,
#                            include_rts = False,
#                            max_id = oldest_id - 1,
#                            tweet_mode = 'extended'
#                            )
#     if len(tweets_scraped) == 0:
#         break

#     oldest_id = tweets_scraped[-1].id
    
#     # Put the tweets in required training format
#     for tweet in tweets_scraped:
#         try: 
#             last_date = tweet.created_at

#             # stop compiling tweets if too old.
#             if tweet.created_at < 'Fri May 29 07:33:37 PDT 2020':
#                 break
                
#             data = ['emergency', tweet.created_at, tweet.id, tweet.text, tweet.user._json['screen_name'], tweet.user._json['name'], tweet.user._json['created_at'], tweet.entities['urls']]
#             data = tuple(data)
#             tweets.append(data)
#         except tweepy.TweepError as e:
#             print(e.reason)
#             continue
#         except StopIteration:
#             break
    
#     print('Number of tweets downloaded till now {}'.format(len(tweets)))

df = pd.DataFrame(tweets, columns = ['emergency_', 'created_at','tweet_id', 'tweet_text', 'screen_name', 'name', 'account_creation_date', 'urls'])

print(df.value_counts())
print(df.head(10))

# df.to_csv(path_or_buf = 'training-tweets-emergency.csv', index=False) 