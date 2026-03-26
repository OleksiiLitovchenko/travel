# Travel Projects API

A Django REST API for managing travel projects and places to visit.

This application allows users to create travel projects, add places from a third-party API, attach notes, and track whether places have been visited.

## Features

Travel Projects:
- Create a travel project
- Update project information (name, description, start date)
- List all projects
- Retrieve a single project
- Delete a project (not allowed if any place is marked as visited)

Project Places:
- Create a project with places in a single request
- Add a place to an existing project
- Update notes for a place
- Mark a place as visited
- List all places within a project
- Retrieve a single place

Business rules:
- Maximum 10 places per project
- Duplicate places are not allowed within a project
- A project is automatically marked as completed when all its places are visited
- Places are validated using the Art Institute of Chicago API

## Tech Stack

- Python 3.12
- Django
- Django REST Framework
- SQLite
- Requests
- Docker

## Third-Party API

This project uses the Art Institute of Chicago API:

GET https://api.artic.edu/api/v1/artworks/{id}

It is used to validate that a place exists and to fetch its title.

## Installation and Local Run

1. Clone the repository:
git clone https://github.com/OleksiiLitovchenko/travel.git
cd travel

2. Create virtual environment:
python -m venv .venv

3. Activate virtual environment:

Windows:
.venv\Scripts\Activate.ps1

Linux / macOS:
source .venv/bin/activate

4. Install dependencies:
pip install -r requirements.txt

5. Apply migrations:
python manage.py makemigrations
python manage.py migrate

6. Create superuser (optional):
python manage.py createsuperuser

7. Run server:
python manage.py runserver

Application will be available at:
http://127.0.0.1:8000/api/
http://127.0.0.1:8000/admin/

## Run with Docker

Build the image:
docker build -t travel-api .

Run the container:
docker run -p 8000:8000 travel-api

Application will be available at:
http://127.0.0.1:8000/api/
http://127.0.0.1:8000/admin/

To create a superuser inside Docker:
docker exec -it <container_id> python manage.py createsuperuser

## API Endpoints

Travel Projects:
POST /api/projects/
GET /api/projects/
GET /api/projects/{id}/
PATCH /api/projects/{id}/
DELETE /api/projects/{id}/

Project Places:
GET /api/projects/{id}/places/
POST /api/projects/{id}/places/
GET /api/project-places/{id}/
PATCH /api/project-places/{id}/

## Example Requests

Create project with places:
POST /api/projects/

{
  "name": "Chicago Trip",
  "description": "Art museums visit",
  "start_date": "2026-04-01",
  "places": [
    {
      "external_id": 129884,
      "notes": "Must see first"
    },
    {
      "external_id": 111628,
      "notes": "Check opening hours"
    }
  ]
}

Add place to project:
POST /api/projects/1/places/

{
  "external_id": 14644,
  "notes": "Interesting place"
}

Update place:
PATCH /api/project-places/1/

{
  "visited": true,
  "notes": "Visited in the morning"
}

## Postman Collection

A Postman collection is included in the repository:

postman/Travel_API.postman_collection.json

To use it:
1. Open Postman
2. Click Import
3. Select the collection file
4. Use base URL: http://127.0.0.1:8000

## Notes

- Places are validated against the Art Institute of Chicago API before being stored
- Only external_id and title are stored locally
- Each project maintains its own visited state for places
- SQLite is used as the database for simplicity

## Author

Oleksii Litovchenko
