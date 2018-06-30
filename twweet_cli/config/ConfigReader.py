# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 01:26:52 2017
@author: Ankit Singh
"""
import yaml
from os.path import expanduser

##to do
yml_path = expanduser("~")
#implement singleton pattern here
class ConfigurationReader(object):
    __tweets = None
    __hashtag = None
    def __init__(self):
        with open(yml_path + '/.twweet-cli/data/config.yml', 'r') as ymlfile:
             cfg = yaml.load(ymlfile)
        ConfigurationReader.__tweets = cfg['tweets']
        ConfigurationReader.__hashtag = cfg['hashtag']

    @staticmethod
    def get_tweets_storage():
        return ConfigurationReader.__tweets

    @staticmethod
    def get_hashtag_storage():
        return ConfigurationReader.__hashtag
