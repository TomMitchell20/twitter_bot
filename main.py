import tweepy
import facts
import keys
import random
import time

filename = 'last_id.txt'

class Twitter_API:

    def get_auth(self, consumer_api_key, api_secret_key):

        self.consumer_api_key = consumer_api_key
        self.api_key = api_secret_key

        auth = tweepy.OAuthHandler(consumer_api_key, api_secret_key)

        return auth

    def set_access_tokens(self, access_tokens, access_token_secret):

        self.access_tokens = access_tokens
        self.access_token_secret = access_token_secret

        auth = self.get_auth(keys.consumer_api_key, keys.API_secret_key)

        auth.set_access_token(access_tokens, access_token_secret)

        return auth

    def get_twitter_api(self):

        auth = self.set_access_tokens(keys.access_token, keys.access_token_secret)

        return tweepy.API(auth)

    def get_mentions(self, twitter_api, last_id):
        self.twitter_api = twitter_api
        self.last_id = last_id

        mentions = twitter_api.mentions_timeline(last_id)

        return mentions

    def save_last_id(self, latest_id, filename):
        self.latest_id = latest_id
        self.filename = filename

        f_write = open(filename, 'w')
        f_write.write(str(latest_id))
        f_write.close()

    def retrieve_last_id(self, filename):
        self.filename = filename

        f_open = open(filename, 'r')
        last_id = int(f_open.read().strip())
        f_open.close()
        return last_id

    def run(self):
        api = self.get_twitter_api()
        try:
            last_id = self.retrieve_last_id(filename)
            mentions = self.get_mentions(api, last_id)
        except:
            mentions = self.get_mentions(api, None)

        for mention in reversed(mentions):
            if 'fact' in mention.text.lower():
                last_id = mention.id
                message = '@' + mention.user.screen_name + ' ' + str(random.choice(facts.random_facts))
                self.save_last_id(last_id, filename)
                api.update_status(message)


while True:
    api = Twitter_API()
    api.run()
    time.sleep(5)