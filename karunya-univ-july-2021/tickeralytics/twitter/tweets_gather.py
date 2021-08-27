import pickle

import twint

TWITTER_HANDLES = {"spacguru", "satorimind", "daddyspac", "malibuinvest","thethawarrior","spachero2", "spac_insider", "spacresearch",
                   "mrzackmorris", "thetawarrior", "traderstewie", "malibuinvest"}

TWEETS_LIMIT = 10000

class Twint():
    def __init__(self):
        pass

    def get_tweets(self, username):
        twitter_config = twint.Config()
        twitter_config.Username = username
        twitter_config.Limit = TWEETS_LIMIT
        twitter_config.Store_csv = True
        twitter_config.Output = "test.csv"
        twitter_config.Store_object = True
        # Run
        try:
            twint.run.Search(twitter_config)
        except:
            print("handled####")
        tweets = twint.output.tweets_list

        return tweets

if __name__ == '__main__':
    t = Twint()
    for handle in TWITTER_HANDLES:
        tweets = t.get_tweets(handle)
        print('########################')
        # print(tweets)
        print(type(tweets))
        print('########################')
        # with open("twitter_notes.txt","wb") as f:
        #     for tweet in tweets:
        #         f.write(tweet)
        with open(f"{handle}_tweets.pickle", "wb") as dump_file:
            pickle.dump(tweets, dump_file)
