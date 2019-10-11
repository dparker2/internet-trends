from worker.twitter import TwitterClient
from textblob import TextBlob, download_corpora

if __name__ == "__main__":
    download_corpora.download_lite()
    t = TwitterClient()
    for tweet in t.stream():
        print(TextBlob(tweet).noun_phrases)
    print("worker!")
