import tweepy

'''STREAM'''


class StreamListener(tweepy.StreamListener):
    # Decided I would keep all the overridable functions from the 
    # BaseClass so we know what we have to play with.
    def __init__(self, twweeter_obj, time_limit=60):
        self.twweeter_obj = twweeter_obj
        super(StreamListener, self).__init__(self.twweeter_obj.api)

    def on_status(self, status):
        print('@{} => {}'.format(status.user.screen_name,
                                 status.text.replace("\n", " ")))

    def on_error(self, status_code):
        print('AN ERROR: {}'.format(status_code))
    #   read the docs and handle different errors

    def keep_alive(self):
        """Called when a keep-alive arrived"""
        return

    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        return

    def on_delete(self, status_id, user_id):
        """Called when a delete notice arrives for a status"""
        return

    def on_event(self, status):
        """Called when a new event arrives"""
        return

    def on_direct_message(self, status):
        """Called when a new direct message arrives"""
        return

    def on_friends(self, friends):
        """Called when a friends list arrives.

        friends is a list that contains user_id
        """
        return

    def on_limit(self, track):
        """Called when a limitation notice arrives"""
        return

    def on_timeout(self):
        """Called when stream connection times out"""
        return

    def on_disconnect(self, notice):
        """Called when twitter sends a disconnect notice

        Disconnect codes are listed here:
        https://dev.twitter.com/docs/streaming-apis/\
        messages#Disconnect_messages_disconnect
        """
        return

    def on_warning(self, notice):
        """Called when a disconnection warning message arrives"""
        return


class Listener():

    def __init__(self, twweeter_obj):
        self.twweeter_obj = twweeter_obj
        self.stream_listener_ob = StreamListener(self.twweeter_obj)

    # authorise the StreamListener
    def auth_streamer(self):
        stream = tweepy.Stream(auth=self.twweeter_obj.api.auth,
                               listener=self.stream_listener_ob)
        return stream

    # listen for tweets containing a specific word or hashtag \
    #(a phrase might work too)
    def stream_word_or_hashtag(self, words_list):
        stream = self.auth_streamer()
        stream.filter(track=words_list, is_async=True)


'''END STREAM'''
