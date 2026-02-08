from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from app.services.movie_service import MovieService
from app.services.recommender import recommender
from config import settings

router = APIRouter(prefix="/api", tags=["movies"])

# Pydantic models for request/response
class MovieResponse(BaseModel):
    id: int
    tmdb_id: int
    title: str
    original_title: str
    overview: str
    genres: List[str]
    release_date: str
    vote_average: float
    vote_count: int
    popularity: float
    poster_path: Optional[str]
    backdrop_path: Optional[str]
    trailer_key: Optional[str]
    actors: Optional[List[str]]
    director: Optional[str]
    runtime: Optional[int]
    
    class Config:
        from_attributes = True

class RecommendationRequest(BaseModel):
    movie_title: str
    top_n: int = 10

class RecommendationResponse(BaseModel):
    movie: MovieResponse
    similarity_score: float

class ImageUrlHelper:
    """Helper to generate full image URLs"""
    @staticmethod
    def get_poster_url(path: Optional[str], size: str = "w500") -> Optional[str]:
        if not path:
            return None
        return f"{settings.TMDB_IMAGE_BASE_URL}/{size}{path}"
    
    @staticmethod
    def get_backdrop_url(path: Optional[str], size: str = "w1280") -> Optional[str]:
        if not path:
            return None
        return f"{settings.TMDB_IMAGE_BASE_URL}/{size}{path}"
    
    @staticmethod
    def get_trailer_url(key: Optional[str]) -> Optional[str]:
        if not key:
            return None
        return f"https://www.youtube.com/watch?v={key}"

def enrich_movie_data(movie) -> dict:
    """Add full image URLs to movie data"""
    movie_dict = movie if isinstance(movie, dict) else movie.to_dict()
    
    # Add full URLs
    movie_dict["poster_url"] = ImageUrlHelper.get_poster_url(movie_dict.get("poster_path"))
    movie_dict["backdrop_url"] = ImageUrlHelper.get_backdrop_url(movie_dict.get("backdrop_path"))
    movie_dict["trailer_url"] = ImageUrlHelper.get_trailer_url(movie_dict.get("trailer_key"))
    
    return movie_dict

@router.get("/movies", response_model=List[dict])
async def get_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """Get all movies with pagination"""
    movies = MovieService.get_all_movies(skip=skip, limit=limit)
    return [enrich_movie_data(movie) for movie in movies]

@router.get("/movies/search")
async def search_movies(q: str = Query(..., min_length=1)):
    """Search movies by title"""
    results = recommender.search_movies(q, limit=20)
    return [enrich_movie_data(movie) for movie in results]

@router.get("/movies/trending")
async def get_trending():
    """Get trending/popular movies"""
    movies = recommender.get_trending_movies(limit=20)
    return [enrich_movie_data(movie) for movie in movies]

@router.get("/movies/top-rated")
async def get_top_rated():
    """Get top rated movies"""
    movies = recommender.get_top_rated_movies(limit=20)
    return [enrich_movie_data(movie) for movie in movies]

@router.get("/movies/{movie_id}")
async def get_movie(movie_id: int):
    """Get a single movie by ID"""
    movie = MovieService.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return enrich_movie_data(movie)

@router.post("/recommend")
async def get_recommendations(request: RecommendationRequest):
    """
    Get movie recommendations based on a movie title.
    Returns similar movies with similarity scores.
    """
    try:
        recommendations = recommender.get_recommendations(
            request.movie_title, 
            top_n=request.top_n
        )
        
        if not recommendations:
            raise HTTPException(
                status_code=404, 
                detail=f"Movie '{request.movie_title}' not found"
            )
        
        # Format response
        response = []
        for movie_data, score in recommendations:
            enriched_movie = enrich_movie_data(movie_data)
            response.append({
                "movie": enriched_movie,
                "similarity_score": round(score * 100, 2)  # Convert to percentage
            })
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_stats():
    """Get database statistics"""
    total_movies = MovieService.count_movies()
    return {
        "total_movies": total_movies,
        "status": "active" if total_movies > 0 else "empty"
    }