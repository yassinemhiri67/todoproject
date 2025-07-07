# todoproject

A Python project repository.

## Overview

This repository, **todoproject**, is a Python-based project.  
It is currently public and maintained by [yassinemhiri67](https://github.com/yassinemhiri67).

## Features

- Django-based web application
- RESTful API with Django REST Framework
- Task, Employee, and Snippet management
- User authentication and permissions
- Pagination for all list endpoints
- Filtering (filtrage) for Task, Employee, and Snippet endpoints

## Getting Started

1. **Clone the repository**
   ```sh
   git clone https://github.com/yassinemhiri67/todoproject.git
   cd todoproject
   ```

2. **Set up a virtual environment (recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

HEAD
4. **Run the project**
   ```sh
   python manage.py migrate
   python manage.py runserver
   ```

4. **Set up environment variables**
   - Create a `.env` file in the project root with your secret key and debug setting:
     ```
     DJANGO_SECRET_KEY=your-very-secret-key-here
     DJANGO_DEBUG=True
     ```

5. **Run migrations**
   ```sh
   python manage.py migrate
   ```

6. **Run the development server**
   ```sh
   python manage.py runserver
   ```

## API Usage

- **Pagination:**
  - All list endpoints are paginated (default: 10 items per page).
  - Use `?page=2` to access the next page.

- **Filtering:**
  - Filter tasks, employees, and snippets using query parameters. Examples:
    - `/api/tasks/?status=DONE`
    - `/api/employees/?department=HR`
    - `/api/snippets/?language=python`
>>>>>>> 775b106 (add filtering, pagination, update requirements and readme)

## Project Structure

- `todoproject/` – Django project settings
- `todo/` – Main app (models, views, serializers, migrations)
- `attachments/` – Uploaded files
- `requirements.txt` – Python dependencies

## Contributing

Feel free to fork the repository and submit pull requests.

## License

*No license specified yet.*

## Links

- [Repository on GitHub](https://github.com/yassinemhiri67/todoproject)
