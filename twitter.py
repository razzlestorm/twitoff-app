"""Retrieve Tweets, embeddings, and persist in the database."""
import basilica
from decouple import config
from .models import DB, Tweet, User
import tweepy

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                config('TWITTER_CONSUMER_SECRET'))

TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                            config('TWITTER_ACCESS_TOKEN_SECRET'))

TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))


def embedded_tweet_to_db(t_user):
    """
    Gets the tweets of a user and appends their latest 200 tweets (excluding
    retweets and replies) to the database. Appends the id, text,
    basilica embedding, and Twitter user ID in that order to the DB.

    Only needs the twitter handle as an argument.
    """
    tweets = t_user.timeline(count=200, exclude_replies=True,
                            include_rts=False, tweet_mode='extended')

    db_user = User(id=t_user.id, handle=t_user.screen_name,
                name=t_user.name, newest_tweet_id=tweets[0].id)

    for tweet in tweets:
        embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300],
                        embedding=embedding)
        DB.session.add(db_tweet)
        db_user.tweets.append(db_tweet)
    DB.session.add(db_user)
    DB.session.commit()
