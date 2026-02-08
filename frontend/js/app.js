/**
 * CineMatch - Main Application Logic
 * Handles UI interactions and state management
 */

class CineMatchApp {
    constructor() {
        this.selectedMovie = null;
        this.searchTimeout = null;
        this.init();
    }

    /**
     * Initialize the application
     */
    async init() {
        this.cacheDOMElements();
        this.attachEventListeners();
        await this.loadInitialData();
    }

    /**
     * Cache frequently used DOM elements
     */
    cacheDOMElements() {
        // Search
        this.searchInput = document.getElementById('searchInput');
        this.searchButton = document.getElementById('searchButton');
        this.searchResults = document.getElementById('searchResults');
        
        // Sections
        this.selectedMovieSection = document.getElementById('selectedMovieSection');
        this.recommendationsSection = document.getElementById('recommendationsSection');
        this.trendingSection = document.getElementById('trendingSection');
        this.topRatedSection = document.getElementById('topRatedSection');
        
        // Containers
        this.selectedMovieContainer = document.getElementById('selectedMovie');
        this.recommendationsGrid = document.getElementById('recommendationsGrid');
        this.trendingGrid = document.getElementById('trendingGrid');
        this.topRatedGrid = document.getElementById('topRatedGrid');
        
        // Modal
        this.modal = document.getElementById('movieModal');
        this.modalBody = document.getElementById('modalBody');
        this.modalClose = document.getElementById('modalClose');
        
        // Other
        this.loadingSpinner = document.getElementById('loadingSpinner');
        this.totalMoviesEl = document.getElementById('totalMovies');
        this.navLinks = document.querySelectorAll('.nav-link');
    }

    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // Search
        this.searchInput.addEventListener('input', (e) => this.handleSearchInput(e));
        this.searchButton.addEventListener('click', () => this.handleSearch());
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSearch();
        });
        
        // Modal
        this.modalClose.addEventListener('click', () => this.closeModal());
        this.modal.querySelector('.modal-backdrop').addEventListener('click', () => this.closeModal());
        
        // Navigation
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleNavigation(e));
        });
        
        // Close search results when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-container')) {
                this.searchResults.classList.remove('active');
            }
        });
    }

    /**
     * Load initial data
     */
    async loadInitialData() {
        try {
            // Load stats
            const stats = await MovieAPI.getStats();
            this.totalMoviesEl.textContent = stats.total_movies.toLocaleString();
            
            // Load trending movies
            await this.loadTrendingMovies();
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showError('Failed to load data. Please refresh the page.');
        }
    }

    /**
     * Handle search input with debounce
     */
    handleSearchInput(e) {
        const query = e.target.value.trim();
        
        clearTimeout(this.searchTimeout);
        
        if (query.length < 2) {
            this.searchResults.classList.remove('active');
            return;
        }
        
        this.searchTimeout = setTimeout(() => {
            this.performSearch(query);
        }, 300);
    }

    /**
     * Perform search
     */
    async performSearch(query) {
        try {
            const results = await MovieAPI.searchMovies(query);
            this.displaySearchResults(results);
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    /**
     * Handle search button click
     */
    async handleSearch() {
        const query = this.searchInput.value.trim();
        if (query.length < 2) return;
        
        await this.performSearch(query);
    }

    /**
     * Display search results
     */
    displaySearchResults(movies) {
        if (movies.length === 0) {
            this.searchResults.innerHTML = '<div class="search-result-item"><p>No movies found</p></div>';
            this.searchResults.classList.add('active');
            return;
        }
        
        const html = movies.map(movie => `
            <div class="search-result-item" data-movie='${JSON.stringify(movie)}'>
                <img 
                    src="${movie.poster_url || 'https://via.placeholder.com/50x75?text=No+Image'}" 
                    alt="${movie.title}"
                    class="search-result-poster"
                >
                <div class="search-result-info">
                    <div class="search-result-title">${movie.title}</div>
                    <div class="search-result-meta">
                        ${movie.release_date ? movie.release_date.split('-')[0] : 'N/A'} • 
                        ${movie.genres.slice(0, 2).join(', ')}
                    </div>
                </div>
            </div>
        `).join('');
        
        this.searchResults.innerHTML = html;
        this.searchResults.classList.add('active');
        
        // Attach click handlers
        this.searchResults.querySelectorAll('.search-result-item').forEach(item => {
            item.addEventListener('click', () => {
                const movie = JSON.parse(item.dataset.movie);
                this.selectMovie(movie);
            });
        });
    }

    /**
     * Select a movie and get recommendations
     */
    async selectMovie(movie) {
        this.selectedMovie = movie;
        this.searchResults.classList.remove('active');
        this.searchInput.value = '';
        
        // Display selected movie
        this.displaySelectedMovie(movie);
        
        // Get recommendations
        await this.getRecommendations(movie.title);
        
        // Scroll to recommendations
        this.recommendationsSection.scrollIntoView({ behavior: 'smooth' });
    }

    /**
     * Display selected movie
     */
    displaySelectedMovie(movie) {
        const html = `
            <img 
                src="${movie.poster_url || 'https://via.placeholder.com/200x300?text=No+Image'}" 
                alt="${movie.title}"
                class="selected-movie-poster"
            >
            <div class="selected-movie-details">
                <h2 class="selected-movie-title">${movie.title}</h2>
                <div class="movie-meta" style="margin-bottom: 1rem;">
                    <span>⭐ ${movie.vote_average.toFixed(1)}</span>
                    <span>•</span>
                    <span>${movie.release_date ? movie.release_date.split('-')[0] : 'N/A'}</span>
                    ${movie.runtime ? `<span>•</span><span>${movie.runtime} min</span>` : ''}
                </div>
                <p class="selected-movie-overview">${movie.overview}</p>
                <div class="selected-movie-genres">
                    ${movie.genres.map(genre => `<span class="genre-tag">${genre}</span>`).join('')}
                </div>
            </div>
        `;
        
        this.selectedMovieContainer.innerHTML = html;
        this.selectedMovieSection.classList.remove('hidden');
    }

    /**
     * Get movie recommendations
     */
    async getRecommendations(movieTitle) {
        this.showLoading();
        
        try {
            const recommendations = await MovieAPI.getRecommendations(movieTitle, 10);
            this.displayRecommendations(recommendations);
        } catch (error) {
            console.error('Recommendations error:', error);
            this.showError('Failed to get recommendations. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    /**
     * Display recommendations
     */
    displayRecommendations(recommendations) {
        const html = recommendations.map(({ movie, similarity_score }) => 
            this.createMovieCard(movie, similarity_score)
        ).join('');
        
        this.recommendationsGrid.innerHTML = html;
        this.recommendationsSection.classList.remove('hidden');
        
        // Attach click handlers
        this.attachMovieCardHandlers();
    }

    /**
     * Load trending movies
     */
    async loadTrendingMovies() {
        try {
            const movies = await MovieAPI.getTrendingMovies();
            const html = movies.map(movie => this.createMovieCard(movie)).join('');
            this.trendingGrid.innerHTML = html;
            this.attachMovieCardHandlers();
        } catch (error) {
            console.error('Error loading trending movies:', error);
        }
    }

    /**
     * Load top rated movies
     */
    async loadTopRatedMovies() {
        try {
            const movies = await MovieAPI.getTopRatedMovies();
            const html = movies.map(movie => this.createMovieCard(movie)).join('');
            this.topRatedGrid.innerHTML = html;
            this.attachMovieCardHandlers();
        } catch (error) {
            console.error('Error loading top rated movies:', error);
        }
    }

    /**
     * Create movie card HTML
     */
    createMovieCard(movie, similarityScore = null) {
        const ratingClass = movie.vote_average >= 7 ? 'high' : movie.vote_average >= 5 ? 'medium' : 'low';
        
        return `
            <div class="movie-card" data-movie='${JSON.stringify(movie)}'>
                <div class="movie-poster-container">
                    ${similarityScore !== null ? `<div class="similarity-badge">${similarityScore}% Match</div>` : ''}
                    <div class="movie-rating ${ratingClass}">
                        ⭐ ${movie.vote_average.toFixed(1)}
                    </div>
                    <img 
                        src="${movie.poster_url || 'https://via.placeholder.com/200x300?text=No+Image'}" 
                        alt="${movie.title}"
                        class="movie-poster"
                    >
                </div>
                <div class="movie-info">
                    <h3 class="movie-title">${movie.title}</h3>
                    <div class="movie-meta">
                        <span class="movie-year">${movie.release_date ? movie.release_date.split('-')[0] : 'N/A'}</span>
                        ${movie.genres.length > 0 ? `<span>•</span><span class="movie-genre">${movie.genres[0]}</span>` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Attach click handlers to movie cards
     */
    attachMovieCardHandlers() {
        document.querySelectorAll('.movie-card').forEach(card => {
            card.addEventListener('click', () => {
                const movie = JSON.parse(card.dataset.movie);
                this.openMovieModal(movie);
            });
        });
    }

    /**
     * Open movie modal
     */
    openMovieModal(movie) {
        const html = `
            ${movie.backdrop_url ? `
                <div class="modal-header">
                    <img src="${movie.backdrop_url}" alt="${movie.title}" class="modal-backdrop-img">
                    <div class="modal-header-overlay"></div>
                </div>
            ` : ''}
            
            <h2 class="modal-title">${movie.title}</h2>
            
            <div class="modal-meta">
                <div class="modal-meta-item">
                    ⭐ ${movie.vote_average.toFixed(1)} / 10
                </div>
                <div class="modal-meta-item">
                    📅 ${movie.release_date ? movie.release_date.split('-')[0] : 'N/A'}
                </div>
                ${movie.runtime ? `
                    <div class="modal-meta-item">
                        ⏱️ ${movie.runtime} min
                    </div>
                ` : ''}
            </div>
            
            ${movie.overview ? `
                <div class="modal-section">
                    <h3 class="modal-section-title">Overview</h3>
                    <p class="modal-overview">${movie.overview}</p>
                </div>
            ` : ''}
            
            ${movie.genres && movie.genres.length > 0 ? `
                <div class="modal-section">
                    <h3 class="modal-section-title">Genres</h3>
                    <div class="selected-movie-genres">
                        ${movie.genres.map(genre => `<span class="genre-tag">${genre}</span>`).join('')}
                    </div>
                </div>
            ` : ''}
            
            ${movie.actors && movie.actors.length > 0 ? `
                <div class="modal-section">
                    <h3 class="modal-section-title">Cast</h3>
                    <div class="actors-list">
                        ${movie.actors.map(actor => `<span class="actor-tag">${actor}</span>`).join('')}
                    </div>
                </div>
            ` : ''}
            
            ${movie.director ? `
                <div class="modal-section">
                    <h3 class="modal-section-title">Director</h3>
                    <p style="color: var(--text-secondary);">${movie.director}</p>
                </div>
            ` : ''}
            
            ${movie.trailer_url ? `
                <div class="modal-section">
                    <h3 class="modal-section-title">Trailer</h3>
                    <div class="trailer-container">
                        <iframe 
                            class="trailer-iframe"
                            src="https://www.youtube.com/embed/${movie.trailer_key}"
                            allowfullscreen
                        ></iframe>
                    </div>
                </div>
            ` : ''}
        `;
        
        this.modalBody.innerHTML = html;
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    /**
     * Close modal
     */
    closeModal() {
        this.modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    /**
     * Handle navigation
     */
    async handleNavigation(e) {
        e.preventDefault();
        
        const section = e.target.dataset.section;
        
        // Update active nav link
        this.navLinks.forEach(link => link.classList.remove('active'));
        e.target.classList.add('active');
        
        // Hide all sections
        this.trendingSection.classList.add('hidden');
        this.topRatedSection.classList.add('hidden');
        
        // Show selected section
        switch(section) {
            case 'home':
                this.trendingSection.classList.remove('hidden');
                break;
            case 'trending':
                this.trendingSection.classList.remove('hidden');
                await this.loadTrendingMovies();
                break;
            case 'top-rated':
                this.topRatedSection.classList.remove('hidden');
                await this.loadTopRatedMovies();
                break;
        }
    }

    /**
     * Show loading spinner
     */
    showLoading() {
        this.loadingSpinner.classList.remove('hidden');
    }

    /**
     * Hide loading spinner
     */
    hideLoading() {
        this.loadingSpinner.classList.add('hidden');
    }

    /**
     * Show error message
     */
    showError(message) {
        alert(message); // In production, use a proper toast/notification system
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new CineMatchApp();
});