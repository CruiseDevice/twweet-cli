# twweet-cli
Tweet right from your cli without even opening your browser.

[![Join the chat at https://gitter.im/twweet-cli/Lobby](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/twweet-cli/Lobby)

<!-- [![Build Status](https://travis-ci.org/CruiseDevice/twweet-cli.svg?branch=master)](https://travis-ci.org/CruiseDevice/twweet-cli) -->

## Install

### Build from Source

**Install the dependencies**

`$ pip install tweepy`

**Clone the source**

`$ git clone https://github.com/CruiseDevice/twweet-cli.git`

**Navigate to the tweet-cli folder**

`$ cd twweet-cli`

**Now run setup.py file.**

For Linux users:
`$ sudo python3 setup.py install`

For Windows users:
`$ python setup.py install`

**Create a Twitter "App"**

Log in to https://apps.twitter.com/ to create a new app and generate your OAuth credentials:

* Consumer Key (API Key)
* Consumer Secret (API Secret)
* Access Token
* Access Token Secret

**Run the application**

`$ twweet-cli`

**_Note: Requires Python 3.x_**

## Usage

* type ` twweet` to post a tweet.
* type ` get` to get different types of information from twitter. A menu will be provided to choose for your choice of             information.
* type ` edit` to change your Ouath credentials.
* type ` 99` to quit the application. 


## Contributing

I appreciate any help and support. Feel free to [fork](https://github.com/CruiseDevice/twweet-cli#fork-destination-box) and [create a pull request](https://github.com/CruiseDevice/twweet-cli/compare)

### Features present

* tweet from your CLI without opening the browser.
* Changing `Consumer Key`  `Consumer Secret`  `Access Token`  `Access Token Secret` keys for twweet-cli. 
* getting the tweets of any user by providing the username.
* getting the tweets of a particular hashtag by providing the same.
* getting the trending topics on twitter. 
* getting the tweets in your timeline.
* getting your follower list and their respective user name on twitter(number of followers to be displayed can be assigned).
* getting your own tweets(number of tweets to be displayed can be assigned).
