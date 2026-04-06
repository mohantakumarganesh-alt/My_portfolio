# Full Stack Blog Application

A complete, fully-featured blog application built with Django 6.0 and Bootstrap 5. 

## Features
- **User Authentication**: Secure Sign up, Log in, Log out.
- **Content Management**: Create, view, update, and delete blog posts.
- **Social Interactions**: Users can leave comments on posts, and Upvote/Downvote posts dynamically.
- **Third-party Login**: Configured for Google OAuth login via `django-allauth`.
- **Cinematic UI**: Modern dark-themed user interface utilizing Vanilla CSS and Bootstrap.

## Local Development Setup

To run this application locally on your machine for testing or development, follow these exact steps:

### 1. Prerequisites
Ensure you have **Python 3.12** or higher installed on your machine.

### 2. Create a Virtual Environment
It's highly recommended to run the app inside an isolated virtual environment. Navigate to the project root directory (`projects_code/blog_app/`) in your terminal and run:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required Python packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Create the Local Database
Set up the local SQLite database by running the standard Django migrations.
```bash
python manage.py makemigrations
python manage.py migrate
```

*(Optional)* You can create an admin "superuser" to log into the `/admin` backend area:
```bash
python manage.py createsuperuser
```

### 5. Run the Local Server
Start the Django development server.
```bash
python manage.py runserver
```
Visit the app in your browser at: `http://127.0.0.1:8000/`

---

## Production Deployment (Render)

This application is pre-configured for seamless deployment on [Render](https://render.com/). It uses a Render **Blueprint** (`render.yaml`) to automatically configure the environment and run the app.

1. **Environment Setup**: Render reads the `render.yaml` file to set up a Python 3.12.2 environment.
2. **Build Process**: Render automatically runs the `build.sh` script, which executes:
   - Dependency Installation (`pip install`)
   - Static File Collection for production (`collectstatic`)
   - Database Migrations (`migrate`)
   - Google Social Auth Database Seeding (`setup_social_auth`)
3. **App Startup**: Uses Gunicorn to serve the WSGI application (`blog_project.wsgi`).

### Important Note on Free Tier Data Persistence:
This app currently uses Render's **Free Tier Web Services**, and relies on a local `db.sqlite3` database file. Because free-tier Render web services have an **ephemeral (temporary) filesystem**, the SQL data (users, blog posts, comments) will reset to an empty state whenever the app goes to sleep or is redeployed. 

To permanently save your data, you should link the application to an external, free PostgreSQL database (such as Supabase or Neon). Once created, simply add the `DATABASE_URL` environment variable back into the Render dashboard!
