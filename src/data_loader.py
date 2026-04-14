import pandas as pd

def load_data():
    # Ratings
    ratings = pd.read_csv(
        "data/ml-100k/u.data",
        sep="\t",
        names=["user_id", "item_id", "rating", "timestamp"]
    )

    # Movies + genres
    columns = [
        "item_id", "title", "release_date", "video_release", "IMDb_URL",
        "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy",
        "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
        "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    ]

    movies = pd.read_csv(
        "data/ml-100k/u.item",
        sep="|",
        encoding="latin-1",
        header=None,
        names=columns
    )

    data = pd.merge(ratings, movies, on="item_id")

    return data, ratings, movies