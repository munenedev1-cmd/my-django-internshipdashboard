# Internship application portal

A Django application for internship applicant registration, applications, and a personal dashboard.

## Requirements

- Python 3.14 (the project dependencies are pinned in `requirements.txt`; Django 6.1.3 supports Python 3.14)
- A terminal in the project directory

## First-time setup

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
export DEBUG=true
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
$env:DEBUG = "true"
python -c "import secrets; print(secrets.token_urlsafe(50))"
# Copy the generated value into the next command:
$env:SECRET_KEY = "paste-generated-value-here"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. The Django admin is at <http://127.0.0.1:8000/admin/>.
Keep the terminal open while using the development server; press `Ctrl+C` to stop it.

For later starts, activate `.venv` and set `DEBUG=true` and the same `SECRET_KEY` in that terminal before running `python manage.py runserver`. `.env.example` lists the supported settings, but Django does not load `.env` files automatically.

## Checks and tests

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test applications
```

On PowerShell, set `$env:DEBUG = "true"` before running these commands because the local development key is only enabled in debug mode.

## Local data

The default database is `db.sqlite3`; uploaded application documents are stored under `media/` and can only be retrieved through the authenticated document view. Back up both locations if you need to preserve local applicant data. They are excluded from Git.

## Production

The development server is for local use only. Before any public deployment, configure a strong `SECRET_KEY`, `DEBUG=false`, the production `ALLOWED_HOSTS`, HTTPS and secure cookie settings, production-grade database and media storage, and a production web server. Run `python manage.py check --deploy` with those production settings and address its security warnings.
