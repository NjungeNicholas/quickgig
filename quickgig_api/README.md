# QuickGig API (Django + DRF)

QuickGig is a service marketplace platform where clients can book services from taskers (freelancers/service providers).
This API powers the QuickGig frontend (React).

---

## Features

- JWT Authentication (Login, Register, Logout)

- User Roles (Client, Tasker, or Both)

- Tasker Profiles (bio, skills, availability slots)

- Availability Slots for booking scheduling

- Bookings System (clients create bookings, taskers receive assignments)

- Reviews & Ratings (future feature)

## Project Structure

    quickgig-api/
    ├── bookings/           # Booking models, serializers, views
    ├── tasks/              # Tasks and services
    ├── users/              # Custom user model, registration, profiles
    ├── availability/       # Tasker availability slots
    ├── quickgig/           # Project config (settings, urls)
    └── requirements.txt

## Getting started

1. Create a virtual environment

    ```powershell
    python -m venv venv
    source venv/bin/activate   # macOS/Linux
    venv\Scripts\activate      # Windows
    ```

2. Install dependencies

    ```powershell
    pip install -r requirements.txt
    ```

3. Run migrations

    ```powershell
    python manage.py migrate
    ```

4. Run server

    ```powershell
    python manage.py runserver
    ```

Server runs at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Authentication

- Login & Registration use JWT (SimpleJWT)

- Endpoints:

  - POST /api/auth/register/ → Register new user

  - POST /api/auth/login/ → Obtain JWT token

  - POST /api/auth/refresh/ → Refresh access token

Use the `Authorization: Bearer <token>` header for protected routes.

## API Endpoints

Booking Payload Example:

```json
{
  "client": 1,
  "tasker": 5,
  "task": 3,
  "availability_slot": 10,
  "description": "Deep cleaning for 2 rooms"
}
```
