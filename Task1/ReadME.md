# Movie Database API

## Overview

This project is a RESTful API designed to manage a movie database. It allows users to perform basic operations such as adding, retrieving, updating, and deleting movie records. The API is built using Python's **FastAPI** framework, which provides automatic documentation through **Swagger UI** for easy interaction.

The API is ideal for managing a collection of movies with details like title, director, release year, genre, and IMDb rating. It also ensures data integrity by preventing duplicate entries based on the movie's unique ID.

---

## Features

- **Create**: Add new movies to the database.
- **Read**: Retrieve all movies or a specific movie by its ID.
- **Update**: Modify existing movie details.
- **Delete**: Remove a movie from the database.
- **Validation**: Ensures all movie data adheres to the required format (e.g., correct data types).
- **Duplicate Prevention**: Prevents adding movies with duplicate IDs.
- **Interactive Documentation**: Swagger UI is automatically generated for testing and exploring the API.

---

## How to Use the API

### Prerequisites

Before using the API, ensure you have the following installed:
1. **Python 3.7 or higher**
2. **FastAPI** and **Uvicorn** (install using `pip install fastapi uvicorn`)

### Running the API

1. Clone or download this repository to your local machine.
2. Open a terminal and navigate to the folder containing the `main.py` file.
3. Run the following command to start the server:
   ```bash
   uvicorn main:app --reload
