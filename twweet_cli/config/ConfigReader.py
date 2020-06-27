import yaml
import os
from os.path import expanduser

home = expanduser("~")


class ConfigurationReader(object):
    __tweets = None
    __hashtag = None

    def __init__(self):
        ymlfile = home + '/.twweet-cli/data/config.yml'
        if os.path.isfile(ymlfile):
            with open(ymlfile, 'r') as file:
                cfg = yaml.load(file)
            ConfigurationReader.__tweets = cfg['Tweets']
            ConfigurationReader.__hashtag = cfg['HashTag']
        else:
            if not os.path.exists(home + '/.twweet-cli/data'):
                os.makedirs(home + '/.twweet-cli/data')

            with open(home + '/.twweet-cli/data/config.yml', 'w') as ymlfile:
                ymlLine1 = "#Depending on the system(Windows or Linux) change the\
                                 backward or forward slash appropriately."
                ymlLine2 = "Tweets: /TweetsStore/"
                ymlLine3 = "HashTag: /HashTagStore/"
                ymlfile.write("%s\n%s\n%s\n" % (ymlLine1, ymlLine2, ymlLine3))

    @staticmethod
    def get_tweets_storage():
        return ConfigurationReader.__tweets

    @staticmethod
    def get_hashtag_storage():
        return ConfigurationReader.__hashtag
