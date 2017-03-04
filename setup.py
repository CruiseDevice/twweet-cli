#!/usr/bin/env python

from setuptools import setup
from sys import platform as OPERATING_SYSTEM

if OPERATING_SYSTEM == "win32":
  packages = [
    'tweepy==2.3.0',
  ]
else:
  packages = [
    'tweepy==2.3.0'
  ]

setup(
  name='twweet-cli',
  version='1.0',
  description='A Twitter CLI',
  author='Akash Chavan',
  author_email='meakashchavan@gmail.com',
  url='http://github.com/CruiseDevice/twweet-cli',
  scripts=['twweet-cli.py'],
  install_requires=packages,
  entry_points = {
    'console_scripts': [
      'tt = app:main'
    ]
  }
)
