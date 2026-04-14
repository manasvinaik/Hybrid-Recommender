import pandas as pd

class ColdStartRecommender:
    def __init__(self, content_model):
        self.content = content_model

    def recommend(self, user_ratings, top_n=5):
        scores = pd.Series(dtype=float)

        for movie, rating in user_ratings.items():
            if movie not in self.content.similarity_df:
                continue

            similar_movies = self.content.get_similar_movies(movie)

            scores = scores.add(similar_movies * rating, fill_value=0)

        # remove already rated movies
        for movie in user_ratings:
            if movie in scores:
                scores.drop(movie, inplace=True)

        return scores.sort_values(ascending=False).head(top_n)