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
        self.twweeter_obj = None
        self.listener_obj = None

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
            self.twweeter_obj.get_all_tweets(input('Enter the username whose twweet\'s you want to grab '))
        elif option == '2':
            words = input('Enter the hashtag or word\nyou may enter multiple words/hashtags separated by a "," : ')
            self.listener_obj.stream_word_or_hashtag(words_list=words)
            # get_tweets_of_hashtag(input('Enter the hashtag : '))
        elif option == '3':
            self.twweeter_obj.get_trending_topics()
        elif option == '4':
            print(('\nStreaming tweets from your TimeLine...'))
            self.listener_obj.stream_your_tl()
            return False
            # read_timeline(api)
        elif option == '5':
            self.twweeter_obj.get_followers_list()
        elif option == '6':
            self.twweeter_obj.get_tweets()
        else:
            print(('please choose any of the above options\n \n'))

    def main(self):
        self.twweeter_obj = Twweeter()
        self.listener_obj = Listener(self.twweeter_obj)
        self.check_data_dir_exists()
        print(""" 
_____________      __  __      ___________________________________
\__    ___/  \    /  \/  \    /  \_   _____/\_   _____/\__    ___/
  |    |  \   \/\/   /\   \/\/   /|    __)_  |    __)_   |    |     ______ 
  |    |   \        /  \        / |        \ |        \  |    |    /_____/ 
  |____|    \__/\  /    \__/\  / /_______  //_______  /  |____| 
                 \/          \/          \/         \/ 
_________ .____    .___ 
\_   ___ \|    |   |   | 
/    \  \/|    |   |   | 
\     \___|    |___|   | 
 \______  /_______ \___| 
        \/        \/ 
        """)
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
                self.twweeter_obj.api.update_status(status=tweet)
                # Yes, tweet is called 'status' rather confusing
            elif option == 'get':
                check = True
                while check:
                    check = self.home_select_action()
            elif option == 'edit':
                self.twweeter_obj.create_creds()
            else:
                print('Please choose any of the above options \n \n')


def cli():
    tww = TwweetCLI()
    tww.main()


if __name__ == "__main__":
    cli()
