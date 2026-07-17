from ninja import Router
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from ninja.errors import HttpError
from ..models import APIToken
from ..schemas import UserRegister, UserLogin, TokenOut

router = Router()


@router.post("/register", response={201: dict, 400: dict})
def register(request, data: UserRegister):
    """
    Registers a new user in the system and automatically generates an API token.
    :param request: standard Django HTTP request object
    :param data: Pydantic schema containing username, password, and optional email
    :return: tuple of HTTP status code and response dictionary with message and token
    """
    try:
        user = User.objects.create_user(
            username=data.username,
            password=data.password,
            email=data.email or ""
        )
        api_token = APIToken.objects.create(user=user)
        return 201, {"message": "User registered successfully", "token": api_token.token}
    except IntegrityError:
        return 400, {"message": "Username already exists"}


@router.post("/login", response={200: TokenOut, 401: dict})
def login(request, data: UserLogin):
    """
    Authenticates a user and retrieves or creates their API token.
    :param request: standard Django HTTP request object
    :param data: Pydantic schema containing username and password
    :return: tuple of HTTP status code and TokenOut schema or error dictionary
    """
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return 401, {"message": "Invalid username or password"}

    api_token, _ = APIToken.objects.get_or_create(user=user)
    return 200, TokenOut(token=api_token.token, username=user.username)
