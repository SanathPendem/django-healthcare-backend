# Healthcare Backend API

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![Django Framework](https://img.shields.io/badge/django-5.1-green.svg)
![DRF](https://img.shields.io/badge/django%20rest%20framework-3.15-red.svg)
![Authentication](https://img.shields.io/badge/auth-JWT%20(SimpleJWT)-orange.svg)
![Database](https://img.shields.io/badge/database-PostgreSQL-darkblue.svg)
![Build & Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

An enterprise-grade, production-ready Django REST Framework (DRF) backend API for healthcare management systems. It features secure **JWT authentication**, **tenant-isolated patient record management**, a **doctor directory**, and **patient-doctor assignment mappings** backed by a **PostgreSQL** database.

---

## 📌 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Prerequisites](#-prerequisites)
- [Quickstart Guide](#-quickstart-guide)
- [Environment Configuration](#-environment-configuration)
- [API Reference](#-api-reference)
  - [1. Authentication](#1-authentication-api-auth)
  - [2. Patients](#2-patients-api-patients)
  - [3. Doctors](#3-doctors-api-doctors)
  - [4. Patient-Doctor Mappings](#4-patient-doctor-mappings-api-mappings)
- [cURL Request Examples](#-curl-request-examples)
- [Security & Access Control](#-security--access-control)
- [Automated Testing](#-automated-testing)
- [Postman Collection](#-postman-collection)

---

## ✨ Features

- 🔐 **JWT Authentication & Custom User Model**: Email-based authentication (no usernames required) using `djangorestframework-simplejwt`.
- 🩺 **Patient Management (CRUD)**: Tenant-isolated patient record administration. Non-admin users can only view, update, and delete patient records they created.
- 👨‍⚕️ **Doctor Directory**: Catalog indexing medical practitioners, specializations, experience, and hospital affiliations.
- 🔗 **Patient-Doctor Mappings**: Relational mapping linking patients to assigned doctors with database-level uniqueness constraints to prevent duplicate mappings.
- 🛡️ **Strict Data Isolation**: Object-level permissions (`IsOwnerOrAdmin`, `IsMappingOwnerOrAdmin`) ensuring strict boundaries across all endpoints.
- 🐘 **PostgreSQL Powered**: Built and optimized for PostgreSQL databases with indexed lookups and transaction safety.
- 🧪 **Automated Testing**: 100% test pass rate covering authentication, data isolation, mapping rules, and error handling.

---

## 🚀 Tech Stack

- **Framework:** Python 3.11+ & Django 5.1
- **API Engine:** Django REST Framework (DRF) 3.15+
- **Database Engine:** PostgreSQL
- **Authentication:** JSON Web Tokens (JWT) via `djangorestframework-simplejwt`
- **Environment Management:** `python-dotenv` & `dj-database-url`
- **Testing:** Django TestRunner (`unittest`)

---

## 📁 Project Architecture

```text
django-healthcare-backend/
├── config/                     # Core Django project configuration & settings
│   ├── settings.py             # Global settings (JWT, PostgreSQL, Apps)
│   ├── urls.py                 # Main API router table
│   ├── wsgi.py                 # Production WSGI entrypoint
│   └── asgi.py                 # Async ASGI entrypoint
├── users/                      # Custom User authentication module
│   ├── models.py               # Custom User model (Email as USERNAME_FIELD)
│   ├── views.py                # Register & Login API views
│   └── serializers.py          # Auth payload serializers
├── patients/                   # Patient records management module
│   ├── models.py               # Patient data model
│   ├── views.py                # PatientViewSet with tenant filtering
│   └── permissions.py          # Object-level ownership permissions
├── doctors/                    # Doctor directory management module
│   ├── models.py               # Doctor data model
│   └── views.py                # DoctorViewSet catalog endpoints
├── mappings/                   # Patient-Doctor assignment module
│   ├── models.py               # Mapping model (Unique constraint)
│   └── views.py                # MappingViewSet assignment endpoints
├── tests/                      # Automated test suite
│   ├── test_auth.py            # Registration & JWT auth tests
│   ├── test_patients.py        # Patient CRUD & access control tests
│   ├── test_doctors.py         # Doctor directory tests
│   └── test_mappings.py        # Patient-Doctor mapping tests
├── manage.py                   # Django CLI management utility
├── requirements.txt            # Python dependencies list
├── .env.example                # Sample environment configuration template
└── postman_collection.json     # Pre-configured Postman API collection
```

---

## 📋 Prerequisites

Before running the project locally, ensure you have installed:
- **Python 3.11+**
- **PostgreSQL 14+** (running locally on port `5432`)
- **Git**

---

## ⚡ Quickstart Guide

Follow these steps to run the application on your local machine:

### 1. Clone Repository & Set Up Virtual Environment

```bash
# Clone the repository
git clone https://github.com/SanathPendem/django-healthcare-backend.git
cd django-healthcare-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate
# Linux / macOS:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create your local `.env` file from `.env.example`:

```bash
# Windows:
copy .env.example .env

# Linux / macOS:
cp .env.example .env
```

### 4. Set Up PostgreSQL & Run Migrations

Ensure PostgreSQL is running, then run database migrations:

```bash
python manage.py migrate
```

### 5. Create an Admin Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Start Development Server

```bash
python manage.py runserver
```

The API server will run at: **`http://127.0.0.1:8000/`**

---

## ⚙️ Environment Configuration

Environment settings are managed using `python-dotenv`. Update your `.env` file with your local database credentials:

```env
# Security Configuration
SECRET_KEY=django-insecure-healthcare-backend-local-dev-secret-key-2026
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# PostgreSQL Connection Credentials
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/healthcare_db

# JWT Token Expiry (Minutes / Days)
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=1
```

---

## 🔌 API Reference

### 1. Authentication (`/api/auth/`)

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Register a new user with name, email, and password | Public |
| `POST` | `/api/auth/login/` | Authenticate credentials & return JWT access/refresh tokens | Public |
| `POST` | `/api/auth/token/refresh/` | Obtain a new access token using a valid refresh token | Public |

### 2. Patients (`/api/patients/`)

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/patients/` | List all patient records owned by requesting user | Owner / Admin |
| `POST` | `/api/patients/` | Create a new patient record (automatically binds creator) | Authenticated |
| `GET` | `/api/patients/<id>/` | Retrieve details for a specific patient by ID | Owner / Admin |
| `PUT` | `/api/patients/<id>/` | Update a patient record by ID | Owner / Admin |
| `DELETE` | `/api/patients/<id>/` | Delete a patient record by ID | Owner / Admin |

### 3. Doctors (`/api/doctors/`)

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/doctors/` | List all doctors in the directory | Authenticated |
| `POST` | `/api/doctors/` | Add a new doctor entry to directory | Authenticated |
| `GET` | `/api/doctors/<id>/` | Retrieve details for a specific doctor by ID | Authenticated |
| `PUT` | `/api/doctors/<id>/` | Update doctor details by ID | Creator / Admin |
| `DELETE` | `/api/doctors/<id>/` | Remove a doctor entry from directory | Creator / Admin |

### 4. Patient-Doctor Mappings (`/api/mappings/`)

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/mappings/` | List mappings for patients owned by requesting user | Patient Owner / Admin |
| `POST` | `/api/mappings/` | Assign a doctor to an owned patient | Patient Owner / Admin |
| `GET` | `/api/mappings/<patient_id>/` | List all doctors assigned to a specific patient ID | Patient Owner / Admin |
| `DELETE` | `/api/mappings/<id>/` | Remove a patient-doctor mapping by mapping ID | Patient Owner / Admin |

---

## 💻 cURL Request Examples

### 1. Register User

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Sarah Connor",
    "email": "sarah.connor@hospital.org",
    "password": "SecurePassword123!"
  }'
```

### 2. Login User & Obtain JWT Tokens

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sarah.connor@hospital.org",
    "password": "SecurePassword123!"
  }'
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "sarah.connor@hospital.org",
    "name": "Dr. Sarah Connor"
  }
}
```

### 3. Create Patient Record

```bash
curl -X POST http://127.0.0.1:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0199",
    "date_of_birth": "1990-05-15",
    "gender": "Male",
    "medical_history": "Hypertension, Asthma"
  }'
```

### 4. Create Doctor Entry

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

---

## 🔒 Security & Access Control

- **Stateless JWT Authorization**: All protected endpoints require a valid `Bearer <access_token>` in the `Authorization` header.
- **Tenant Isolation**: Non-admin users can only view and modify patient records that they created (`created_by == request.user`).
- **Mapping Constraints**: Users can only create mappings for patients they own. Attempts to assign doctors to patients owned by another user yield a `403 Forbidden` response.
- **Database Unique Constraint**: Unique constraint on `('patient', 'doctor')` prevents duplicate doctor assignments.

---

## 🧪 Automated Testing

Run the full Django test suite:

```bash
python manage.py test
```

**Test Coverage Highlights:**
- User registration, login, and JWT token rotation.
- Tenant isolation ensuring users cannot access other users' patient records.
- Doctor directory creation and listing permissions.
- Unique constraints and ownership rules for patient-doctor mappings.

---

## 📬 Postman Collection

A pre-configured Postman API collection is included in the project root: `postman_collection.json`.

1. Open **Postman** and click **Import**.
2. Select `postman_collection.json`.
3. Set the collection variable `base_url` to `http://127.0.0.1:8000`.
4. Execute the **Login** request; the `access_token` will automatically populate for subsequent requests.
