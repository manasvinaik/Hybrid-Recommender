from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

class CollaborativeModel:
    def __init__(self, data):
        self.data = data
        self.model = SVD()

    def train(self):
        reader = Reader(rating_scale=(1, 5))

        dataset = Dataset.load_from_df(
            self.data[['user_id', 'item_id', 'rating']], reader
        )

        trainset, testset = train_test_split(dataset, test_size=0.2)

        self.model.fit(trainset)

    def predict(self, user_id, item_id):
        return self.model.predict(user_id, item_id).est