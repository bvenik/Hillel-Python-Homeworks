from ninja import Router
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from datetime import date
from ..models import Movie, Genre, Review
from ..schemas import MovieIn, MovieOut, GenreIn, GenreOut, ReviewIn, ReviewOut
from ..auth import bearer_auth

router = Router()


@router.get("/genres", response=List[GenreOut], auth=bearer_auth)
def list_genres(request):
    """
    Retrieves all available movie genres.
    :param request: standard Django HTTP request object
    :return: list of Genre instances
    """
    return Genre.objects.all()


@router.post("/genres", response={201: GenreOut}, auth=bearer_auth)
def create_genre(request, data: GenreIn):
    """
    Creates a new movie genre.
    :param request: standard Django HTTP request object
    :param data: Pydantic schema containing genre name
    :return: tuple of HTTP status code 201 and the created Genre instance
    """
    genre = Genre.objects.create(**data.dict())
    return 201, genre


@router.get("/", response=List[MovieOut], auth=bearer_auth)
def list_movies(
    request,
    genre_name: Optional[str] = None,
    min_rating: Optional[float] = None,
    release_date: Optional[date] = None,
    search: Optional[str] = None
):
    """
    Retrieves the list of movies with optional filtering, rating thresholds, and text search.
    :param request: standard Django HTTP request object
    :param genre_name: optional genre name filter
    :param min_rating: optional minimum average rating filter (1.0 to 5.0)
    :param release_date: optional exact release date filter (YYYY-MM-DD)
    :param search: optional partial string match on movie title
    :return: list of Movie instances matching the search parameters
    """
    movies = Movie.objects.prefetch_related('genres').all()

    if search:
        movies = movies.filter(title__icontains=search)

    if genre_name:
        movies = movies.filter(genres__name__iexact=genre_name)

    if release_date:
        movies = movies.filter(release_date=release_date)

    if min_rating is not None:
        movies = movies.annotate(avg_rating=Avg('reviews__rating')).filter(
            avg_rating__gte=min_rating)

    return movies


@router.get("/{movie_id}", response=MovieOut, auth=bearer_auth)
def get_movie(request, movie_id: int):
    """
    Retrieves a single movie's details by its ID.
    :param request: standard Django HTTP request object
    :param movie_id: unique integer identifier of the movie
    :return: Movie instance or raises 404 Not Found
    """
    return get_object_or_404(Movie, id=movie_id)


@router.post("/", response={201: MovieOut}, auth=bearer_auth)
def create_movie(request, data: MovieIn):
    """
    Creates a new movie entry and associates it with genres.
    :param request: standard Django HTTP request object
    :param data: Pydantic schema containing movie title, description, release date, and genre IDs
    :return: tuple of HTTP status code 201 and the created Movie instance
    """
    genres = Genre.objects.filter(id__in=data.genre_ids)
    movie = Movie.objects.create(
        title=data.title,
        description=data.description,
        release_date=data.release_date
    )
    movie.genres.set(genres)
    return 201, movie


@router.put("/{movie_id}", response=MovieOut, auth=bearer_auth)
def update_movie(request, movie_id: int, data: MovieIn):
    """
    Updates an existing movie entry's details and genres.
    :param request: standard Django HTTP request object
    :param movie_id: unique integer identifier of the movie to update
    :param data: Pydantic schema containing updated title, description, release date, and genre IDs
    :return: updated Movie instance
    """
    movie = get_object_or_404(Movie, id=movie_id)
    genres = Genre.objects.filter(id__in=data.genre_ids)

    movie.title = data.title
    movie.description = data.description
    movie.release_date = data.release_date
    movie.save()
    movie.genres.set(genres)

    return movie


@router.delete("/{movie_id}", response={204: None}, auth=bearer_auth)
def delete_movie(request, movie_id: int):
    """
    Deletes a movie entry from the database.
    :param request: standard Django HTTP request object
    :param movie_id: unique integer identifier of the movie to delete
    :return: tuple of HTTP status code 204 and None
    """
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return 204, None


@router.post("/{movie_id}/reviews", response={201: ReviewOut}, auth=bearer_auth)
def add_review(request, movie_id: int, data: ReviewIn):
    """
    Submits a new rating and comment review for a movie by the authenticated user.
    :param request: standard Django HTTP request object containing authenticated user
    :param movie_id: unique integer identifier of the movie to review
    :param data: Pydantic schema containing rating (1-5) and comment text
    :return: tuple of HTTP status code 201 and custom serialized review dictionary
    """
    movie = get_object_or_404(Movie, id=movie_id)
    review = Review.objects.create(
        movie=movie,
        user=request.user,
        rating=data.rating,
        comment=data.comment
    )
    return 201, {
        "id": review.id,
        "movie_id": review.movie_id,
        "username": review.user.username,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at
    }


@router.get("/{movie_id}/reviews", response=List[ReviewOut], auth=bearer_auth)
def list_reviews(request, movie_id: int):
    """
    Retrieves all reviews submitted for a specific movie.
    :param request: standard Django HTTP request object
    :param movie_id: unique integer identifier of the movie
    :return: list of reviews with username field formatted
    """
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie).select_related('user')
    return [
        {
            "id": r.id,
            "movie_id": r.movie_id,
            "username": r.user.username,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at
        } for r in reviews
    ]
