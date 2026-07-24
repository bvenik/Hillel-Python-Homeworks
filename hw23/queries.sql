-- 1. Select all authors who have books with >= X reviews (e.g. 10 reviews)
SELECT a.id, a.name, b.title, COUNT(r.id) AS review_count
FROM myapp_author a
JOIN myapp_book b ON b.author_id = a.id
JOIN myapp_review r ON r.book_id = b.id
GROUP BY b.id
HAVING COUNT(r.id) >= 10;

-- 2. Count the total number of books with rating >= Y (e.g. 4.0)
SELECT COUNT(*)
FROM myapp_book
WHERE rating >= 4.0;
