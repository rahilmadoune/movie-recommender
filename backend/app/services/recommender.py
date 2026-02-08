import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from app.models import Movie, SessionLocal

class MovieRecommender:
    """AI-powered movie recommendation engine using content-based filtering"""
    
    def __init__(self):
        self.df = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.vectorizer = None
        
    def load_movies_from_db(self) -> pd.DataFrame:
        """Load all movies from database into DataFrame"""
        db = SessionLocal()
        try:
            movies = db.query(Movie).all()
            data = [movie.to_dict() for movie in movies]
            self.df = pd.DataFrame(data)
            return self.df
        finally:
            db.close()
    
    def create_content_features(self, movie: Dict) -> str:
        """
        Create a text representation of movie content for similarity calculation.
        Combines: genres, overview, actors, director
        """
        features = []
        
        # Genres (high weight - most important)
        if movie.get("genres"):
            genres = " ".join(movie["genres"]) * 3  # Triple weight
            features.append(genres)
        
        # Overview/Plot (medium weight)
        if movie.get("overview"):
            features.append(movie["overview"])
        
        # Actors (medium weight)
        if movie.get("actors"):
            actors = " ".join(movie["actors"]) * 2
            features.append(actors)
        
        # Director (lower weight)
        if movie.get("director"):
            features.append(movie["director"])
        
        return " ".join(features)
    
    def build_similarity_matrix(self):
        """Build TF-IDF matrix and calculate cosine similarity"""
        print("🧠 Building AI recommendation model...")
        
        if self.df is None or self.df.empty:
            self.load_movies_from_db()
        
        # Create content features for each movie
        self.df["content_features"] = self.df.apply(
            lambda row: self.create_content_features(row.to_dict()), 
            axis=1
        )
        
        # Create TF-IDF matrix
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2)
        )
        
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["content_features"])
        
        # Calculate cosine similarity
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
        print(f"✅ Recommendation model built with {len(self.df)} movies!")
        
    def get_recommendations(
        self, 
        movie_title: str, 
        top_n: int = 10
    ) -> List[Tuple[Dict, float]]:
        """
        Get top N movie recommendations based on content similarity.
        
        Returns: List of (movie_dict, similarity_score) tuples
        """
        if self.cosine_sim is None:
            self.build_similarity_matrix()
        
        # Find the movie index
        try:
            idx = self.df[self.df["title"].str.lower() == movie_title.lower()].index[0]
        except IndexError:
            # Try fuzzy matching
            matches = self.df[self.df["title"].str.lower().str.contains(movie_title.lower())]
            if matches.empty:
                return []
            idx = matches.index[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort by similarity (excluding the movie itself)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        similarity_scores = [i[1] for i in sim_scores]
        
        # Return movies with their similarity scores
        recommendations = []
        for idx, score in zip(movie_indices, similarity_scores):
            movie_data = self.df.iloc[idx].to_dict()
            recommendations.append((movie_data, float(score)))
        
        return recommendations
    
    def get_movie_by_title(self, title: str) -> Dict:
        """Get movie details by title"""
        if self.df is None:
            self.load_movies_from_db()
        
        try:
            movie = self.df[self.df["title"].str.lower() == title.lower()].iloc[0]
            return movie.to_dict()
        except IndexError:
            # Try fuzzy matching
            matches = self.df[self.df["title"].str.lower().str.contains(title.lower())]
            if not matches.empty:
                return matches.iloc[0].to_dict()
            return None
    
    def search_movies(self, query: str, limit: int = 20) -> List[Dict]:
        """Search movies by title"""
        if self.df is None:
            self.load_movies_from_db()
        
        matches = self.df[
            self.df["title"].str.lower().str.contains(query.lower(), na=False)
        ]
        
        # Sort by popularity
        matches = matches.sort_values("popularity", ascending=False)
        
        return matches.head(limit).to_dict("records")
    
    def get_trending_movies(self, limit: int = 20) -> List[Dict]:
        """Get trending/popular movies"""
        if self.df is None:
            self.load_movies_from_db()
        
        trending = self.df.sort_values("popularity", ascending=False)
        return trending.head(limit).to_dict("records")
    
    def get_top_rated_movies(self, limit: int = 20) -> List[Dict]:
        """Get top rated movies"""
        if self.df is None:
            self.load_movies_from_db()
        
        # Filter movies with at least 100 votes
        top_rated = self.df[self.df["vote_count"] >= 100]
        top_rated = top_rated.sort_values("vote_average", ascending=False)
        return top_rated.head(limit).to_dict("records")

# Global recommender instance
recommender = MovieRecommender()