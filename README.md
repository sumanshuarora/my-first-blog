# My First Blog

A simple Django blog application with full CRUD functionality for creating and managing blog posts.

## Features

- View all published blog posts
- View individual post details
- Create new blog posts (authenticated users)
- Edit existing posts
- Admin panel for post management
- User authentication integration

## Tech Stack

- **Framework**: Django 5.2.8
- **Database**: SQLite
- **Python**: 3.14.0
- **Timezone**: Asia/Kolkata

## Project Structure

```
my-first-blog/
├── blog/                  # Main blog application
│   ├── migrations/        # Database migrations
│   ├── static/           # CSS and static files
│   ├── templates/        # HTML templates
│   ├── admin.py          # Admin configuration
│   ├── forms.py          # Form definitions
│   ├── models.py         # Database models
│   ├── urls.py           # Blog URL routing
│   └── views.py          # View logic
├── mysite/               # Project configuration
│   ├── settings.py       # Main settings file
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI configuration
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Installation & Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd my-first-blog
```

### 2. Create and activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate  # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations
```bash
python manage.py migrate
```

### 5. Create a superuser
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

### 7. Access the application
- **Blog**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Usage

### Creating Blog Posts

1. Log in to the admin panel at `/admin/`
2. Navigate to Posts section
3. Click "Add Post" to create a new blog post
4. Fill in the title and content
5. Click "Save" to publish

Alternatively, use the web interface:
- Visit `/post/new/` to create a new post (requires authentication)
- Visit `/post/<id>/edit/` to edit an existing post

### Viewing Posts

- Homepage (`/`) displays all published posts
- Click on any post to view its details
- Posts are ordered by publication date

## Database Schema

### Post Model
- `author` - ForeignKey to Django User model
- `title` - CharField (max 200 characters)
- `text` - TextField
- `created_date` - DateTimeField (auto-set)
- `published_date` - DateTimeField (nullable)

## Configuration

Key settings in `mysite/settings.py`:
- **DEBUG**: Set to `True` for development
- **ALLOWED_HOSTS**: Configured for local and PythonAnywhere deployment
- **DATABASES**: SQLite (file-based)
- **TIME_ZONE**: Asia/Kolkata
- **STATIC_URL**: `/static/`

## Deployment

This project is configured for deployment on PythonAnywhere. The `ALLOWED_HOSTS` setting includes `.pythonanywhere.com`.

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper SECRET_KEY (use environment variables)
3. Set up static files collection: `python manage.py collectstatic`
4. Configure production database if needed

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## License

This project is for educational purposes.

## Author

Sumanshu Arora
