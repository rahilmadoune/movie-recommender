from sqlalchemy import Column, Integer, String, Float, Text, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True, index=True)
    title = Column(String, index=True)
    original_title = Column(String)
    overview = Column(Text)
    genres = Column(JSON)  # ["Action", "Sci-Fi"]
    release_date = Column(String)
    vote_average = Column(Float)
    vote_count = Column(Integer)
    popularity = Column(Float)
    poster_path = Column(String)
    backdrop_path = Column(String)
    trailer_key = Column(String, nullable=True)  # YouTube key
    actors = Column(JSON, nullable=True)  # ["Actor 1", "Actor 2"]
    director = Column(String, nullable=True)
    runtime = Column(Integer, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "tmdb_id": self.tmdb_id,
            "title": self.title,
            "original_title": self.original_title,
            "overview": self.overview,
            "genres": self.genres,
            "release_date": self.release_date,
            "vote_average": self.vote_average,
            "vote_count": self.vote_count,
            "popularity": self.popularity,
            "poster_path": self.poster_path,
            "backdrop_path": self.backdrop_path,
            "trailer_key": self.trailer_key,
            "actors": self.actors,
            "director": self.director,
            "runtime": self.runtime,
        }

# Database setup
engine = create_engine(
    settings.DATABASE_URL.replace("+aiosqlite", ""),
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)