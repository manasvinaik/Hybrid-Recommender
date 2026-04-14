class HybridRecommender:
    def __init__(self, collab_model, content_model, movies, alpha=0.7):
        self.collab = collab_model
        self.content = content_model
        self.movies = movies
        self.alpha = alpha

    def recommend(self, user_id, data, top_n=5):
        all_movies = data['item_id'].unique()
        scores = []

        for movie_id in all_movies:
            collab_score = self.collab.predict(user_id, movie_id)

            final_score = self.alpha * collab_score

            scores.append((movie_id, final_score))

        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for movie_id, score in scores[:top_n]:
            title = self.movies[
                self.movies['item_id'] == movie_id
            ]['title'].values[0]

            results.append((title, round(score, 2)))

        return results