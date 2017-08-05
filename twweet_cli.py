import tweepy
import os
import csv
import json
import errno

# Twitter API credentials
cfg = {}

def get_api(cfg):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def get_all_tweets(screen_name):
    api = get_api(cfg)

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

    api = get_api(cfg)

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
        process_or_store(status._json)

def getFollowersList(api):
    for friend in tweepy.Cursor(api.user_timeline).items(10):
        process_or_store(friend._json)

def getTweets(api):
    for tweet in tweepy.Cursor(api.user_timeline).items(10):
        process_or_store(tweet._json)

def getCreds():
    if not os.path.isfile('data/creds.json'):
        createCreds()
    with open('data/creds.json') as json_file:
        return json.load(json_file)

def createCreds():
    ck = raw_input('Enter your Consumer Key: ').strip()
    cs = raw_input('Enter your Consumer Secret: ').strip()
    at = raw_input('Enter your Access Token: ').strip()
    ats = raw_input('Enter your Access Token Secret: ').strip()
    jsondata= {"consumer_key": ck,
    "consumer_secret": cs,
    "access_token": at,
    "access_token_secret": ats}
    with open("data/creds.json", "w") as outfile:
        json.dump(jsondata, outfile)

def check_data_dir_exists():
    try:
        os.makedirs('./data')
    except OSError:
        pass

def main():
    global cfg
    check_data_dir_exists()
    cfg = getCreds()
    api = get_api(cfg)
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
            get_tweets_of_hashtag(raw_input('Enter the hashtag : '))
        elif option == '3':
            get_trending_topics()
        elif option == '4':
            readTimeLine(api)
        elif option == '5':
            getFollowersList(api)
        elif option == '6':
            getTweets(api)
    elif option == 'edit':
        createCreds()

if __name__ == "__main__":
    main()
