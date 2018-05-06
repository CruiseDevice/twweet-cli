from .Twweeter import Twweeter
import os
import sys
from os.path import expanduser
from .Listener import Listener

# Twitter API credentials
home = expanduser("~")


def _decorator(f):
    f()
    print("DONE \n")
    return f


class TwweetCLI():

    def __init__(self):
        self.twweeterObj = None
        self.listenerObj = None

    def _decorator(self, f):
        self.f()
        print("DONE \n")
        return self.f

    def check_data_dir_exists(self):
        try:
            original_umask = os.umask(0)
            os.makedirs(home + '/.twweet-cli/data')
        except OSError:
            pass
        finally:
            os.umask(original_umask)

    def home_select_action(self):

        option = input(
            '''1. Get tweets of any user
            2. Get tweets of particular hashtag
            3. Get trending topics
            4. Read your timeline
            5. Get your followers list
            6. Get your tweets
            Press 99 to exit or press 66 to go back to main menu :: ''')
        if option == '99':
            sys.exit(0)
        if option == '66':
            print(('\n\n'))
            return False
        if option == '1':
            self.twweeterObj.get_all_tweets(input('Enter the username whose twweet\'s you want to grab '))
        elif option == '2':
            words = input('Enter the hashtag or word\nyou may enter multiple words/hashtags separated by a "," : ')
            self.listenerObj.streamWordOrHashtag(wordsList=words)
            # get_tweets_of_hashtag(input('Enter the hashtag : '))
        elif option == '3':
            self.twweeterObj.get_trending_topics()
        elif option == '4':
            print(('\nStreaming tweets from your TimeLine...'))
            self.listenerObj.streamYourTL()
            return False
            # readTimeLine(api)
        elif option == '5':
            self.twweeterObj.getFollowersList()
        elif option == '6':
            self.twweeterObj.getTweets()
        else:
            print(('please choose any of the above options\n \n'))


    def main(self):
        self.twweeterObj = Twweeter()
        self.listenerObj = Listener(self.twweeterObj)
        self.check_data_dir_exists()
        print("_____________      __  __      ___________________________________\n\__    ___/  \    /  \/  \    /  \_   _____/\_   _____/\__    ___/\n  |    |  \   \/\/   /\   \/\/   /|    __)_  |    __)_   |    |     ______ \n  |    |   \        /  \        / |        \ |        \  |    |    /_____/ \n  |____|    \__/\  /    \__/\  / /_______  //_______  /  |____| \n                 \/          \/          \/         \/ \n_________ .____    .___ \n\_   ___ \|    |   |   | \n/    \  \/|    |   |   | \n\     \___|    |___|   | \n \______  /_______ \___| \n        \/        \/ \n")
        print('Press 99 to quit the Application')
        while True:
            option = input('Enter \'twweet\' or \'get\' or \'edit\': ')
            if option == '99':
                break
            if option == 'twweet':
                tweet = input('Enter your twweet\n')
                if len(tweet) >= 140:
                    print("Tweet length exceeds the limit of 140 characters!")
                    continue
                self.twweeterObj.api.update_status(status=tweet)
                # Yes, tweet is called 'status' rather confusing
            elif option == 'get':
                check = True
                while check:
                    check = self.home_select_action()
            elif option == 'edit':
                self.twweeterObj.createCreds()
            else:
                print('Please choose any of the above options \n \n')


def cli():
    Tww = TwweetCLI()
    Tww.main()


if __name__ == "__main__":
    cli()
