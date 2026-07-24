import time
from django.db import connection, reset_queries
from django.db.models import Avg, Count
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.cache import cache
from celery.result import AsyncResult

from .models import Author, Book
from .tasks import import_books_from_csv
from .nosql import run_nosql_benchmark


def login_view(request) -> HttpResponse:
    """
    Handles user login, saving username to cookies and age to session.
    :param request: HTTP request
    :return: HTTP response
    """
    if request.COOKIES.get('username') and request.session.get('age'):
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        age = request.POST.get('age', '').strip()

        if not username or not age:
            messages.error(request, "Name and age are required.")
            return render(request, 'myapp/login.html')

        response = redirect('home')
        response.set_cookie('username', username, max_age=300)
        request.session['age'] = age
        return response

    return render(request, 'myapp/login.html')


def home_view(request) -> HttpResponse:
    """
    Displays the personalized greeting page and auto-renews username cookie.
    :param request: HTTP request
    :return: HTTP response
    """
    username = request.COOKIES.get('username')
    age = request.session.get('age')

    if not username or not age:
        messages.warning(request, "Session or cookie expired. Please log in again.")
        return redirect('login')

    response = render(request, 'myapp/home.html', {
        'username': username,
        'age': age,
    })
    response.set_cookie('username', username, max_age=300)
    return response


def logout_view(request) -> HttpResponse:
    """
    Logs out the user by clearing cookies and sessions.
    :param request: HTTP request
    :return: HTTP response
    """
    request.session.flush()
    response = redirect('login')
    response.delete_cookie('username')
    messages.success(request, "You have logged out successfully.")
    return response


def orm_performance_view(request) -> HttpResponse:
    """
    Measures and compares query counts and times between non-optimized and optimized Django ORM calls.
    :param request: HTTP request
    :return: HTTP response
    """
    reset_queries()
    start_non_opt = time.perf_counter()
    books_all = list(Book.objects.all())
    non_opt_list = []
    for b in books_all:
        author_name = b.author.name
        reviews_count = b.reviews.count()
        non_opt_list.append({
            'title': b.title,
            'author': author_name,
            'reviews_count': reviews_count,
        })
    time_non_opt = time.perf_counter() - start_non_opt
    queries_non_opt = len(connection.queries)

    reset_queries()
    start_opt = time.perf_counter()
    books_opt = list(Book.objects.select_related('author').prefetch_related('reviews'))
    opt_list = []
    for b in books_opt:
        author_name = b.author.name
        reviews_count = len(b.reviews.all())
        opt_list.append({
            'title': b.title,
            'author': author_name,
            'reviews_count': reviews_count,
        })
    time_opt = time.perf_counter() - start_opt
    queries_opt = len(connection.queries)

    queries_saved = queries_non_opt - queries_opt
    speedup = round(time_non_opt / time_opt, 1) if time_opt > 0 else 0

    return render(request, 'myapp/orm_performance.html', {
        'time_non_opt': round(time_non_opt, 4),
        'queries_non_opt': queries_non_opt,
        'time_opt': round(time_opt, 4),
        'queries_opt': queries_opt,
        'queries_saved': queries_saved,
        'speedup': speedup,
        'books': opt_list[:10]
    })


def books_list_view(request) -> HttpResponse:
    """
    Displays the list of books, fetching from cache if available.
    Also shows index measurement.
    :param request: HTTP request
    :return: HTTP response
    """
    start_time = time.perf_counter()
    cached_data = cache.get('books_list')
    cache_hit = True

    if cached_data is None:
        cache_hit = False
        books = Book.objects.select_related('author').prefetch_related('reviews')
        cached_data = []
        for book in books:
            cached_data.append({
                'title': book.title,
                'author': book.author.name,
                'rating': book.rating,
                'reviews': [{'reviewer': r.reviewer_name, 'rating': r.rating} for r in book.reviews.all()]
            })
        cache.set('books_list', cached_data, timeout=300)

    elapsed_time = time.perf_counter() - start_time

    reset_queries()
    t0 = time.perf_counter()
    list(Book.objects.filter(rating=4.5))
    rating_query_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    list(Book.objects.filter(published_date='2020-01-01'))
    date_query_time = time.perf_counter() - t0

    return render(request, 'myapp/books_list.html', {
        'books': cached_data,
        'cache_hit': cache_hit,
        'elapsed_time': round(elapsed_time, 4),
        'rating_query_time': round(rating_query_time, 6),
        'date_query_time': round(date_query_time, 6),
    })


def celery_task_view(request) -> HttpResponse:
    """
    Renders Celery task dashboard, allowing users to submit CSV and trigger import.
    :param request: HTTP request
    :return: HTTP response
    """
    sample_csv = "title,author_name,published_date,rating\nPython Magic,Guido van Rossum,2026-01-01,5.0\nDjango Blueprint,Adrian Holovaty,2026-05-18,4.8\nCelery Guide,Ask Solem,2026-07-24,4.2\n"

    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        recipient_email = request.POST.get('email', '').strip()

        if not csv_file or not recipient_email:
            messages.error(request, "CSV file and email address are required.")
            return render(request, 'myapp/celery_task.html', {'sample_csv': sample_csv})

        try:
            csv_text = csv_file.read().decode('utf-8')
        except Exception:
            messages.error(request, "Invalid file format. Please upload a valid CSV file.")
            return render(request, 'myapp/celery_task.html', {'sample_csv': sample_csv})

        task = import_books_from_csv.delay(csv_text, recipient_email)
        return redirect('celery_status', task_id=task.id)

    return render(request, 'myapp/celery_task.html', {
        'sample_csv': sample_csv,
    })


def celery_status_view(request, task_id: str) -> HttpResponse:
    """
    Displays the status page for a Celery task.
    :param request: HTTP request
    :param task_id: ID of the background task
    :return: HTTP response
    """
    res = AsyncResult(task_id)
    status = res.status
    result = str(res.result) if res.ready() else None

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('json') == '1':
        return JsonResponse({
            'task_id': task_id,
            'status': status,
            'result': result
        })

    return render(request, 'myapp/celery_status.html', {
        'task_id': task_id,
        'status': status,
        'result': result
    })


def orm_aggregations_view(request) -> HttpResponse:
    """
    Handles aggregation and annotation queries and displays results in tables.
    :param request: HTTP request
    :return: HTTP response
    """
    authors_avg = Author.objects.annotate(
        avg_rating=Avg('books__rating')
    ).order_by('-avg_rating')

    books_with_reviews = Book.objects.select_related('author').annotate(
        reviews_count=Count('reviews'),
        avg_review_rating=Avg('reviews__rating')
    ).order_by('-reviews_count', '-avg_review_rating')

    return render(request, 'myapp/orm_aggregations.html', {
        'authors_avg': authors_avg,
        'books': books_with_reviews,
    })


def raw_sql_view(request) -> HttpResponse:
    """
    Runs raw SQL queries securely using parameters to prevent SQL injection.
    :param request: HTTP request
    :return: HTTP response
    """
    min_reviews = request.GET.get('min_reviews', '10')
    min_rating = request.GET.get('min_rating', '4.0')

    try:
        min_reviews_val = int(min_reviews)
    except ValueError:
        min_reviews_val = 10

    try:
        min_rating_val = float(min_rating)
    except ValueError:
        min_rating_val = 4.0

    query_authors = """
        SELECT a.id, a.name, b.title, COUNT(r.id) AS review_count
        FROM myapp_author a
        JOIN myapp_book b ON b.author_id = a.id
        JOIN myapp_review r ON r.book_id = b.id
        GROUP BY b.id
        HAVING COUNT(r.id) >= %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query_authors, [min_reviews_val])
        author_rows = cursor.fetchall()

    authors_list = [
        {'id': row[0], 'name': row[1], 'book_title': row[2], 'review_count': row[3]}
        for row in author_rows
    ]

    query_count = """
        SELECT COUNT(*)
        FROM myapp_book
        WHERE rating >= %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query_count, [min_rating_val])
        count_row = cursor.fetchone()

    total_books_filtered = count_row[0] if count_row else 0

    return render(request, 'myapp/raw_sql.html', {
        'authors': authors_list,
        'total_books_filtered': total_books_filtered,
        'min_reviews': min_reviews_val,
        'min_rating': min_rating_val,
    })


def nosql_compare_view(request) -> HttpResponse:
    """
    Executes a performance benchmark comparing SQLite and TinyDB, displaying the results.
    :param request: HTTP request
    :return: HTTP response
    """
    results = run_nosql_benchmark()
    return render(request, 'myapp/nosql_compare.html', {
        'results': results
    })