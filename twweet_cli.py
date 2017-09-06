import tweepy
import os
import csv
import json
import sys
from os.path import expanduser
from .ConfigReader import ConfigurationReader
from importlib import reload

# Twitter API credentials
cfg = {}
home = expanduser("~")
Configuration=ConfigurationReader()
TweetsStorage=Configuration.GetTweetsStorage()
HashTagStorage=Configuration.GetTweetsStorage()

'''STREAM'''

class StreamListener(tweepy.StreamListener):
    # Decided I would keep all the overridable functions from the BaseClass so we know what we have to play with.
    def __init__(self, time_limit=60):
        super(StreamListener, self).__init__(api)

    def on_status(self, status):
        print('@{} => {}'.format(status.user.screen_name, status.text.replace("\n", " ")))

    def on_error(self, status_code):
        print('AN ERROR: {}'.format(status_code))
    #   read the docs and handle different errors

    def keep_alive(self):
        """Called when a keep-alive arrived"""
        return

    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        return

    def on_delete(self, status_id, user_id):
        """Called when a delete notice arrives for a status"""
        return

    def on_event(self, status):
        """Called when a new event arrives"""
        return

    def on_direct_message(self, status):
        """Called when a new direct message arrives"""
        return

    def on_friends(self, friends):
        """Called when a friends list arrives.

        friends is a list that contains user_id
        """
        return

    def on_limit(self, track):
        """Called when a limitation notice arrives"""
        return

    def on_timeout(self):
        """Called when stream connection times out"""
        return

    def on_disconnect(self, notice):
        """Called when twitter sends a disconnect notice

        Disconnect codes are listed here:
        https://dev.twitter.com/docs/streaming-apis/messages#Disconnect_messages_disconnect
        """
        return

    def on_warning(self, notice):
        """Called when a disconnection warning message arrives"""
        return

# authorise the stream listener
def authStreamer():
    streamListenerOB = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListenerOB)
    return stream

#Listen for tweets on the current users timeline
def streamYourTL():
    stream = authStreamer()
    stream.userstream(_with='following', async=True)

#listen for tweets containing a specific word or hashtag (a phrase might work too)
def streamWordOrHashtag(wordsList):
    stream = authStreamer()
    stream.filter(track=wordsList, async=True)

def decoMain(func):
    func()
    print( "DONE \n")
    return func

'''END STREAM'''

def get_api(cfg):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def get_all_tweets(screen_name):
    api = get_api(cfg)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name, count = 200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    # while respecting the api's rate limiting to avoid 429s
    # probably should lower this to be used a few times in a 15 minute window
    last=0
    for iter in range(0,899):
        print(("getting tweets before {}".format(oldest)))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name, count = 200, max_id = oldest)

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
def get_tweets_of_hashtag(hash_tag):
    all_tweets = []
    new_tweets = []
    print(("Please be patient while we download the tweets"))

    api = get_api(cfg)
    for i in range(0,179):
        new_tweets = tweepy.Cursor(api.search, q=hash_tag).items(200)
        for tweet in new_tweets:
            all_tweets.append(tweet.text.encode("utf-8"))
            # max_id will be id of last tweet when loop completes. shitty wasy of doing things
            max_id = tweet.id

        print(("We have got {} tweets so far".format(len(all_tweets))))
        new_tweets = tweepy.Cursor(api.search, q=hash_tag).items(200)
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


def get_trending_topics():

    api = get_api(cfg)

    trends1 = api.trends_place(1) # 1 for worldwide
    data = trends1[0]
    trends = data['trends']
    print(("\nTrending topics worldwide :"))
    for item in trends:
        print((item['name']))

def process_or_store(tweet):
    print((json.dumps(tweet,indent=1)))

def readTimeLine(api):
    # loop through the first ten items of your home timeline
    for status in tweepy.Cursor(api.home_timeline).items(10):
        # process a single status
        # print((status.text))
        process_or_store(status._json)

def getFollowersList(api):
    for friend in tweepy.Cursor(api.user_timeline).items(10):
        process_or_store(friend._json)


def getTweets(api):
    for tweet in tweepy.Cursor(api.user_timeline).items(10):
        process_or_store(tweet._json)

def getCreds():
    if not os.path.isfile(home+'/.twweet-cli/data/creds.json'):
        createCreds()
    with open(home+'/.twweet-cli/data/creds.json') as json_file:
        return json.load(json_file)

def createCreds():
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

def check_data_dir_exists():
    try:
        original_umask = os.umask(0)
        os.makedirs(home+'/.twweet-cli/data')
    except OSError:
        pass
    finally:
        os.umask(original_umask)

def home_select_action():
    option = input(
        '1.Get tweets of any user \n2.Get tweets of particular hashtag \n3.Get trending topics\n4.Read your timeline\n5.Get your followers list \n6.Get your tweets\nPress 99 to exit or press 66 to go back to main menu :: \n')
    if option == '99':
        sys.exit(0)
    if option == '66':
        print(('\n\n'))
        return False
    if option == '1':
        get_all_tweets(input('Enter the username whose twweet\'s you want to grab '))
    elif option == '2':
        words=input('Enter the hashtag or word\nyou may enter multiple words/hashtags separated by a "," : ')
        streamWordOrHashtag(wordsList=words)
        # get_tweets_of_hashtag(input('Enter the hashtag : '))
    elif option == '3':
        get_trending_topics()
    elif option == '4':
        print(('\nStreaming tweets from your TimeLine...'))
        streamYourTL()
        return False
        # readTimeLine(api)
    elif option == '5':
        getFollowersList(api)
    elif option == '6':
        getTweets(api)
    else:
        print(('please choose any of the above options\n \n'))

@decoMain
def main():
    global cfg, api
    check_data_dir_exists()
    cfg = getCreds()
    api = get_api(cfg)
    print(('Press 99 to quit the Application'))
    while True:
        option = input('Enter \'twweet\' or \'get\' or \'edit\': ')
        if option =='99':
            break
        if option == 'twweet':
            tweet = input('Enter your twweet\n')
            api.update_status(status=tweet)
            # Yes, tweet is called 'status' rather confusing
        elif option == 'get':
            check = True
            while check:
                check = home_select_action()
        elif option == 'edit':
            createCreds()
        else :
            print(('Please choose any of the above options \n \n'))

if __name__ == "__main__":
    main()
