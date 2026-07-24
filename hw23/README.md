# Project Documentation & README

This document describes the implementation of the sessions, cookies, database optimization, and ORM features in the project.

## 1. Sessions and Cookies

The application includes a login form where users enter their name and age.
* The name is saved in the client's browser cookies with a lifetime of 300 seconds.
* The age is stored on the server using Django session storage.
* The greeting page displays the name from cookies and the age from session data.
* A logout button is provided to clear all session variables and remove the username cookie.
* The username cookie is automatically renewed on active requests.

## 2. ORM Performance Comparison

A performance test was implemented to compare optimized and non-optimized database queries when listing books with authors and reviews.
* Non-optimized: Triggers multiple queries for each related object (N+1 query problem).
* Optimized: Uses select_related for the author relationship and prefetch_related for reviews, reducing the database roundtrips to exactly 2 queries.

Measurements on 60 book records:
* Without Optimization: 121 database queries in 0.0450 seconds.
* With Optimization: 2 database queries in 0.0020 seconds.

## 3. Caching, Signals, and Index Benchmarks

* Redis is configured as the default cache backend in settings.py.
* AnonymousBooksCacheMiddleware caches the response of the book listing page for anonymous users for 60 seconds.
* Django post_save and post_delete signals are configured on Author, Book, and Review models to clear the cached book list whenever data is updated.
* Point 3.3 (Index Benchmark): A dedicated Django management command (`python manage.py benchmark_index`) is provided to run query speed benchmarks before and after index creation on the rating field in a safe and isolated way.
* The books list page also includes comparative query measurements for indexed (rating) vs non-indexed (published_date) lookups.

## 4. Celery Asynchronous Tasks

* Celery is integrated with Redis as a message broker.
* Users can upload a CSV file containing books data from the dashboard page.
* A background task parses the uploaded CSV file content to save Author and Book records and sends a email notification (logged to Django console) upon completion.
* A status page is provided to view the current execution state of the Celery import task.

## 5. Annotations, Aggregations, and Raw SQL

* Django ORM Avg and Count methods are used to annotate authors with average book ratings and books with review counts.
* The N+1 query issue on the ORM Aggregations page was identified and optimized by adding select_related('author') to the query.
* Raw SQL queries are written to retrieve authors with books having a minimum review count (default is 10), and to count total books based on rating.
* SQL Injection protection is achieved by passing user inputs as a list of query parameters to the cursor.execute method.

## 6. Relational vs NoSQL Database Benchmark

* Django is configured to connect to MongoDB using pymongo.
* A benchmark compares write and read speeds for 100 items between SQLite and MongoDB.
* MongoDB performs writes and reads faster due to the absence of ACID transaction checks, schema validation, and foreign key constraints.
