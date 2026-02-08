from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.routes import movie_routes
from app.models import init_db
from app.services.movie_service import MovieService
from app.services.recommender import recommender
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting CineMatch API...")
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    # Populate database if empty
    try:
        MovieService.populate_database()
    except Exception as e:
        print(f"⚠️  Warning: Could not populate database: {e}")
        print("💡 Make sure to set TMDB_API_KEY in .env file")
    
    # Build recommendation model
    try:
        recommender.build_similarity_matrix()
    except Exception as e:
        print(f"⚠️  Warning: Could not build recommendation model: {e}")
    
    print("✅ CineMatch API is ready!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down CineMatch API...")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered movie recommendation system with content-based filtering",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(movie_routes.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to CineMatch API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "endpoints": {
            "movies": "/api/movies",
            "search": "/api/movies/search?q=inception",
            "trending": "/api/movies/trending",
            "top_rated": "/api/movies/top-rated",
            "recommend": "/api/recommend (POST)"
        }
    }

# Health check
@app.get("/health")
async def health_check():
    movie_count = MovieService.count_movies()
    return {
        "status": "healthy",
        "total_movies": movie_count,
        "recommendation_engine": "active" if recommender.cosine_sim is not None else "initializing"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )