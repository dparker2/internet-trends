from worker.twitter import TwitterClient
from textblob import TextBlob, download_corpora
from nltk.tokenize import TweetTokenizer
#from gensim import corpora
#from gensim.models import LdaModel
import re

def tweets_to_file():
    t = TwitterClient()
    with open('worker/tweets', 'w') as f:
        for index, tweet in enumerate(t.stream()):
            print(tweet, file=f)
            print('=-=-=-=', file=f)
            if index == 1000:
                break

def clean_tweet(tweet):
    cleaned = re.sub(r"@\S+\s?", "", tweet)  # Remove @s
    cleaned = re.sub(r"https?:\/\/\S+\s?", "", cleaned)  # Remove links
    return cleaned

def tweets_file_to_noun_phrases():
    with open('worker/tweets', 'r') as f:
        all_tweets = f.read()
    tweets = all_tweets.split('=-=-=-=')
    for tweet in tweets:
        blob = TextBlob(clean_tweet(tweet))
        np = blob.noun_phrases
        tags = [hashtag for hashtag in blob.tokenize(TweetTokenizer()) if hashtag.startswith("#")]
        if np or tags:
            yield np + tags

if __name__ == "__main__":
    download_corpora.download_lite()
    # tweets_to_file()
    documents = [text for text in tweets_file_to_noun_phrases()]
    print(documents)
    #mydict = corpora.Dictionary()
    #mycorpus = [mydict.doc2bow(doc, allow_update=True) for doc in documents]
    #print(mycorpus)
    print("worker!")
