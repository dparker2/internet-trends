from worker.twitter import TwitterClient
from textblob import TextBlob, download_corpora
import re

if __name__ == "__main__":
    download_corpora.download_lite()
    t = TwitterClient()
    for tweet in t.stream():
        print(TextBlob(re.sub(r"@\S+\s", "", tweet)).noun_phrases)
    print("worker!")
