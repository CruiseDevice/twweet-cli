import tweepy
#setting up twitter bot authentication
consumer_key = '#'
consumer_secret = '#'
access_token = '#'
access_token_secret = '#'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Creating an instance to connect to the twitter api
api = tweepy.API(auth)