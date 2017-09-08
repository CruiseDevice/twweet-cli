# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 01:26:52 2017
@author: Ankit Singh
"""
import yaml

##to do
#implement singleton pattern here
class ConfigurationReader(object):
    __Tweets=None
    __HashTag=None
    def __init__(self):
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        ConfigurationReader.__Tweets=cfg['Tweets']
        ConfigurationReader.__HashTag=cfg['HashTag']

    @staticmethod
    def GetTweetsStorage():
        return ConfigurationReader.__Tweets

    @staticmethod
    def GetHashTagStorage():
        return ConfigurationReader.__HashTag
