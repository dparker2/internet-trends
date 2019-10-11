from requests_oauthlib import OAuth1Session
from os import environ
from json import loads


US_WOEID = 23424977


class TwitterClient(object):
    API = "https://api.twitter.com"
    TWEET_URL = f"{API}/1.1/statuses/update.json"
    TRENDS_URL = f"{API}/1.1/trends/place.json"
    SEARCH_URL = f"{API}/1.1/search/tweets.json"
    GEO_URL = f"{API}/1.1/geo/id/{{}}.json"
    TOKEN_URL = f"{API}/oauth2/token"
    OAUTH_TOKEN_URL = f"{API}/oauth/access_token"

    STREAM = "https://stream.twitter.com"
    FILTER_URL = f"{STREAM}/1.1/statuses/filter.json"

    def __init__(self):
        self.session = OAuth1Session(
            environ["TWITTER_API_KEY"],
            client_secret=environ["TWITTER_API_SECRET"],
            resource_owner_key=environ["TWITTER_TOKEN_ACCESS"],
            resource_owner_secret=environ["TWITTER_TOKEN_SECRET"],
        )

    def stream(self):
        with self.session.get(
            self.FILTER_URL,
            params=dict(
                filter_level="low",
                language="en",
                locations=[-180, -90, 180, 90],  # whole planet
            ),
            stream=True,
        ) as resp:
            for i in resp.iter_lines():
                tweet = loads(i)
                # Retweets do not have geo data, therefore tweet must be an original tweet
                if "extended_tweet" in tweet:
                    yield tweet["extended_tweet"]["full_text"]
                else:
                    yield tweet["text"]
