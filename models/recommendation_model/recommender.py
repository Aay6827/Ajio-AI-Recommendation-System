import os
import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ProductRecommender:

    def __init__(self, csv_path):
        """
        Initialize recommender system
        """
        self.csv_path = csv_path

        # Get database URL from environment (Docker)
        self.db_url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://postgres:admin123@db:5432/ajio"
        )

        # Create database engine
        self.engine = create_engine(self.db_url)

        # Load and process data
        self.load_data()


    def load_data(self):
        """
        Load product data and store in PostgreSQL
        """

        # Load CSV data
        self.products = pd.read_csv(self.csv_path)

        # Combine product features for recommendation
        self.products["features"] = (
            self.products["name"].fillna("") + " " +
            self.products["brand"].fillna("") + " " +
            self.products["category"].fillna("")
        )

        # Only insert into DB if table is empty or doesn't exist
        with self.engine.connect() as conn:
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM products"))
                count = result.scalar()
                if count == 0:
                    self.products.to_sql(
                        "products",
                        self.engine,
                        if_exists="replace",
                        index=False
                    )
            except Exception:
                # Table doesn't exist yet, create it
                self.products.to_sql(
                    "products",
                    self.engine,
                    if_exists="replace",
                    index=False
                )

        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words="english")

        # Convert text → vectors
        self.tfidf_matrix = self.vectorizer.fit_transform(self.products["features"])

        # Compute similarity matrix
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)


    def recommend(self, product_name, top_n=5):
        """
        Recommend similar products
        """

        # Case-insensitive product search
        match = self.products[
            self.products["name"].str.lower() == product_name.lower()
        ]

        if match.empty:
            return []

        # Get index of product
        idx = match.index[0]

        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[idx]))

        # Sort by similarity (descending)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Skip the first one (itself) and get top_n
        sim_scores = sim_scores[1:top_n + 1]

        product_indices = [i[0] for i in sim_scores]

        return self.products["name"].iloc[product_indices].tolist()






