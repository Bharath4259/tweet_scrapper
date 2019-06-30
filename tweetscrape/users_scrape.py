import logging
from datetime import datetime

from tweetscrape.tweets_scrape import TweetScrapper


class TwitterUserPopup(TweetScrapper):
    username = "5hirish"

    def __init__(self, username, request_proxies):
        self.username = username

        self.__twitter_profile_popup_url__ = 'https://twitter.com/i/profiles/popup'
        self.__twitter_profile_url__ = 'https://twitter.com/{username}'.format(username=self.username)

        self.__twitter_profile_popup_params__ = {
            'lang': 'en',
            'wants_hovercard': 'true',
        }

        self.__twitter_profile_params__ = {
            'include_available_features': 1,
            'include_entities': 1,
            'include_new_items_bar': True
        }

        self.__twitter_profile_header__ = {
            'referer': 'https://twitter.com/{username}'.format(username=self.username)
        }

        super().__init__(self.__twitter_profile_url__,
                         self.__twitter_profile_header__,
                         self.__twitter_profile_params__,
                         request_proxies,
                        1, None, None)

    def get_profile_info(self, save_output):
        output_file_name = '/' + self.username + '_profile'
        if self.username is not None and self.username != "":
            tweet_count, last_tweet_id, last_tweet_time, dump_path = \
                self.execute_twitter_request(username=self.username,
                                             log_output=save_output,
                                             log_file=None)
            return self.get_user_info()
        return ""

    def get_popup_info(self):
        self.__twitter_profile_popup_params__['_'] = int(datetime.now().timestamp())
        self.__twitter_profile_popup_params__['user_id'] = 1

        # XPATH extraction from the popup here
