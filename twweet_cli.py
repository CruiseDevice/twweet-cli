import sqlite3
import tweepy
import os
import csv
import json
import sys

# Twitter API credentials
#setting up twitter bot authentication
consumer_key = '#'
consumer_secret = '#'
access_token = '#'
access_token_secret = '#'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Creating an instance to connect to the twitter api
api = tweepy.API(auth)
cfg = {}
db = './TwtApi.db'

#Change system encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')




class StreamListener(tweepy.StreamListener):
    # Decided I would keep all the overridable functions from the BaseClass so we know what we have to play with.
    def on_status(self, status):
        print '@{} => {}'.format(status.user.screen_name, status.text)

    def on_error(self, status_code):
        print 'AN ERROR'
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
    wordsList = wordsList.split(" ")
    stream = authStreamer()
    stream.filter(track=wordsList, async=True)

def decoMain(func):
    func()
    print "DONE \n"
    return func

def get_api(cfg):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def get_all_tweets(screen_name):
#    api = get_api(cfg)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name, count = 200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name, count = 200, max_id = oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far"%(len(alltweets))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str,tweet.created_at,tweet.text.encode("utf-8")]for tweet in alltweets]

    # write to csv
    with open('%s_tweets.csv' % screen_name,'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)

    pass

def editapi():
    os.remove(db)
    conn = sqlite3.connect(db)
    c=conn.cursor()
    c.execute('''CREATE TABLE ApiDetails
                    (consumer_key text, consumer_secret text, access_token text, acccess_token_secret text)''')
    cfg["consumer_key"] = raw_input('Enter your Consumer Key: ')
    cfg["consumer_secret"] = raw_input('Enter your Consumer Secret: ')
    cfg["access_token"] = raw_input('Enter your Access Token: ')
    cfg["access_token_secret"] = raw_input('Enter your Access Token Secret: ')
    c.execute("INSERT INTO ApiDetails VALUES (:consumer_key,:consumer_secret,:access_token,:access_token_secret)",cfg)
    conn.commit()
    conn.close()
    main()

#function to download the tweets of a particular hashtag
def get_tweets_of_hashtag(hash_tag):
    all_tweets = []
    new_tweets = []
    print "Please be patient while we download the tweets"

    api = get_api(cfg)
    new_tweets = tweepy.Cursor(api.search, q=hash_tag).items(200)

    while new_tweets:
        for tweet in new_tweets:
            all_tweets.append(tweet.text.encode("utf-8"))
            #max_id will be id of last tweet when loop completes. shitty wasy of doing things
            max_id = tweet.id

        print "We have got %s tweets so far" % (len(all_tweets))
        new_tweets = tweepy.Cursor(api.search, q=hash_tag).items(200)

        if (len(all_tweets)) >= 1000:
            break

    with open('%s.csv'%hash_tag, 'wb') as f:
        writer = csv.writer(f)
        for tweet in all_tweets:
            if tweet:
                writer.writerow([tweet])

    print "1000 tweets have been saved to %s.csv" % hash_tag

def get_trending_topics():

#    api = get_api(cfg)

    trends1 = api.trends_place(1) #1 for worldwide
    data = trends1[0]
    trends = data['trends']
    print "\nTrending topics worldwide :"
    for item in trends:
        print item['name']

def process_or_store(tweet):
    print(json.dumps(tweet))

def readTimeLine(api):
    for status in tweepy.Cursor(api.home_timeline).items(10):
        # process a single status
        # print(status.text)

        #lets start by making output user friendly
        process_or_store(status._json['text'])

def getFollowersList(api):
    for friend in tweepy.Cursor(api.user_timeline).items(10):
        process_or_store(friend._json)

def getTweets(api):
    for tweet in tweepy.Cursor(api.user_timeline).items(10):
        process_or_store(tweet._json)

def setupStuffICanLiveWithOut():
    if os.path.isfile(db):
        conn = sqlite3.connect(db)
        c=conn.cursor()
        c.execute("SELECT * FROM ApiDetails")
        results = c.fetchone()
        if not results:
            editapi()
        else:
            cfgdb = results
            cfg["consumer_key"] = str(cfgdb[0])
            cfg["consumer_secret"] = str(cfgdb[1])
            cfg["access_token"] = str(cfgdb[2])
            cfg["access_token_secret"] = str(cfgdb[3])
    else:
        conn = sqlite3.connect(db)
        c=conn.cursor()
        c.execute('''CREATE TABLE ApiDetails
                     (consumer_key text, consumer_secret text, access_token text, acccess_token_secret text)''')
        cfg["consumer_key"] = raw_input('Enter your Consumer Key: ')
        cfg["consumer_secret"] = raw_input('Enter your Consumer Secret: ')
        cfg["access_token"] = raw_input('Enter your Access Token: ')
        cfg["access_token_secret"] = raw_input('Enter your Access Token Secret: ')
        c.execute("INSERT INTO ApiDetails VALUES (:consumer_key,:consumer_secret,:access_token,:access_token_secret)",cfg)
        conn.commit()
        conn.close()
    api = get_api(cfg)

@decoMain
def main():
    option = raw_input('Enter \'twweet\' or \'get\' or \'edit\': ')
    if option == 'twweet':
        tweet = raw_input('Enter your twweet\n')
        api.update_status(status=tweet)
    # Yes, tweet is called 'status' rather confusing
    elif option == 'get':
        option = raw_input('1.Get tweets of any user \n2.Get tweets of particular hashtag \n3.Get trending topics\n4.Read your timeline\n5.Get your followers list\n6.Get your tweets')
        if option == '1':
            get_all_tweets(raw_input('Enter the username whose twweet\'s you want to grab '))
        elif option == '2':
            streamWordOrHashtag(wordsList=raw_input('Enter the hashtag : '))
            # get_tweets_of_hashtag(raw_input('Enter the hashtag : '))
        elif option == '3':
            get_trending_topics()
        elif option == '4':
            streamYourTL()
            #readTimeLine(api)
        elif option == '5':
            getFollowersList(api)
        elif option == '6':
            getTweets(api)
    elif option == 'edit':
        editapi()

if __name__ == "__main__":
    #streemWordOrHashtag(['#obamaday', '#KasiVibeFestival'])
    main()
