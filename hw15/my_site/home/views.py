from django.http import HttpRequest, HttpResponse


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Displays a welcome message on the home page

    :param request: HTTP request
    :return: response with a welcome string
    """
    return HttpResponse("Ласкаво просимо на головну сторінку")


def about_view(request: HttpRequest) -> HttpResponse:
    """
    Displays the about page message

    :param request: HTTP request
    :return: response with about string
    """
    return HttpResponse("Сторінка про нас")


def contact_view(request: HttpRequest) -> HttpResponse:
    """
    Display contact information message

    :param request: HTTP request
    :return: response with contact details string
    """
    return HttpResponse("Зв'яжіться з нами")


def post_view(request: HttpRequest, id: int) -> HttpResponse:
    """
    Display a specific post identified by ID

    :param request: HTTP request
    :param id: ID of post
    :return: response showing the post ID
    """
    return HttpResponse(f"Ви переглядаєте пост з ID: {id}")


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    """
    Display the profile of a specific user

    :param request: HTTP request
    :param username: username
    :return: response showing the username
    """
    return HttpResponse(f"Ви переглядаєте профіль користувача: {username}")


def event_view(request: HttpRequest, year: int, month: int, day: int) -> HttpResponse:
    """
    Display the date of a specific event

    :param request: HTTP request
    :param year: year of the event
    :param month: month of the event
    :param day: day of the event
    :return: response showing the date
    """
    return HttpResponse(f"Дата події: {year}-{month}-{day}")
