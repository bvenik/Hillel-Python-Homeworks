# Homework 24 - Django Ninja REST API

This project contains the implementation of all 7 API options using Django Ninja and SQLite.

## How to Run the Server

1. Open your terminal in the project directory.
2. Run the server:
   ```bash
   ..\venv\Scripts\python.exe manage.py runserver
   ```
3. Open `http://127.0.0.1:8000/api/docs` in your browser to view the Swagger UI documentation.

## How to Test with Postman

There is a ready Postman collection file in the root folder: `hw24_postman_collection.json`.

1. Open Postman and click **Import** to load `hw24_postman_collection.json`.
2. Go to the `Authentication` folder and send a `Register` or `Login` request to get your token.
3. Copy the token string from the JSON response.
4. Click on the collection root folder `Unified REST API Collection` in the left menu.
5. Go to the **Variables** tab (or **Authorization** tab) and paste the token into the token value field.
6. Save the settings (Ctrl + S). Now you can run any request in the subfolders.

## Admin Panel

You can use the admin panel to add objects (products, movies, books, etc.) to the database.
- URL: `http://127.0.0.1:8000/admin/`
- Username: `admin`
- Password: `adminpass`
