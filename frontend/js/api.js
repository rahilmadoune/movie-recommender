/**
 * API Communication Layer
 * Handles all backend requests
 */

const API_BASE_URL = 'http://localhost:8000/api';

class MovieAPI {
    /**
     * Make a GET request to the API
     */
    static async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            throw error;
        }
    }

    /**
     * Make a POST request to the API
     */
    static async post(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            throw error;
        }
    }

    /**
     * Get all movies with pagination
     */
    static async getMovies(skip = 0, limit = 20) {
        return await this.get(`/movies?skip=${skip}&limit=${limit}`);
    }

    /**
     * Search movies by title
     */
    static async searchMovies(query) {
        return await this.get(`/movies/search?q=${encodeURIComponent(query)}`);
    }

    /**
     * Get trending movies
     */
    static async getTrendingMovies() {
        return await this.get('/movies/trending');
    }

    /**
     * Get top rated movies
     */
    static async getTopRatedMovies() {
        return await this.get('/movies/top-rated');
    }

    /**
     * Get movie by ID
     */
    static async getMovie(movieId) {
        return await this.get(`/movies/${movieId}`);
    }

    /**
     * Get recommendations for a movie
     */
    static async getRecommendations(movieTitle, topN = 10) {
        return await this.post('/recommend', {
            movie_title: movieTitle,
            top_n: topN
        });
    }

    /**
     * Get API stats
     */
    static async getStats() {
        try {
            const response = await fetch(`${API_BASE_URL}/stats`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching stats:', error);
            return { total_movies: 0, status: 'unknown' };
        }
    }
}

// Export for use in app.js
window.MovieAPI = MovieAPI;