import tweepy
import os
import csv
import json
import sys
from os.path import expanduser
from .config.ConfigReader import ConfigurationReader

# Twitter API credentials
home = expanduser("~")
Configuration = ConfigurationReader()
TweetsStorage = Configuration.GetTweetsStorage()
HashTagStorage = Configuration.GetTweetsStorage()

class Twweeter():
    
    def __init__(self):
        self.cfg = self.getCreds()
        self.api = self.get_api(self.cfg)

    def get_api(self, cfg):
        #Twitter only allows access to a users most recent 3240 tweets with this method
        """get api
        Args:
            cfg : 
        Returns:
            Tweepy API 
        """
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        return tweepy.API(auth)

    def get_all_tweets(self, screen_name):
        """get all tweets 
        Args:
            screen_name : 
        Returns:

        """
        # initialize a list to hold all the tweepy Tweets
        alltweets = []

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = self.api.user_timeline(screen_name = screen_name, count = 200)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        # while respecting the api's rate limiting to avoid 429s
        # probably should lower this to be used a few times in a 15 minute window
        last=0
        for i in range(0,899):
            print(("getting tweets before {}".format(oldest)))

            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = self.api.user_timeline(screen_name = screen_name, count = 200, max_id = oldest)

            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print(("...{} tweets downloaded so far".format(len(alltweets))))
            if last==len(alltweets):
                break
            last=len(alltweets)

        # transform the tweepy tweets into a 2D array that will populate the csv
        outtweets = [[tweet.id_str,tweet.created_at,tweet.text.encode("utf-8")]for tweet in alltweets]

        # write to csv
        global TweetsStorage
        TweetsStorage=str(os.getcwd()+TweetsStorage)
        os.makedirs(os.path.dirname(TweetsStorage), exist_ok=True)
        fn=str(TweetsStorage+screen_name+'_tweets.csv')
        with open(fn,'w') as f:
            writer = csv.writer(f)
            writer.writerow(["id","created_at","text"])
            writer.writerows(outtweets)

        pass

    # function to download the tweets of a particular hashtag
    def get_tweets_of_hashtag(self, hash_tag):
        print(("Please be patient while we download the tweets"))

        # initialize a list to hold all the tweepy Tweets
        all_tweets = []

        for i in range(0,179):
            new_tweets = tweepy.Cursor(self.api.search, q=hash_tag).items(200)
            for tweet in new_tweets:
                all_tweets.append(tweet.text.encode("utf-8"))
                # max_id will be id of last tweet when loop completes. shitty way of doing things
                max_id = tweet.id

            print(("We have got {} tweets so far".format(len(all_tweets))))
            new_tweets = tweepy.Cursor(self.api.search, q=hash_tag).items(200)
            if (len(all_tweets)) >= 1000:
                break
        global HashTagStorage
        HashTagStorage=str(os.getcwd()+HashTagStorage)
        os.makedirs(os.path.dirname(TweetsStorage), exist_ok=True)
        filename=str(HashTagStorage+hash_tag+'s.csv')
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            for tweet in all_tweets:
                if tweet:
                    writer.writerow([tweet])

        print(("1000 tweets have been saved to {}.csv".format(hash_tag)))

    def get_trending_topics(self):
    
        trends1 = self.api.trends_place(1) # 1 for worldwide
        data = trends1[0]
        trends = data['trends']
        print(("\nTrending topics worldwide :"))
        for item in trends:
            print((item['name']))
    
    def process_or_store(self, tweet):
        print((json.dumps(tweet,indent=1)))
    
    def readTimeLine(self):
        # loop through the first ten items of your home timeline
        for status in tweepy.Cursor(self.api.home_timeline).items(10):
            # process a single status
            # print((status.text))
            self.process_or_store(status._json)

    def getFollowersList(self):
        id=0
        numberOfFollowers = input('Enter number of followers you want to get: ')
        for friend in tweepy.Cursor(self.api.followers).items(int(numberOfFollowers)):
            friend=friend._json
            id +=1
            print("{}. {} -- @{}".format(id,friend["name"],friend["screen_name"] ))

    def getTweets(self):
        id = 0
        numberOfTweets = input('Enter the number of Tweets you want to get: ')
        for tweet in tweepy.Cursor(self.api.user_timeline).items(int(numberOfTweets)):
            # process_or_store(tweet._json)
            tweet = tweet._json
            id += 1
            print("{}.{}".format(id,tweet["text"]))

    def getCreds(self):
        if not os.path.isfile(home+'/.twweet-cli/data/creds.json'):
            self.createCreds()
        with open(home+'/.twweet-cli/data/creds.json') as json_file:
            return json.load(json_file)

    def createCreds(self):
        try:
            ck = input('Enter your Consumer Key: ').strip()
            cs = input('Enter your Consumer Secret: ').strip()
            at = input('Enter your Access Token: ').strip()
            ats = input('Enter your Access Token Secret: ').strip()
            jsondata= {"consumer_key": ck,
            "consumer_secret": cs,
            "access_token": at,
            "access_token_secret": ats}
            with open(home+"/.twweet-cli/data/creds.json", "w") as outfile:
                json.dump(jsondata, outfile)
        except KeyError:
            sys.stderr.write("TWITTER_* environment variables not set\n")
            sys.exit(1)
