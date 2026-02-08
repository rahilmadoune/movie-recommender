# movie-recommender
AI-powered movie recommendation system using content-based filtering.  Built with Python FastAPI backend and vanilla JavaScript frontend.  Features 1000+ movies, real-time search, and personalized recommendations.

---

# CineMatch - AI-Powered Movie Recommendation System

**Discover your next favorite movie with AI-powered content-based filtering**


---

> **Current Version:** v1.0 - Beta  
> **Active Development:** We're continuously adding features and fixing bugs.
> **Coming Soon:** Light/Dark mode toggle, improved navigation, user profiles, and more


---

## Features

### AI-Powered Recommendations
- **Content-based filtering** using TF-IDF vectorization and cosine similarity
- Analyzes movie genres, plot, actors, directors, and more
- Returns similarity scores showing why movies match

### Core Functionality
-  Search through 1000+ movies with real-time autocomplete
-  Get personalized recommendations based on content similarity
-  Browse trending and top-rated movies
-  View detailed movie information with embedded trailers
-  Beautiful, responsive Netflix-inspired UI
-  Fast, efficient SQLite database

###  Design
- Modern dark cinematic theme
- Smooth animations and transitions
- Glassmorphism effects
- Fully responsive (mobile + desktop)
- Professional typography and spacing

---

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **scikit-learn** - Machine learning library (TF-IDF, cosine similarity)
- **pandas** - Data manipulation and analysis
- **SQLite** - Lightweight embedded database

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with CSS variables
- **Vanilla JavaScript** - ES6+ features, Fetch API
- **No frameworks** - Pure, lightweight code

### External APIs
- **TMDb API** - The Movie Database for movie data, posters, trailers

---

## Prerequisites

Before you begin, ensure you have:
- **Python 3.13+** installed ([Download](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (optional, for cloning)
- **TMDb API Key** (free - see below)

> **Beta Notice:** This is an active development project. Some features may have bugs or be incomplete. We're working on improvements.

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/cinematch.git
cd cinematch
```

### Step 2: Get TMDb API Key (Free)

1. Go to [TMDb Sign Up](https://www.themoviedb.org/signup)
2. Create a free account and verify your email
3. Visit [API Settings](https://www.themoviedb.org/settings/api)
4. Click **"Request an API Key"** → Choose **"Developer"**
5. Fill in the form:
   - **Type**: Website
   - **Application Name**: CineMatch (or any name)
   - **Application URL**: http://localhost:3000
   - **Application Summary**: Personal movie recommendation project
6. **Copy your API Key** (looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

### Step 3: Backend Setup

#### Windows:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Mac/Linux:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

**IMPORTANT FOR GITHUB:**

**Follow these steps:**

1. **Copy the example file:**
   ```bash
   # Windows
   copy .env.example .env
   
   # Mac/Linux
   cp .env.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   notepad .env        # Windows
   nano .env           # Mac/Linux
   ```

3. **Add your TMDb API key:**
   ```
   TMDB_API_KEY=your_actual_api_key_here
   ```
   
   Replace `your_actual_api_key_here` with your real key from Step 2

4. **Save and close**

### Step 5: Create Data Directory

```bash
mkdir data
```

### Step 6: Start Backend Server

#### From backend directory:

**Windows:**
```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Mac/Linux:**
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**First run**: Takes 10-15 minutes to fetch 1000 movies from TMDb  
**Subsequent runs**: Instant (< 5 seconds)

You'll see:
```
Fetching 1000 movies from TMDb...
Successfully fetched 1000 movies!
Building AI recommendation model...
CineMatch API is ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!**

### Step 7: Start Frontend Server

**Open a NEW terminal:**

```bash
cd frontend

# Start HTTP server
python -m http.server 3000        # Windows/Mac/Linux
```

**Keep this terminal open too!**

### Step 8: Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

---

## Usage

### Search for Movies
1. Type a movie name in the search bar (e.g., "Inception")
2. Click on a movie from the dropdown results
3. View the selected movie details

### Get Recommendations
1. After selecting a movie, scroll down
2. See 10 AI-recommended similar movies
3. Each recommendation shows a match percentage

### Browse Collections
- Click **"Trending"** in the navigation to see popular movies
- Click **"Top Rated"** to view critically acclaimed films
- Click **"Home"** to return to the main page

### View Movie Details
1. Click on any movie card
2. A modal opens with:
   - Movie poster and backdrop
   - Plot overview
   - Genres, cast, director
   - Release date, rating, runtime
   - Embedded YouTube trailer

---

## API Documentation

The backend provides a RESTful API with automatic interactive documentation.

### Access API Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Key Endpoints

#### Get All Movies
```http
GET /api/movies?skip=0&limit=20
```

#### Search Movies
```http
GET /api/movies/search?q=inception
```

#### Get Trending Movies
```http
GET /api/movies/trending
```

#### Get Top Rated Movies
```http
GET /api/movies/top-rated
```

#### Get Recommendations
```http
POST /api/recommend
Content-Type: application/json

{
  "movie_title": "Inception",
  "top_n": 10
}
```

**Response:**
```json
[
  {
    "movie": {
      "id": 123,
      "title": "Interstellar",
      "overview": "...",
      "genres": ["Sci-Fi", "Drama"],
      "vote_average": 8.6,
      "poster_url": "https://...",
      "trailer_url": "https://youtube.com/..."
    },
    "similarity_score": 87.5
  }
]
```

---

## How the AI Works

### Content-Based Filtering Algorithm

1. **Feature Extraction**
   - Combines multiple movie attributes:
     - Genres (weight: 3x)
     - Plot/Overview (weight: 1x)
     - Actors (weight: 2x)
     - Director (weight: 1x)

2. **TF-IDF Vectorization**
   - Converts text features into numerical vectors
   - Uses n-grams (1-2 words) for better context understanding
   - Removes stop words and normalizes text

3. **Cosine Similarity**
   - Calculates similarity between all movie pairs
   - Returns top N most similar movies with scores (0-100%)

### Example

**Input Movie:** "Inception"
```
Features: "Action Sci-Fi Thriller Christopher Nolan Leonardo DiCaprio..."
```

**Top Recommendations:**
1. **Interstellar** (88% match) - Same director, similar sci-fi themes
2. **The Dark Knight** (82% match) - Same director, some cast overlap
3. **Shutter Island** (79% match) - Same lead actor, psychological thriller

---

## Project Structure

```
cinematch/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry
│   │   ├── models.py            # SQLAlchemy database models
│   │   ├── routes/
│   │   │   └── movie_routes.py  # API endpoints
│   │   ├── services/
│   │   │   ├── movie_service.py # Business logic
│   │   │   └── recommender.py   # AI recommendation engine
│   │   └── utils/
│   │       └── data_loader.py   # TMDb API fetcher
│   ├── data/
│   │   └── movies.db            # SQLite database (auto-generated)
│   ├── requirements.txt         # Python dependencies
│   ├── config.py                # Configuration settings
│   ├── .env.example             # Environment variables template
│   └── .env                     # Your API key (DO NOT COMMIT!)
│
├── frontend/
│   ├── index.html               # Main HTML page
│   ├── css/
│   │   └── style.css            # Styling
│   └── js/
│       ├── api.js               # API communication layer
│       └── app.js               # Application logic
│
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
└── LICENSE                      # MIT License
```

---

## Development

### Running in Development Mode

**Backend** (with auto-reload):
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend
python -m http.server 3000
```

### Database Management

**Reset database** (re-fetch all movies):
```bash
# Delete database
rm backend/data/movies.db  # Mac/Linux
del backend\data\movies.db  # Windows

# Restart backend - it will re-fetch movies
python -m uvicorn app.main:app --reload
```

---

## Testing

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Test API Endpoints
```bash
# Search
curl "http://localhost:8000/api/movies/search?q=inception"

# Recommendations
curl -X POST "http://localhost:8000/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{"movie_title": "Inception", "top_n": 5}'
```

### Test Frontend
Open http://localhost:3000 and verify:
- Search works
- Recommendations appear
- Trending/Top Rated load
- Modal opens on click
- Trailer plays

---

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.13+

# Reinstall dependencies
pip install -r requirements.txt

# Check .env file exists
ls .env  # Mac/Linux
dir .env  # Windows
```

### "TMDb API Error"
- Verify API key in `.env` is correct
- No spaces or quotes around the key
- Check internet connection
- Verify TMDb account is verified

### "Module not found" errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Should see (venv) in terminal
```

### Frontend can't connect to backend
- Check backend is running on port 8000
- Visit http://localhost:8000/health
- Check browser console (F12) for CORS errors

### Port already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <number> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

---

## Deployment

### Backend (Heroku, Render, Railway)

1. Add `Procfile`:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

2. Set environment variable:
   ```
   TMDB_API_KEY=your_key_here
   ```

3. Deploy!

### Frontend (Netlify, Vercel, GitHub Pages)

1. Update API URL in `frontend/js/api.js`:
   ```javascript
   const API_BASE_URL = 'https://your-backend-url.com/api';
   ```

2. Deploy `frontend/` folder

---

## Future Enhancements

We're continuously improving CineMatch! Here's what's coming:

### Coming Soon

#### **Phase 1: UI/UX Improvements** (In Progress)
- [ ] **Light/Dark Mode Toggle** - Switch between cinema dark mode and bright light theme
- [ ] **Fix Navigation Issues** - Ensure all buttons (Trending, Top Rated) work smoothly
- [ ] **Improve Search Interactions** - Better click handlers and responsiveness
- [ ] **Loading Skeletons** - Smooth content placeholders instead of spinners
- [ ] **Toast Notifications** - Beautiful feedback messages instead of alerts

#### **Phase 2: User Features**
- [ ] **User Authentication** - Sign up, login, and personalized profiles
- [ ] **Favorites & Watchlist** - Save movies you want to watch
- [ ] **User Ratings** - Rate movies and get personalized recommendations
- [ ] **Recommendation History** - See your past searches and suggestions
- [ ] **Share Recommendations** - Send movie suggestions to friends

#### **Phase 3: Advanced AI**
- [ ] **Collaborative Filtering** - Recommendations based on users with similar tastes
- [ ] **Hybrid Recommendation Engine** - Combine content-based + collaborative filtering
- [ ] **Mood-Based Recommendations** - "I'm feeling happy" → Get comedy suggestions
- [ ] **Multi-Movie Recommendations** - "Movies like X, Y, and Z combined"
- [ ] **Explanation System** - Show WHY movies are recommended (shared actors, genres, themes)

#### **Phase 4: Enhanced Features**
- [ ] **Advanced Filters** - Filter by year, genre, rating, runtime
- [ ] **Similar Movies Network** - Visual graph of movie relationships
- [ ] **Movie Comparison** - Side-by-side comparison of multiple movies
- [ ] **Streaming Availability** - Where to watch (Netflix, Prime, etc.)
- [ ] **Movie Collections** - Create and share custom movie lists

#### **Phase 5: Platform Expansion**
- [ ] **Mobile App** - React Native iOS/Android app
- [ ] **Progressive Web App (PWA)** - Install as app on mobile/desktop
- [ ] **Social Features** - Follow users, share lists, discuss movies
- [ ] **Multi-language Support** - Support for Spanish, French, Arabic, etc.
- [ ] **Accessibility Improvements** - Screen reader support, keyboard navigation

### Known Issues & Fixes

We're aware of some bugs and actively working on fixes:

- [ ] **Search Click Handler** - Sometimes search results don't respond to clicks (fixing in next update)
- [ ] **Navigation Buttons** - Trending/Top Rated may not load movies on first click (being improved)
- [ ] **Image Loading** - Add lazy loading for better performance
- [ ] **Mobile Responsiveness** - Fine-tune layout for smaller screens
- [ ] **Browser Compatibility** - Test and fix issues in Safari, Firefox
- [ ] **API Rate Limiting** - Handle TMDb API limits more gracefully
- [ ] **Database Performance** - Optimize queries for larger datasets (10K+ movies)

### Experimental Ideas

Features we're considering:
- AI-generated movie summaries in simple language
- Voice search: "Find me a movie like Inception"
- Movie quiz: "What should I watch tonight?" questionnaire
- Box office predictions using ML
- Sentiment analysis of movie reviews
- Auto-generate movie posters with AI
- Virtual watch parties with friends

---


## License

This project is licensed under the MIT License 

---

## Changelog

### Version 1.0.0 - Beta (Current)
**Released:** February 2026

**Features:**
- AI-powered content-based movie recommendations
- Search through 1000+ movies with autocomplete
- Browse trending and top-rated movies
- Detailed movie information with trailers
- Beautiful Netflix-inspired dark theme UI
- RESTful API with automatic documentation
- SQLite database with efficient queries
- Responsive design for mobile and desktop

**Known Issues:**
- Search results may not respond to clicks occasionally
- Navigation buttons (Trending/Top Rated) need reliability improvements
- Theme toggle (light/dark mode) coming in v1.1

**Coming in v1.1:**
- Light/Dark mode toggle
- Fixed navigation and search interactions
- Loading skeletons for better UX
- Toast notifications
- Performance optimizations

---

## Acknowledgments

- **TMDb** for providing the comprehensive movie database API
- **FastAPI** for the excellent Python web framework
- **scikit-learn** for machine learning tools
- Inspired by Netflix, IMDb, and other streaming platforms
- Special thanks to the open-source community

---



**Built with ❤️ using Python, FastAPI, and Vanilla JavaScript**

