![JMM](/media/uploads/jmm.jpg "jMM")

# Django File Upload/Download API

Classic Django + DRF (Django REST Framework) web application for registered users from various organizations that allows them to upload and download files.

Each user and file belongs to an organization. All downloads are tracked.

Implemented with Standart Django SQLite as DB (Just wanted to keep it simple) + Docker standart things to run.

## Features

* Session-based login/logout (works with DRF browsable API & admin)
* Upload and download files (downloads recorded automatically)
* List files with download counts
* List organizations with total download counts
* View downloads per user or per file

## Little bit about Structure
There is 4 domain objects: Users, Organizations, Files and Downloads.
Each user and uploaded file belongs to an organization
Users can log in and log out (via session authentication)

# Classic Python Venv installation if needed
python3 -m venv .venv
source .venv/bin/activate
pip instal

## start Django's development server
python manage.py runserver
python manage.py makemigrations
python manage.py migrate

## Test the API Run the development server:
python manage.py runserver
## http://127.0.0.1:8000/api/items/

python manage.py createsuperuser
# admin/salasana


## Running with Docker

```docker
docker-compose up --build
```

Admin interface: http://localhost:8000/admin/

API root: http://localhost:8000/api/

Django Rest login: http://localhost:8000/api/auth/login/?next=/api/

## HEre is already created test users and organizations for testing:
```python
python manage.py createsuperuser
# admin/salasana or you can log as admin2/admin2
# you can check and modify users at http://localhost:8000/admin/

python manage.py create_org_user --org "Soul Goodman" --username jimmy --password salasana1
python manage.py create_org_user --org "Davis & Miles" --username cliff --password salasana2
python manage.py create_org_user --org "Mesa Verde" --username kevin --password salasana3
python manage.py create_org_user --org "Schweikart & Cokely" --username richard --password salasana4
python manage.py create_org_user --org "Hamlin & McGill" --username howard --password salasana5
```

## How to test the application:
* Create user in http://localhost:8000/admin/ or you can use above list
* Login at http://localhost:8000/api/ as <b>"jimmy/salasana1"</b> or else from list above
* Go to /api/files/ and upload some file. File will be uploaded to your organization
* Go to /api/files/{id}/download/ and download a file. It will creates a Download record
* Go to /api/organizations/ and see total download counts by Organization
* Go to /api/downloads/by-user/{user_id}/ and see how much downloads by user
* Go to /api/downloads/by-file/{file_id}/ and see how much downloads for a file
* Login as "howard/salasana5" or someone else and try again