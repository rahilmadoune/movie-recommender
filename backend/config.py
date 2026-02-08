import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # TMDb API Configuration
    TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")  # You'll need to get this from https://www.themoviedb.org/settings/api
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p"
    
    # Database
    DATABASE_URL = "sqlite+aiosqlite:///./data/movies.db"
    
    # Application
    APP_NAME = "CineMatch - AI Movie Recommender"
    APP_VERSION = "1.0.0"
    
    # Movie fetching
    TOTAL_MOVIES_TO_FETCH = 1000
    MOVIES_PER_PAGE = 20
    
    # CORS
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

settings = Settings()