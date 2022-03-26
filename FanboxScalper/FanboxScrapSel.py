import logging
from FanboxScalper import config
from FanboxScalper.FanboxPost import FanboxPost
from TweetBot.TwitterBot import TwitterBot
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


class FanboxScrapSel:
    def __init__(self):
        self.seen_posts = self.dataPreparation()
        self.new_posts = []

    def fanboxScrapProcess(self):
        self.getRecentPosts(config.FANBOX_URL)
        self.publishNewPosts()
        self.updateRecord()

    def dataPreparation(self):
        logging.info("{} - data Preparation starting.".format(__name__))
        try:
            return set(line.strip() for line in open(config.FANBOX_SEEN_POST_FILENAME, 'r'))
        except:
            return set()

    def updateRecord(self):
        logging.info("{} - preparing to update records.".format(__name__))
        file = open(config.FANBOX_SEEN_POST_FILENAME, 'a')
        [file.write(new_post.link + '\n') for new_post in self.new_posts]
        file.close()
        self.new_posts.clear()
        logging.info("{} - record updated successfully.".format(__name__))

    def getRecentPosts(self, url):
        logging.info("{} - executing fetch request to url: {}.".format(__name__, url))
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.implicitly_wait(10)

        try:
            driver.get(config.FANBOX_URL)
            driver.refresh()

            raw_posts = None
            artist_name = None

            for try_count in range(0, config.MAXIMUM_RETRY):
                try:
                    raw_posts = driver.find_elements_by_class_name(config.FANBOX_POST_CLASS_NAME)
                    break
                except StopIteration as e:
                    continue

            for try_count in range(0, config.MAXIMUM_RETRY):
                try:
                    artist_name = next(
                        elem.text for elem in driver.find_elements_by_class_name(config.FANBOX_ARTIST_CLASS_NAME) if
                        elem.text)
                    break
                except StopIteration as e:
                    continue

            for raw_post in reversed(raw_posts):  # this will be in reversed order.
                if raw_post.get_attribute("href") not in self.seen_posts:
                    # NOTE the magic number for index.
                    post = FanboxPost(artist_name=artist_name, link=raw_post.get_attribute("href"),
                                      title=raw_post.text.splitlines()[3],
                                      datetime_posted=raw_post.text.splitlines()[1])
                    logging.info("{} - found new post: {}, calling Twitter bot".format(__name__, post))
                    self.seen_posts.add(post.link)
                    self.new_posts.append(post)
        except NoSuchElementException as e:
            logging.error("{} - NOSuchElement. Fetch request failed for {}".format(__name__, str(e)))
        except Exception as e:
            logging.error("{} - fetch request failed for {}".format(__name__, str(e)))
        finally:
            logging.info("{} - getRecentPosts successful.".format(__name__))
            driver.quit()

    def find(self, driver, className):
        element = driver.find_elements_by_class_name(className)
        if element:
            return element
        else:
            return False

    def publishNewPosts(self):
        for post in self.new_posts:  # as new_posts were added in reversed order, they will be posted from old to new.
            TwitterBot().createFanBoxAlertTweet(post)


if __name__ == "__main__":
    # CODE TEST
    fbs = FanboxScrapSel()
    fbs.fanboxScrapProcess()
