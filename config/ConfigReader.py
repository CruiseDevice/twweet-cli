# -*- coding: utf-8 -*-
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
    def GetTweetsStorage():
        return ConfigurationReader.__Tweets
    
    @staticmethod
    def GetHashTagStorage():
        return ConfigurationReader.__HashTag
    

