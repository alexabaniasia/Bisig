# Bisig

Bisig is a Django web app where neighbors in a barangay offer and request skills and services, such as tutoring, plumbing, cooking and errands.

## Features

- Register, log in and log out
- Browse listings and filter them by category
- Post an offer or a request
- Listing detail page with a button to respond
- Profile page with photo upload
- Settings page with a dark mode toggle

Not built yet: email notifications, reviews, neighbor verification, editing or deleting your own listings.

## Tech stack

Django 6.1, PostgreSQL, Pillow, plain HTML and CSS.

## Setup

1. Clone and enter the project:
   ```
   git clone https://github.com/alexabaniasia/Bisig.git
   cd Bisig
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   (On macOS/Linux: `source venv/bin/activate`)
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create your environment file and fill it in:
   ```
   copy .env.example .env
   ```
5. Create the database tables (this also adds the default categories):
   ```
   python manage.py migrate
   ```
6. Create an admin account:
   ```
   python manage.py createsuperuser
   ```
7. Run the server:
   ```
   python manage.py runserver
   ```
   Then open http://127.0.0.1:8000/

## Environment variables

| Name | Description |
|------|-------------|
| `SECRET_KEY` | Django secret key. Generate a long random one. |
| `DEBUG` | `True` for local development, `False` in production. |
| `ALLOWED_HOSTS` | Comma-separated hosts, e.g. `127.0.0.1,localhost`. |
| `DATABASE_URL` | PostgreSQL connection URL. The app requires an SSL connection. |

## Project structure

```
apps/        Django apps (accounts, home, listings, login, register, user_profile, user_settings)
templates/   HTML templates
static/      CSS files
Bisig/       Project settings and URLs
```