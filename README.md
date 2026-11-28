# Bisig

Bisig is a Django web app where neighbors in a barangay offer and request skills and services, such as tutoring, plumbing, cooking and errands.

## Features

- Register with your name and barangay, log in and log out (with password checks)
- Browse listings with search, type filter, sorting, category chips and pagination
- Post an offer or a request, and edit, close, reopen or delete your own listings
- Listing detail page: respond to a listing, or (as the owner) accept or decline responses
- Reviews and star ratings after an accepted response, shown on public profiles
- Public profile pages with bio, verified badge, open listings and reviews
- "My activity" page with your listings and your responses
- "Needs help" page: open requests nobody has responded to yet (SQL subquery)
- Profile page with photo upload and personal details
- Settings: dark mode, show/hide your contact number, change password
- Admin site to manage users (including marking neighbors as verified), listings, responses and reviews

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
7. (Optional) Add sample users, listings, responses and reviews:
   ```
   python manage.py seed_demo_data
   ```
   Remove them again with `python manage.py seed_demo_data --clear`.
8. Run the server:
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

## Useful commands

```
python manage.py show_queries   # prints the SQL behind the JOIN and SUBQUERY features
python manage.py check
```

## Project structure

```
apps/        Django apps (accounts, home, listings, login, register, user_profile, user_settings)
templates/   HTML templates
static/      CSS files
Bisig/       Project settings and URLs
```
