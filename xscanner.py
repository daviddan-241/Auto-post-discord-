import tweepy
from filters import is_relevant

BEARER = "AAAAAAAAAAAAAAAAAAAAADQj8wEAAAAAbNrgyqm7bPPoVa39Oz5qGJKEFUQ%3DrEB8zCcObTE2RrwVGhDCrRhh5KzDDFZEPytFNh5vrHvNaBBZUu"

client = tweepy.Client(bearer_token=BEARER)

def scan_x():
    query = "(meme OR launch OR CA: OR discord.gg) -is:retweet lang:en"

    tweets = client.search_recent_tweets(query=query, max_results=10)

    results = []

    if tweets.data:
        for t in tweets.data:
            if is_relevant(t.text):
                results.append(t.text)

    return results