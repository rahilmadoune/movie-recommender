from typing import List, Optional
from app.models import Movie, SessionLocal
from app.utils.data_loader import TMDbFetcher
from config import settings

class MovieService:
    """Business logic for movie operations"""
    
    @staticmethod
    def get_all_movies(skip: int = 0, limit: int = 100) -> List[Movie]:
        """Get all movies with pagination"""
        db = SessionLocal()
        try:
            movies = db.query(Movie).offset(skip).limit(limit).all()
            return movies
        finally:
            db.close()
    
    @staticmethod
    def get_movie_by_id(movie_id: int) -> Optional[Movie]:
        """Get a single movie by ID"""
        db = SessionLocal()
        try:
            return db.query(Movie).filter(Movie.id == movie_id).first()
        finally:
            db.close()
    
    @staticmethod
    def search_movies(query: str) -> List[Movie]:
        """Search movies by title"""
        db = SessionLocal()
        try:
            movies = db.query(Movie).filter(
                Movie.title.ilike(f"%{query}%")
            ).all()
            return movies
        finally:
            db.close()
    
    @staticmethod
    def get_trending_movies(limit: int = 20) -> List[Movie]:
        """Get trending movies sorted by popularity"""
        db = SessionLocal()
        try:
            movies = db.query(Movie).order_by(
                Movie.popularity.desc()
            ).limit(limit).all()
            return movies
        finally:
            db.close()
    
    @staticmethod
    def get_top_rated_movies(limit: int = 20) -> List[Movie]:
        """Get top rated movies"""
        db = SessionLocal()
        try:
            movies = db.query(Movie).filter(
                Movie.vote_count >= 100
            ).order_by(
                Movie.vote_average.desc()
            ).limit(limit).all()
            return movies
        finally:
            db.close()
    
    @staticmethod
    def count_movies() -> int:
        """Get total number of movies in database"""
        db = SessionLocal()
        try:
            return db.query(Movie).count()
        finally:
            db.close()
    
    @staticmethod
    def populate_database():
        """Fetch movies from TMDb and populate database"""
        db = SessionLocal()
        try:
            # Check if database is already populated
            count = db.query(Movie).count()
            if count > 0:
                print(f"✅ Database already has {count} movies. Skipping population.")
                return
            
            print("🎬 Starting database population from TMDb...")
            fetcher = TMDbFetcher()
            movies_data = fetcher.fetch_and_prepare_movies(settings.TOTAL_MOVIES_TO_FETCH)
            
            # Insert movies into database
            for movie_data in movies_data:
                movie = Movie(**movie_data)
                db.add(movie)
            
            db.commit()
            print(f"✅ Successfully added {len(movies_data)} movies to database!")
            
        except Exception as e:
            db.rollback()
            print(f"❌ Error populating database: {e}")
            raise
        finally:
            db.close()