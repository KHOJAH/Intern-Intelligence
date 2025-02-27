# Importing required libraries
from fastapi import FastAPI, HTTPException  # FastAPI framework for building APIs
from pydantic import BaseModel  # Pydantic for data validation
from typing import List  # For type hinting

# Initialize the FastAPI app
app = FastAPI()

# Define the Movie data model using Pydantic
class Movie(BaseModel):
    id: int  # Unique identifier for the movie
    title: str  # Title of the movie
    director: str  # Director of the movie
    release_year: int  # Year the movie was released
    genre: str  # Genre of the movie (e.g., Action, Drama)
    imdb_rating: float  # IMDb rating of the movie (e.g., 8.5)

# In-memory storage for movies (simulating a database)
movies_db = []

# Endpoint to retrieve all movies (READ operation)
@app.get("/movies", response_model=List[Movie])  # GET request to fetch all movies
def get_all_movies():
    """
    Retrieve a list of all movies.
    Returns:
        List[Movie]: A list of movie objects.
    """
    return movies_db  # Return the list of movies from the in-memory database

# Endpoint to retrieve a single movie by ID (READ operation)
@app.get("/movies/{movie_id}", response_model=Movie)  # GET request to fetch a specific movie
def get_movie_by_id(movie_id: int):
    """
    Retrieve a movie by its ID.
    Args:
        movie_id (int): The ID of the movie to retrieve.
    Returns:
        Movie: The movie object if found.
    Raises:
        HTTPException: If the movie is not found.
    """
    for movie in movies_db:  # Loop through the movies in the database
        if movie.id == movie_id:  # Check if the movie ID matches
            return movie  # Return the matching movie
    raise HTTPException(status_code=404, detail="Movie not found")  # Raise error if no match

@app.post("/movies", response_model=Movie)  # POST request to add a new movie
def add_movie(movie: Movie):
    """
    Add a new movie to the database.
    Args:
        movie (Movie): The movie object to add.
    Returns:
        Movie: The added movie object.
    Raises:
        HTTPException: If a movie with the same ID already exists.
    """
    # Check if a movie with the same ID already exists
    for existing_movie in movies_db:
        if existing_movie.id == movie.id:
            raise HTTPException(status_code=400, detail="Movie with this ID already exists")
    
    # Add the new movie to the in-memory database
    movies_db.append(movie)
    
    # Return the added movie
    return movie

# Endpoint to update an existing movie (UPDATE operation)
@app.put("/movies/{movie_id}", response_model=Movie)  # PUT request to update a movie
def update_movie(movie_id: int, updated_movie: Movie):
    """
    Update an existing movie by its ID.
    Args:
        movie_id (int): The ID of the movie to update.
        updated_movie (Movie): The updated movie object.
    Returns:
        Movie: The updated movie object.
    Raises:
        HTTPException: If the movie is not found.
    """
    for i, movie in enumerate(movies_db):  # Loop through the movies with index
        if movie.id == movie_id:  # Check if the movie ID matches
            movies_db[i] = updated_movie  # Replace the old movie with the updated one
            return updated_movie  # Return the updated movie
    raise HTTPException(status_code=404, detail="Movie not found")  # Raise error if no match

# Endpoint to delete a movie (DELETE operation)
@app.delete("/movies/{movie_id}")  # DELETE request to remove a movie
def delete_movie(movie_id: int):
    """
    Delete a movie by its ID.
    Args:
        movie_id (int): The ID of the movie to delete.
    Returns:
        dict: A confirmation message.
    Raises:
        HTTPException: If the movie is not found.
    """
    for i, movie in enumerate(movies_db):  # Loop through the movies with index
        if movie.id == movie_id:  # Check if the movie ID matches
            del movies_db[i]  # Delete the movie from the in-memory database
            return {"message": "Movie deleted successfully"}  # Return success message
    raise HTTPException(status_code=404, detail="Movie not found")  # Raise error if no match
