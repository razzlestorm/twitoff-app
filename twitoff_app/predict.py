"""Prediction of Users based on Tweet embeddings."""
import numpy as np
from sklearn.neighbors import NearestNeighbors
from .models import User
from .twitter import BASILICA


def predict_user(user1_handle, user2_handle, tweet_text):
    """Determine and return which user is more likely to say a given Tweet.

    # Arguments
        user1_handle: str, twitter user handle for user1 in comparison
        user1_handle: str, twitter user handle for user2 in comparison
        tweet_text: str, tweet text to evaluate
    # Returns
        True if user1 has at least one tweet that is closer (measured in cosine similarity) to the sample tweet.
        False otherwise
    """
    user1 = User.query.filter(User.handle == user1_handle).one()
    user2 = User.query.filter(User.handle == user2_handle).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    user1_neigh = NearestNeighbors(metric='cosine').fit(user1_embeddings)
    user2_neigh = NearestNeighbors(metric='cosine').fit(user2_embeddings)
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    tweet_embedding = np.array(tweet_embedding).reshape(1, -1)
    user_1_neigh_dist, _ = user1_neigh.kneighbors(X=tweet_embedding, n_neighbors=1)
    user_2_neigh_dist, _ = user2_neigh.kneighbors(X=tweet_embedding, n_neighbors=1)
    user_1_neigh_dist = user_1_neigh_dist[0][0]
    user_2_neigh_dist = user_2_neigh_dist[0][0]
    return user_1_neigh_dist > user_2_neigh_dist
