import tweepy

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def main():
  cfg = {
    "consumer_key"        : "<Your consumer_key>",
    "consumer_secret"     : "<Your consumer_secret>",
    "access_token"        : "<Your access_token>",
    "access_token_secret" : "<Your access_token_secret>"
    }

  api = get_api(cfg)
  tweet = raw_input('Enter your tweet\n')
  status = api.update_status(status=tweet)
  # Yes, tweet is called 'status' rather confusing

if __name__ == "__main__":
  main()
