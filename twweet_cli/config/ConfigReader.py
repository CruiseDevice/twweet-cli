# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 01:26:52 2017
@author: Ankit Singh
"""
import yaml
from os.path import expanduser

##to do
ymlPath=expanduser("~")
#implement singleton pattern here
class ConfigurationReader(object):
    __Tweets=None
    __HashTag=None
    def __init__(self):
        with open(ymlPath+'/.twweet-cli/data/config.yml', 'r') as ymlfile:
             cfg = yaml.load(ymlfile)
        ConfigurationReader.__Tweets=cfg['Tweets']
        ConfigurationReader.__HashTag=cfg['HashTag']

    @staticmethod
    def get_tweets_storage():
        return ConfigurationReader.__Tweets

    @staticmethod
    def get_hashtag_storage():
        return ConfigurationReader.__HashTag
