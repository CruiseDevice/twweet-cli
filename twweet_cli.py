import sqlite3
import tweepy
import os
import csv

# Twitter API credentials
cfg = {
   "consumer_key"        : "",
   "consumer_secret"     : "",
   "access_token"        : "",
   "access_token_secret" : ""
   }
db = './TwtApi.db'

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
    conn.close
    main()

def main():
  
    if os.path.isfile(db):
       conn = sqlite3.connect(db)
       c=conn.cursor()
       c.execute("SELECT * FROM ApiDetails")
       cfgdb = list(c.fetchone())
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
       conn.close       
    api = get_api(cfg)

    option = raw_input('Enter \'twweet\' or \'get\' or \'edit\': ')
    if option == 'twweet':
        tweet = raw_input('Enter your twweet\n')
        # Yes, tweet is called 'status' rather confusing
    elif option == 'get':
        get_all_tweets(raw_input('Enter the username whose twweet\'s you want to grab '))
    elif option == 'edit':
        editapi()
       
if __name__ == "__main__":
  main()

			
