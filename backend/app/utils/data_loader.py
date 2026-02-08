import requests
import time
from typing import List, Dict, Optional
from config import settings

class TMDbFetcher:
    """Handles all interactions with TMDb API"""
    
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
        self.session = requests.Session()
        
    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        """Make a request to TMDb API with error handling"""
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from TMDb: {e}")
            return {}
    
    def fetch_popular_movies(self, page: int = 1) -> List[Dict]:
        """Fetch popular movies"""
        data = self._make_request("/movie/popular", {"page": page, "language": "en-US"})
        return data.get("results", [])
    
    def fetch_top_rated_movies(self, page: int = 1) -> List[Dict]:
        """Fetch top rated movies"""
        data = self._make_request("/movie/top_rated", {"page": page, "language": "en-US"})
        return data.get("results", [])
    
    def fetch_movie_details(self, movie_id: int) -> Dict:
        """Fetch detailed information about a specific movie"""
        return self._make_request(f"/movie/{movie_id}", {"language": "en-US"})
    
    def fetch_movie_credits(self, movie_id: int) -> Dict:
        """Fetch cast and crew for a movie"""
        return self._make_request(f"/movie/{movie_id}/credits")
    
    def fetch_movie_videos(self, movie_id: int) -> List[Dict]:
        """Fetch trailers and videos for a movie"""
        data = self._make_request(f"/movie/{movie_id}/videos")
        return data.get("results", [])
    
    def get_youtube_trailer(self, movie_id: int) -> Optional[str]:
        """Get YouTube trailer key for a movie"""
        videos = self.fetch_movie_videos(movie_id)
        for video in videos:
            if video.get("type") == "Trailer" and video.get("site") == "YouTube":
                return video.get("key")
        return None
    
    def fetch_complete_movie_data(self, movie_id: int) -> Dict:
        """Fetch all data for a movie (details, credits, trailer)"""
        details = self.fetch_movie_details(movie_id)
        credits = self.fetch_movie_credits(movie_id)
        trailer_key = self.get_youtube_trailer(movie_id)
        
        # Extract actors (top 5)
        actors = []
        if credits.get("cast"):
            actors = [actor["name"] for actor in credits["cast"][:5]]
        
        # Extract director
        director = None
        if credits.get("crew"):
            for person in credits["crew"]:
                if person.get("job") == "Director":
                    director = person.get("name")
                    break
        
        # Extract genres
        genres = [g["name"] for g in details.get("genres", [])]
        
        return {
            "tmdb_id": details.get("id"),
            "title": details.get("title"),
            "original_title": details.get("original_title"),
            "overview": details.get("overview"),
            "genres": genres,
            "release_date": details.get("release_date", ""),
            "vote_average": details.get("vote_average", 0),
            "vote_count": details.get("vote_count", 0),
            "popularity": details.get("popularity", 0),
            "poster_path": details.get("poster_path"),
            "backdrop_path": details.get("backdrop_path"),
            "trailer_key": trailer_key,
            "actors": actors,
            "director": director,
            "runtime": details.get("runtime"),
        }
    
    def fetch_and_prepare_movies(self, total: int = 1000) -> List[Dict]:
        """Fetch a large collection of movies with all details"""
        print(f"🎬 Fetching {total} movies from TMDb...")
        movies = []
        seen_ids = set()
        
        # Calculate pages needed
        pages_needed = (total // 20) + 1
        
        for page in range(1, pages_needed + 1):
            print(f"📄 Fetching page {page}/{pages_needed}...")
            
            # Get popular movies
            popular = self.fetch_popular_movies(page)
            for movie in popular:
                if movie["id"] not in seen_ids and len(movies) < total:
                    seen_ids.add(movie["id"])
                    movies.append(movie)
            
            # Get top rated movies
            if len(movies) < total:
                top_rated = self.fetch_top_rated_movies(page)
                for movie in top_rated:
                    if movie["id"] not in seen_ids and len(movies) < total:
                        seen_ids.add(movie["id"])
                        movies.append(movie)
            
            # Respect API rate limits
            time.sleep(0.3)
            
            if len(movies) >= total:
                break
        
        # Fetch complete details for each movie
        complete_movies = []
        for i, movie in enumerate(movies[:total], 1):
            print(f"🎞️  Fetching details for movie {i}/{len(movies[:total])}: {movie.get('title')}")
            complete_data = self.fetch_complete_movie_data(movie["id"])
            complete_movies.append(complete_data)
            time.sleep(0.3)  # Rate limiting
        
        print(f"✅ Successfully fetched {len(complete_movies)} movies!")
        return complete_movies