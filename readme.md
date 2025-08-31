# QuickGig Platform

QuickGig is a two-part platform for connecting clients with skilled taskers. It consists of a React/Vite frontend and a Django REST backend.

## Table of Contents

- Overview
- Tech Stack
- Project Structure
- Getting Started
- API Endpoints
- Sample JSON Data
- License

## Overview

- Frontend: Modern, responsive web app for users to browse services, manage profiles, and book taskers.

- Backend: Django REST API for authentication, user management, tasker profiles, and bookings.

## Tech Stack

- Frontend: React, Vite, JavaScript, CSS
- Backend: Django, Django REST Framework, SimpleJWT

## Project Structure

    quickgig/
    ├── quickgig_api/           # Django backend
    │   ├── accounts/           # User & tasker management
    │   ├── services/           # Service definitions
    │   ├── tasks/              # Task and booking logic
    │   ├── media/              # Uploaded files
    │   ├── quickgig_api/       # Django project settings
    │   ├── db.sqlite3          # Database
    │   └── manage.py           # Django CLI
    ├── quickgig_frontend/      # React frontend
    │   ├── public/             # Static assets
    │   ├── src/                # Source code
    │   ├── package.json        # NPM config
    │   ├── vite.config.js      # Vite config
    │   └── README.md           # Frontend docs
    └── README.md               # Main documentation
