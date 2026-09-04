# Healthcare Backend API

A Django REST Framework backend for managing users, patients, doctors, and patient-doctor assignments with JWT authentication and PostgreSQL.

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Simple JWT
- python-dotenv

## Features

- JWT authentication
- Custom user model with email authentication
- Patient CRUD operations
- Patient ownership and access control
- Doctor CRUD operations
- Patient-doctor assignments
- Duplicate mapping prevention
- Input validation
- PostgreSQL database
- Automated tests

## Project Structure

```text
healthcare-backend/
├── config/
├── users/
├── patients/
├── doctors/
├── mappings/
├── tests/
├── manage.py
├── requirements.txt
├── .env.example
└── postman_collection.json
```

## Setup / Installation

```text
Create virtual environment
        ↓
Install dependencies
        ↓
Configure .env
        ↓
Create PostgreSQL database
        ↓
Run migrations
        ↓
Create superuser
        ↓
Run server
```

### Commands

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## Environment Variables

Show `.env.example`:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

> Never put your real `.env` in GitHub.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register user |
| POST | `/api/auth/login/` | Login |
| POST | `/api/auth/token/refresh/` | Refresh token |

### Patients

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Create patient |
| GET | `/api/patients/` | List own patients |
| GET | `/api/patients/<id>/` | Get patient |
| PUT | `/api/patients/<id>/` | Update patient |
| DELETE | `/api/patients/<id>/` | Delete patient |

### Doctors

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Create doctor |
| GET | `/api/doctors/` | List doctors |
| GET | `/api/doctors/<id>/` | Get doctor |
| PUT | `/api/doctors/<id>/` | Update doctor |
| DELETE | `/api/doctors/<id>/` | Delete doctor |

### Mappings

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Create mapping |
| GET | `/api/mappings/` | List mappings |
| GET | `/api/mappings/<patient_id>/` | Get doctors for patient |
| DELETE | `/api/mappings/<id>/` | Delete mapping |

## Authentication

The API uses JWT authentication.

After login, include the access token in requests:

```http
Authorization: Bearer <access_token>
```

## Security

- JWT authentication
- Password hashing using Django's authentication system
- Object-level authorization
- Patient ownership isolation
- Environment-based secrets
- Input validation
- Database-level uniqueness constraints

## Testing

Run:

```bash
python manage.py test
```

Testing includes:
- Authentication
- CRUD operations
- Validation
- Permissions
- Patient ownership isolation
- Patient-doctor mappings

## Postman

Import `postman_collection.json` into Postman to test all API endpoints.

## Django Admin

Create a superuser:

```bash
python manage.py createsuperuser
```

Admin panel:

`/admin/`
