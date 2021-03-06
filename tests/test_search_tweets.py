import pytest
import os
import csv
import ast
from datetime import datetime
from tweetscrape.search_tweets import TweetScrapperSearch


@pytest.mark.parametrize("test_term,test_page", [
        ("New York", 40),
        ("White House", 60),
        ("Avengers Infinity War", 100),
        # ("Machine Learning", 10),
        # ("The Rock", 15)
    ])
def test_search_tweets(test_term, test_page):

    ts = TweetScrapperSearch(search_all=test_term,
                             num_tweets=test_page,
                             tweet_dump_path='twitter.csv',
                             tweet_dump_format='csv')

    tweet_count, tweet_id, last_time, dump_path = ts.get_search_tweets()

    assert os.path.exists(dump_path)

    # assert tweet_count > (test_page - 1) * 20
    assert tweet_count >= 5

    with open(dump_path, 'r') as csv_fp:
        csv_reader = csv.DictReader(csv_fp)
        for tweets in csv_reader:
            assert tweets.get('id') is not None
            assert tweets.get('text') is not None
            assert tweets.get('time') is not None

    os.remove(dump_path)


@pytest.mark.parametrize("test_tag,test_page", [
        ("#StarWars", 60),
        ("#FakeNews", 120),
        # ("#Hamilton", 5),
        # ("#MarchForOurLives", 1),
        # ("#CNN", 12)
    ])
def test_hashtag_tweets(test_tag, test_page):

    ts = TweetScrapperSearch(search_hashtags=test_tag,
                             num_tweets=test_page,
                             tweet_dump_path='twitter.csv',
                             tweet_dump_format='csv')

    tweet_count, tweet_id, last_time, dump_path = ts.get_search_tweets()

    assert os.path.exists(dump_path)

    # assert tweet_count >= (test_page - 1) * 20
    assert tweet_count >= 5

    with open(dump_path, 'r') as csv_fp:
        csv_reader = csv.DictReader(csv_fp)
        for tweets in csv_reader:
            assert tweets.get('id') is not None
            assert tweets.get('text') is not None
            assert tweets.get('time') is not None
            assert tweets.get('hashtags') is not None
            assert len(ast.literal_eval(tweets.get('hashtags'))) > 0
            # extracted_hastags = [ht.lower() for ht in ast.literal_eval(tweets.get('hashtags'))]
            # assert test_tag.lower() in extracted_hastags

    os.remove(dump_path)


@pytest.mark.parametrize("test_until,test_since,test_from,test_page", [
        # ("2019-03-01", "2019-01-01", "@BarackObama", 100),
        ("2016-04-01", "2015-11-01", "@CNN", 40),
        ("2017-08-01", "2017-07-01", "@BBC", 40),
        ("2012-01-01", "2011-12-20", "@ABC", 40)
    ])
def test_time_interval_tweets(test_until, test_since, test_from, test_page):
    ts = TweetScrapperSearch(search_from_accounts=test_from,
                             search_till_date=test_until,
                             search_since_date=test_since,
                             num_tweets=test_page,
                             tweet_dump_path='twitter.csv',
                             tweet_dump_format='csv')

    tweet_count, tweet_id, last_time, dump_path = ts.get_search_tweets()

    since_timestamp = datetime.strptime(test_since, '%Y-%m-%d').timestamp()
    until_timestamp = datetime.strptime(test_until, '%Y-%m-%d').timestamp()

    assert os.path.exists(dump_path)

    assert tweet_count == pytest.approx(test_page, abs=5)

    with open(dump_path, 'r') as csv_fp:
        csv_reader = csv.DictReader(csv_fp)
        for tweets in csv_reader:
            assert tweets.get('id') is not None
            assert tweets.get('text') is not None
            assert tweets.get('time') is not None
            # tweet_time = int(tweets.get('time')) / 1000
            # assert until_timestamp >= tweet_time >= since_timestamp

    os.remove(dump_path)