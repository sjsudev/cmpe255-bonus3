import tweepy
from tweepy import OAuthHandler
import pandas as pd

access_token = '72854806-zqMsDeuXfNpFfBzLSug2tN519Hp1GUiqHzNF05ILC'
access_token_secret = '0sVeL3WgKS4UoJu3sNPI63Nk85BpzQanu1wlAGKwxtPAl'
consumer_key = '4P8vukHtLSAPOcERLJo8cA8lI'
consumer_secret = 'ypZYxqPLVlKKshRaPYxEhq1UrXsVxO21LDrRZb0O4BUSWmuWot'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets = []

count = 1

# First get data for emergency training - @SJPD_PIO San Jose Police Department
# This will be trained as emergency data. 
# Manual review will correct any misclassified data in this automation.

for tweet in tweepy.Cursor(api.search, q="@SJPD_PIO", count=450, since='2020-02-28').items(50000):
	
	print(count)
	count += 1

	try: 
		data = ['emergency', tweet.created_at, tweet.id, tweet.text, tweet.user._json['screen_name'], tweet.user._json['name'], tweet.user._json['created_at'], tweet.entities['urls']]
		data = tuple(data)
		tweets.append(data)

	except tweepy.TweepError as e:
		print(e.reason)
		continue

	except StopIteration:
		break

df = pd.DataFrame(tweets, columns = ['emergency_', 'created_at','tweet_id', 'tweet_text', 'screen_name', 'name', 'account_creation_date', 'urls'])

print(df.head(10))

# df.to_csv(path_or_buf = 'training-tweets-emergency.csv', index=False) 