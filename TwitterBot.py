import config
import tweepy, logging
from FanboxPost import FanboxPost


class TwitterBot:

    def createFanBoxAlertTweet(self, fanbox_post):
        try:
            logging.info("{} - started OAuth1.0 flow.".format(__name__))

            text = "{} has uploaded new post on Fanbox at {}!\n{}\n{}".format(fanbox_post.artist_name,
                                                                              fanbox_post.datetime_posted,
                                                                              fanbox_post.title,
                                                                              fanbox_post.link)

            logging.info("{} - tweet content: {}.".format(__name__, text))

            auth = tweepy.OAuth1UserHandler(config.TWITTER_API_KEY, config.TWITTER_API_KEY_SECRET)
            auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            api.update_status(text)

            logging.info("{} - tweet successful.".format(__name__))
        except Exception as e:
            logging.error("{} -tweet failed for {}.".format(__name__, str(e)))


if __name__ == "__main__":
    # CODE TEST
    test_post = FanboxPost(artist_name="Artist Name", link="https://sakuraoriko.fanbox.cc/posts/3554671", title="Title",
                           datetime_posted="Date Time Posted")
    TwitterBot().createFanBoxAlertTweet(test_post)
