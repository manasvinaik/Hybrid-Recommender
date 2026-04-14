import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class ContentModel:
    def __init__(self, data):
        self.data = data

    def train(self):
        self.user_movie_matrix = self.data.pivot_table(
            index='user_id',
            columns='title',
            values='rating'
        )

        movie_similarity = cosine_similarity(
            self.user_movie_matrix.fillna(0).T
        )

        self.similarity_df = pd.DataFrame(
            movie_similarity,
            index=self.user_movie_matrix.columns,
            columns=self.user_movie_matrix.columns
        )

    def get_similar_movies(self, movie):
        return self.similarity_df[movie].sort_values(ascending=False)