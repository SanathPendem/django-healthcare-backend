# Healthcare Backend API

![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)
![Django Framework](https://img.shields.io/badge/django-5.1-green.svg)
![DRF](https://img.shields.io/badge/django%20rest%20framework-3.15-red.svg)
![Authentication](https://img.shields.io/badge/auth-JWT%20(SimpleJWT)-orange.svg)
![Database](https://img.shields.io/badge/database-PostgreSQL%20%7C%20SQLite-darkblue.svg)
![Build & Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

A production-grade, enterprise Django REST Framework (DRF) backend API for healthcare management systems. It provides robust user authentication, patient health records management, doctor directory indexing, and patient-doctor assignment mappings with tenant isolation, strict object-level authorization, input validation, and automated unit/integration tests.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [API Endpoints Specification](#api-endpoints-specification)
  - [Authentication](#1-authentication-apiauth)
  - [Patients](#2-patients-apipatients)
  - [Doctors](#3-doctors-apidoctors)
  - [Patient-Doctor Mappings](#4-patient-doctor-mappings-apimappings)
- [cURL Request Examples](#curl-request-examples)
- [Authentication & Authorization](#authentication--authorization)
- [Security Architecture](#security-architecture)
- [Automated Testing](#automated-testing)
- [Postman Collection](#postman-collection)
- [Django Admin Interface](#django-admin-interface)

---

## Tech Stack

- **Core Framework:** Python 3.11+ & Django 5.1
- **API Engine:** Django REST Framework (DRF) 3.15+
- **Database Engine:** PostgreSQL (with automatic SQLite fallback for local development)
- **Authentication:** JSON Web Tokens (JWT) via `djangorestframework-simplejwt`
- **Environment Management:** `python-dotenv` & `dj-database-url`
- **Testing Framework:** Django TestRunner / `unittest`

---

## Key Features

- **JWT Authentication & Custom User Model:** Custom user model supporting email-based authentication instead of traditional usernames. Token refresh mechanism powered by Simple JWT.
- **Patient Management (CRUD):** Fully isolated Patient management. Non-admin users can only view, update, and delete patient records created by themselves.
- **Doctor Directory Management:** Publicly readable/viewable catalog of doctors with domain-specific fields (specialization, experience, hospital affiliation).
- **Patient-Doctor Assignment Mappings:** Dynamic mapping model allowing patients to be assigned to specific doctors while enforcing uniqueness to prevent duplicate mappings.
- **Strict Data Isolation & Ownership Controls:** Custom DRF permission classes (`IsOwnerOrAdmin`, `IsMappingOwnerOrAdmin`) ensuring strict data boundary enforcement across endpoints.
- **Input Validation & Guardrails:** Serializer-level sanitization preventing invalid inputs, duplicate entries, or unauthorized relation bindings.
- **PostgreSQL Ready:** Configured for cloud-native production deployment with environment-based connection strings.
- **Automated Test Suite:** Comprehensive coverage including user registration, login, token refresh, CRUD permissions, mapping constraints, and security isolation.

---

## Project Structure

```text
healthcare-backend/
├── config/                     # Core Django project configuration
│   ├── settings.py             # Project settings (JWT, DB, Apps, Middleware)
│   ├── urls.py                 # Root URL routing table
│   ├── wsgi.py                 # WSGI production application entrypoint
│   └── asgi.py                 # ASGI application entrypoint
├── users/                      # Custom User authentication app
│   ├── models.py               # Custom User model (Email as USERNAME_FIELD)
│   ├── views.py                # Register & Login API views
│   ├── serializers.py          # User & Auth payload serializers
│   └── urls.py                 # Endpoint routes for /api/auth/
├── patients/                   # Patient records management app
│   ├── models.py               # Patient model definition
│   ├── views.py                # PatientViewSet with owner-filtering
│   ├── permissions.py          # Object-level IsOwnerOrAdmin permission
│   ├── serializers.py          # Patient data serializers
│   └── urls.py                 # Endpoint routes for /api/patients/
├── doctors/                    # Doctor directory management app
│   ├── models.py               # Doctor model definition
│   ├── views.py                # DoctorViewSet (Directory listing & CRUD)
│   ├── serializers.py          # Doctor data serializers
│   └── urls.py                 # Endpoint routes for /api/doctors/
├── mappings/                   # Patient-Doctor assignment mapping app
│   ├── models.py               # PatientDoctorMapping model (Unique constraint)
│   ├── views.py                # MappingViewSet for creating & retrieving mappings
│   ├── permissions.py          # Mapping ownership security rules
│   ├── serializers.py          # Mapping serialization & validation
│   └── urls.py                 # Endpoint routes for /api/mappings/
├── tests/                      # Automated test suite directory
│   ├── test_auth.py            # User registration & authentication tests
│   ├── test_patients.py        # Patient CRUD & access control tests
│   ├── test_doctors.py         # Doctor directory tests
│   └── test_mappings.py        # Patient-Doctor assignment tests
├── manage.py                   # Django management utility script
├── requirements.txt            # Python dependencies specification
├── .env.example                # Sample environment variables configuration file
└── postman_collection.json     # Pre-configured Postman API Collection
```

---

## Setup & Installation

Follow this step-by-step guide to run the healthcare backend application locally.

### Installation Flow

```text
Create Virtual Environment
        ↓
Install Dependencies
        ↓
Configure .env File
        ↓
Configure PostgreSQL Database
        ↓
Execute Database Migrations
        ↓
Create Superuser Account
        ↓
Launch Development Server
```

### Commands

#### 1. Clone Repository & Create Virtual Environment

```bash
# Clone the repository
git clone https://github.com/SanathPendem/django-healthcare-backend.git
cd django-healthcare-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate
```

#### 2. Install Project Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Environment Configuration

Copy `.env.example` to create your local `.env` configuration file:

```bash
# Windows:
copy .env.example .env
# Linux / macOS:
cp .env.example .env
```

#### 4. Run Migrations & Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Create Administrative Superuser

```bash
python manage.py createsuperuser
```

#### 6. Start Development Server

```bash
python manage.py runserver
```

The API server will run at `http://127.0.0.1:8000/`.

---

## Environment Variables

The project utilizes `python-dotenv` to load sensitive environment credentials. Maintain your secrets inside `.env`.

### `.env.example` Template

```env
# Security Configuration
SECRET_KEY=your-custom-production-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration (PostgreSQL)
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432

# Database URL Fallback (Optional)
DATABASE_URL=postgresql://postgres:your-secure-password@localhost:5432/healthcare_db

# JWT Token Expiry Lifetimes
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=1
```

> **Security Alert:** Never commit your actual `.env` file to public source code control. Ensure `.env` is listed inside `.gitignore`.

---

## API Endpoints Specification

### 1. Authentication (`/api/auth/`)

| Method | Endpoint | Description | Access Level |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Register a new user with name, email, and password | Public |
| `POST` | `/api/auth/login/` | Authenticate credentials and retrieve JWT tokens | Public |
| `POST` | `/api/auth/token/refresh/` | Refresh an expired access token using a refresh token | Public |

### 2. Patients (`/api/patients/`)

| Method | Endpoint | Description | Access Level |
|---|---|---|---|
| `POST` | `/api/patients/` | Create a new patient record (auto-binds creator) | Authenticated |
| `GET` | `/api/patients/` | List all patients created by the requesting user | Owner / Admin |
| `GET` | `/api/patients/<id>/` | Retrieve specific patient details by ID | Owner / Admin |
| `PUT` | `/api/patients/<id>/` | Update existing patient details by ID | Owner / Admin |
| `DELETE` | `/api/patients/<id>/` | Delete a patient record by ID | Owner / Admin |

### 3. Doctors (`/api/doctors/`)

| Method | Endpoint | Description | Access Level |
|---|---|---|---|
| `POST` | `/api/doctors/` | Add a new doctor entry to directory | Authenticated |
| `GET` | `/api/doctors/` | List all doctors in the directory | Authenticated |
| `GET` | `/api/doctors/<id>/` | Retrieve detailed information for a doctor | Authenticated |
| `PUT` | `/api/doctors/<id>/` | Update a doctor's details | Creator / Admin |
| `DELETE` | `/api/doctors/<id>/` | Remove a doctor entry from directory | Creator / Admin |

### 4. Patient-Doctor Mappings (`/api/mappings/`)

| Method | Endpoint | Description | Access Level |
|---|---|---|---|
| `POST` | `/api/mappings/` | Assign a doctor to an owned patient | Patient Owner / Admin |
| `GET` | `/api/mappings/` | List all mappings for patients owned by request user | Patient Owner / Admin |
| `GET` | `/api/mappings/<patient_id>/` | List all doctors assigned to a specific patient ID | Patient Owner / Admin |
| `DELETE` | `/api/mappings/<id>/` | Remove a patient-doctor mapping by mapping ID | Patient Owner / Admin |

---

## cURL Request Examples

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

### 2. Login User (Obtain JWT Token)

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sarah.connor@hospital.org",
    "password": "SecurePassword123!"
  }'
```

*Response:*
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

### 6. Get Doctors Assigned to Patient

```bash
curl -X GET http://127.0.0.1:8000/api/mappings/1/ \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

---

## Authentication & Authorization

This API uses **JWT (JSON Web Tokens)** for stateless authentication.

### Token Usage Header

After calling `/api/auth/login/`, pass the returned `access` token in the request header for protected routes:

```http
Authorization: Bearer <your_access_token>
```

### Authorization Rules

- **Patient Ownership Isolation:** `PatientViewSet` filters the queryset dynamically so users can only access patient records where `created_by == request.user` (Superusers can access all).
- **Mapping Authorization:** A user can only assign doctors to patients that they own. Attempts to map another user's patient yield a `403 Forbidden` error.

---

## Security Architecture

- **JWT Authentication:** Secure token validation using RS256 / HS256 signatures via `djangorestframework-simplejwt`.
- **Password Hashing:** Industry-standard password hashing using Django's default PBKDF2 algorithm with HMAC and SHA256.
- **Object-Level Authorization:** Custom DRF permission classes (`IsOwnerOrAdmin`, `IsMappingOwnerOrAdmin`) verifying object ownership per request.
- **Database Integrity & Constraints:** `UniqueConstraint` on `PatientDoctorMapping` models preventing duplicate doctor-patient bindings at the database level.
- **Strict Input Sanitization:** Serializers validate email formats, dates, required fields, and prevent mass assignment vulnerabilities.
- **Secrets Management:** Environment variables isolate database passwords, secret keys, and runtime flags.

---

## Automated Testing

The project includes an automated unit and integration test suite covering authentication, patient ownership, doctor directory management, and patient-doctor mappings.

### Running Tests

Execute the Django test runner:

```bash
python manage.py test
```

### Tested Scenarios

- **User Authentication:** Registration, valid/invalid logins, token issuance, refresh token rotation.
- **Patient Isolation:** Verifying non-admin users cannot access or edit patients owned by other users.
- **Doctor Directory:** Verifying list/retrieve capabilities and authorized creation.
- **Mapping Constraints:** Preventing duplicate patient-doctor mappings and unauthorized patient mappings.

---

## Postman Collection

A pre-configured Postman API collection is included in the project root: `postman_collection.json`.

### How to Use

1. Open **Postman**.
2. Click **Import** and select `postman_collection.json`.
3. Set the environment variable `base_url` to `http://127.0.0.1:8000`.
4. Run the **Login** request to automatically copy the `access_token` into your collection authorization parameters.

---

## Django Admin Interface

The Django Admin interface is enabled for superusers to manage users, patients, doctors, and mappings visually.

### Accessing Admin Panel

1. Ensure a superuser has been created:
   ```bash
   python manage.py createsuperuser
   ```
2. Start the dev server and navigate to:
   ```text
   http://127.0.0.1:8000/admin/
   ```
