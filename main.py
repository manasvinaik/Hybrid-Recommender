from src.data_loader import load_data
from src.collaborative import CollaborativeModel
from src.content_based import ContentModel
from src.hybrid import HybridRecommender

data, ratings, movies = load_data()

collab = CollaborativeModel(data)
collab.train()

content = ContentModel(data)
content.train()

hybrid = HybridRecommender(collab, content, movies)