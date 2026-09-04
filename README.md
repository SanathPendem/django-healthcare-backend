# Production-Grade Django Healthcare Backend System

A robust, enterprise-grade Django REST Framework (DRF) backend system designed for healthcare management. It features JWT authentication (`djangorestframework-simplejwt`), custom user management with email credentials, patient isolation security, doctor directory management, and patient-doctor assignment mappings.

---

## Tech Stack & Architecture

- **Language:** Python 3.9+ (Tested on Python 3.11)
- **Framework:** Django 5.1 & Django REST Framework (DRF)
- **Database:** PostgreSQL (with SQLite fallback for local development out-of-the-box via `dj-database-url`)
- **Authentication:** JWT via `djangorestframework-simplejwt`
- **Configuration:** Environment variables managed via `python-dotenv` & `.env`

### Apps Architecture
```
Django/
├── config/             # Django settings, WSGI, ASGI, and root URL routing
├── users/              # Custom User model (email authentication), Register & Login APIs
├── patients/           # Patient CRUD API with creator-ownership authorization
├── doctors/            # Doctor Directory API (viewable by all, editable by creator/admin)
├── mappings/           # Patient-Doctor assignment mappings with duplicate checks
├── tests/              # Automated unit and integration test suite
├── .env.example        # Environment variable template
├── requirements.txt    # Project dependencies
├── postman_collection.json # Ready-to-import Postman API collection
└── manage.py           # Django administrative script
```

---

## Local Setup & Quickstart Guide

### 1. Clone & Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

`.env` configuration defaults:
```env
SECRET_KEY=django-insecure-healthcare-backend-local-dev-secret-key-2026
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/healthcare_db
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=1
```

### 4. Run Migrations & Create Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`.

---

## API Endpoints Specification

### Authentication (`/api/auth/`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Register new user (email, name, password) | Public |
| `POST` | `/api/auth/login/` | Authenticate & receive JWT access + refresh tokens | Public |
| `POST` | `/api/auth/token/refresh/` | Refresh expired access token | Public |

### Patients (`/api/patients/`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/patients/` | Create a new patient record | Authenticated |
| `GET` | `/api/patients/` | List all patients created by the authenticated user | Owner / Admin |
| `GET` | `/api/patients/<id>/` | Retrieve specific patient details | Owner / Admin |
| `PUT` | `/api/patients/<id>/` | Update patient record | Owner / Admin |
| `DELETE` | `/api/patients/<id>/` | Delete patient record | Owner / Admin |

### Doctors (`/api/doctors/`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/doctors/` | Add a doctor to directory | Authenticated |
| `GET` | `/api/doctors/` | List all doctors in directory | Authenticated |
| `GET` | `/api/doctors/<id>/` | Retrieve specific doctor details | Authenticated |
| `PUT` | `/api/doctors/<id>/` | Update doctor details | Creator / Admin |
| `DELETE` | `/api/doctors/<id>/` | Delete doctor record | Creator / Admin |

### Mappings (`/api/mappings/`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/mappings/` | Assign doctor to patient | Patient Owner / Admin |
| `GET` | `/api/mappings/` | List all patient-doctor mappings | Authenticated |
| `GET` | `/api/mappings/<patient_id>/` | List all doctors assigned to a patient | Patient Owner / Admin |
| `DELETE` | `/api/mappings/<id>/` | Remove doctor-patient mapping | Patient Owner / Admin |

---

## Example `curl` Commands

### 1. Register User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Sarah Connor",
    "email": "sarah@example.com",
    "password": "SecurePassword123!"
  }'
```

### 2. Login User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sarah@example.com",
    "password": "SecurePassword123!"
  }'
```

### 3. Create Patient
```bash
curl -X POST http://127.0.0.1:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0199",
    "date_of_birth": "1988-11-23",
    "gender": "Male",
    "medical_history": "Hypertension"
  }'
```

### 4. Create Doctor
```bash
curl -X POST http://127.0.0.1:8000/api/doctors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -d '{
    "name": "Dr. Gregory House",
    "email": "house@diagnostics.org",
    "specialization": "Diagnostic Medicine",
    "experience_years": 15,
    "hospital_affiliation": "Princeton-Plainsboro"
  }'
```

### 5. Assign Doctor to Patient
```bash
curl -X POST http://127.0.0.1:8000/api/mappings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -d '{
    "patient": 1,
    "doctor": 1
  }'
```

### 6. Get Doctors Assigned to Patient
```bash
curl -X GET http://127.0.0.1:8000/api/mappings/1/ \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

---

## Running Automated Tests

Run the Django test suite to execute unit and integration tests across all apps:

```bash
python manage.py test
```

---

## Postman Collection

Import `postman_collection.json` into Postman to test all endpoints. Set the `base_url` variable to `http://127.0.0.1:8000` and pass the returned `access_token` in headers.
