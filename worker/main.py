from worker.twitter import TwitterClient
from textblob import TextBlob, download_corpora
from textblob.en.np_extractors import FastNPExtractor
from textblob.en.taggers import PatternTagger, NLTKTagger
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim import corpora
from gensim.models import LdaModel
from gensim.models.phrases import Phrases, Phraser
from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation
import re
import nltk
import stanfordnlp


def tweets_to_file():
    t = TwitterClient()
    with open("worker/tweets", "w") as f:
        for index, tweet in enumerate(t.stream()):
            print(tweet, file=f)
            print("=-=-=-=", file=f)
            if index == 20000:  # bit much
                break


def clean_tweet(tweet):
    print(tweet)
    cleaned = re.sub(r"https?:\/\/\S+\s?", "", tweet)  # Remove links
    stop_words = set(stopwords.words("english"))
    cleaned = " ".join(
        filter(lambda word: word.lower() not in stop_words, cleaned.split(" "))
    )
    print(cleaned)
    return cleaned


import nltk.tag, nltk.data
from nltk.corpus import brown

brown_tagged_sents = brown.tagged_sents(categories="news")
unigram_tagger = nltk.UnigramTagger(
    brown_tagged_sents, backoff=nltk.tag.DefaultTagger("NN")
)
bigram_tagger = nltk.BigramTagger(brown_tagged_sents, backoff=unigram_tagger)
tagger = nltk.tag.RegexpTagger(
    [(r"^#.+$", "HT"), (r"^https?:\/\/.+", "LINK")], backoff=bigram_tagger
)

stanfordnlp.download("en", "./worker", force=True)
nlp = stanfordnlp.Pipeline(
    "tokenize,pos", models_dir="./worker", tokenize_pretokenized=True
)


def tweets_file_to_documents():
    with open("worker/tweets", "r") as f:
        all_tweets = f.read()
    tokenizer = TweetTokenizer(strip_handles=True)
    # stop_words = set(stopwords.words("english"))
    # tweets = [
    #     [
    #         word
    #         for word in TweetTokenizer(strip_handles=True).tokenize(tweet)
    #         if re.match("^[a-zA-Z\d#].*", word)
    #     ]
    #     for tweet in all_tweets.split("=-=-=-=")
    # ]
    tweets = "\n\n".join(
        [
            " ".join(tokenizer.tokenize(re.sub(r"https?:\/\/\S+", "", tweet)))
            for tweet in all_tweets.split("=-=-=-=")
        ]
    )
    doc = nlp(tweets)
    tokens_tags = [
        [
            (word.text, "HT" if re.match(r"#\S+", word.text) else word.upos)
            for word in sent.words
        ]
        for sent in doc.sentences
    ]
    # exit()
    # phraser = Phraser(Phrases(tweets))  # this is not doing noun phrases properly
    # tweets = [phraser[tweet] for tweet in tweets]
    # for t in tweets:
    #     print(t)
    # tokens_tags = [tagger.tag(tweet) for tweet in tweets]
    # print(tokens_tags)
    # exit()
    patterns = """
    CHUNK:
        {<HT>}
        {<PROPN><PROPN>*}
        {<DET|PRON>?<ADJ>*<NOUN>}
    """  # Third doesn't work well. Picks up too many things.
    chunker = nltk.RegexpParser(patterns)
    nps = [chunker.parse(tokens_tag) for tokens_tag in tokens_tags]
    for tree in nps:
        leaves = [
            " ".join([word for word, _ in subtree.leaves()])
            for subtree in tree.subtrees(filter=lambda t: t.label() == "CHUNK")
        ]
        yield leaves
    # lemmatizer = WordNetLemmatizer()
    # tweet_matrix = [tweet.split(" ") for tweet in tweets]
    # bigram = Phrases(tweet_matrix)
    # for tweet in tweet_matrix:
    #     with_phrases = bigram[tweet]
    #     tokenized = tokenizer.tokenize(clean_tweet(" ".join(with_phrases)))
    #     lemmed = [lemmatizer.lemmatize(token) for token in tokenized]
    #     yield lemmed


if __name__ == "__main__":
    download_corpora.download_lite()
    nltk.download("stopwords")
    # tweets_to_file()
    # exit()
    documents = [doc for doc in tweets_file_to_documents()]
    # for document in documents:
    #     print(document)
    # for document in documents:
    #     print(" ".join(document))
    # print(documents)
    mydict = corpora.Dictionary()
    mycorpus = [mydict.doc2bow(doc, allow_update=True) for doc in documents]
    # print(mycorpus)
    lda = LdaModel(
        mycorpus,
        num_topics=100,
        id2word=mydict,
        passes=5,
        alpha="auto",
        eta="auto",
        decay=1,
    )
    score_topics = [
        tuple(zip(*topic[1]))
        for topic in lda.show_topics(num_topics=100, num_words=5, formatted=False)
    ]
    score_topics = sorted(
        map(lambda t: (sum(t[1]), t[0]), score_topics), key=lambda t: t[0], reverse=True
    )
    for score, topics in score_topics:
        if score > 0.05:  # Maybe move this up?
            print(topics)

    print("worker!")
