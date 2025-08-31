# QuickGig Frontend

QuickGig Frontend is a modern web application built with React and Vite, serving as the user interface for the __QuickGig platform__.
It allows __clients__ to find and book services from __taskers__ (service providers) through a smooth, responsive interface.

## Table of Contents

- Features
- Tech Stack
- Project Structure
- Getting Started
- Available Scripts

## Features

- Authentication (login, register, logout with JWT)

- Tasker Cards with service details

- Booking Flow

  - Select tasker

  - Choose availability slot

  - Add description

  - Confirm booking

- Dashboard

  - Toggle between Client Mode and Tasker Mode

  - View created tasks (as client)

  - View assigned tasks (as tasker)

## Tech Stack

- Vite
- React
- Zustand (state management)
- Axios (API calls)
- React-Router-Dom (navigation)
- TailwindCSS

## Project Structure

    quickgig_frontend/
    ├── public/                # Static assets
    ├── src/
    │   ├── assets/            # Images, icons, logos
    │   ├── components/        # Reusable UI components
    │   ├── pages/             # Application pages (Home, Login, Dashboard, etc.)
    │   ├── services/          # API calls and service logic
    │   ├── stores/            # State management
    │   ├── App.jsx            # Main app component
    │   ├── main.jsx           # Entry point
    │   └── index.css          # Global styles
    ├── package.json           # Project metadata and scripts
    ├── vite.config.js         # Vite configuration
    └── README.md              # Project documentation

## Getting Started

1. Install dependencies:

    ```powershell
    npm install
    ```

2. Start the development server:

    ```powershell
    npm run dev
    ```

3. Open in browser: Visit [http://localhost:5173](http://localhost:5173) (default Vite port).

## Available Scripts

- `npm run dev` — Start development server
- `npm run build` — Build for production
- `npm run preview` — Preview production build

## Authentication

- Auth state is managed via Zustand + `localStorage`.

- Tokens are obtained from the Django backend (`/api/auth/login/`).

- Use `Authorization: Bearer <token>` header automatically via Axios.

## API Integration

The frontend communicates with the __QuickGig Django API__.

```json
    {
        "client": 1,
        "tasker": 5,
        "task": 3,
        "availability_slot": 10,
        "description": "Deep cleaning for 2 rooms"
    }
```
