# Fast Python API (Test Assignment)

**This project is a [test assignment](https://basalt-crabapple-753.notion.site/Python-150fd978e02c800b91b3eabcb85a57b0) for the Python Intern / Backend Developer position.**


[![Maintainability](https://api.codeclimate.com/v1/badges/3330a77ad116c8b50205/maintainability)](https://codeclimate.com/github/Asgef/fast_python_api/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/3330a77ad116c8b50205/test_coverage)](https://codeclimate.com/github/Asgef/fast_python_api/test_coverage)

## Overview

- **Description:**\
  This project is a REST API built with FastAPI that integrates external data sources (e.g. the [RandomUser API](https://randomuser.me)), implements CRUD operations for user management, and uses JWT for authentication and authorization.

- **Key Features:**

  - Integration with an external API.
  - CRUD operations for users (create, read, update, delete).
  - Authentication and authorization using JWT.
  - Auto-generated API documentation using Swagger (and ReDoc).
  - (Optional) Docker containerization.
  - CI/CD for automated testing and deployment.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)

## Technologies

- **Backend Framework:** FastAPI
- **Database:** PostgreSQL / SQLite (configurable via environment variables)
- **ORM:** SQLAlchemy (with asynchronous support)
- **Authentication:** JWT
- **HTTP Client:** aiohttp
- **Containerization:** Docker (optional)
- **CI/CD:** e.g., GitHub Actions

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/fast_python_api.git
   cd fast_python_api
   ```

2. **Install dependencies:**

   ```bash
   make install
   ```

3. **Create a `.env` file:**\
   Example content:

   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/db_name
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

   **Generate a secure secret key:**

   ```bash
   openssl rand -hex 32
   ```

4. **Apply database migrations:**

   ```bash
   make migrate_up
   ```

## Running the Application

- **Start locally with Uvicorn:**
  ```bash
  make start
  ```
  The API will be available at `http://127.0.0.1:8000`.




## Testing

- **Run tests with pytest:**
  ```bash
  make test
  ```

### API Tests with cURL


#### Get Access Token

```
curl -X 'POST' \                                                                          
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=johndoe&password=secret&scope=&client_id=string&client_secret=string'
```

#### Fetch Current User Data

```
curl -X 'GET' \
  'http://127.0.0.1:8000/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwicm9sZSI6ImFkbWluIiwiaWQiOiI2YzNiMzYwOS02ZmFlLTRhNzEtYTlmZC05NGVhYWJmMTJjOWEiLCJleHAiOjE3NDA2NjU0NDd9.fBFqZ3fACGRT_6P-GaiO1koxOc40nAnARJmtKPZq2-8'
```

#### Get List of Users
```
curl -X 'GET' \
  'http://127.0.0.1:8000/users/?skip=0&limit=5' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwicm9sZSI6ImFkbWluIiwiaWQiOiI2YzNiMzYwOS02ZmFlLTRhNzEtYTlmZC05NGVhYWJmMTJjOWEiLCJleHAiOjE3NDA2NjU0NDd9.fBFqZ3fACGRT_6P-GaiO1koxOc40nAnARJmtKPZq2-8'
```

#### Create a New User

```
curl -X 'POST' \
  'http://127.0.0.1:8000/users/create' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwicm9sZSI6ImFkbWluIiwiaWQiOiI2YzNiMzYwOS02ZmFlLTRhNzEtYTlmZC05NGVhYWJmMTJjOWEiLCJleHAiOjE3NDA2NjU0NDd9.fBFqZ3fACGRT_6P-GaiO1koxOc40nAnARJmtKPZq2-8' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": {
    "title": "Ms",
    "first_name": "Alice",
    "last_name": "Smith"
  },
  "login": {
    "username": "alice_smith",
    "role": "user",
    "password": "my_secret_password"
  },
  "dob": "1990-01-01",
  "city": "New York",
  "email": "alice@example.com"
}'
```

#### Delete a User

```
curl -X 'DELETE' \
  'http://127.0.0.1:8000/users/c647e0c3-d0fb-47fd-bbea-c61b3cd999dd' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwicm9sZSI6ImFkbWluIiwiaWQiOiI2YzNiMzYwOS02ZmFlLTRhNzEtYTlmZC05NGVhYWJmMTJjOWEiLCJleHAiOjE3NDA2NjU0NDd9.fBFqZ3fACGRT_6P-GaiO1koxOc40nAnARJmtKPZq2-8'
```

#### Test an external service

```
curl -X 'GET' \
  'http://127.0.0.1:8000/test?results=5' \
  -H 'accept: application/json'
```

#### Get user data from external service

```
curl -X 'POST' \
  'http://127.0.0.1:8000/import?results=5' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwicm9sZSI6ImFkbWluIiwiaWQiOiI2YzNiMzYwOS02ZmFlLTRhNzEtYTlmZC05NGVhYWJmMTJjOWEiLCJleHAiOjE3NDA2NjU0NDd9.fBFqZ3fACGRT_6P-GaiO1koxOc40nAnARJmtKPZq2-8' \
  -d ''
```

## API Documentation

- **Swagger UI:**\
  Visit `http://127.0.0.1:8000/docs` for interactive API documentation.
- **ReDoc:**\
  Alternatively, visit `http://127.0.0.1:8000/redoc` for another view.

## Deployment

- **Deployment Platforms:**\
  The application is deployed on **Render** and can be accessed at: [Deployment Link Placeholder].
- **Deployment Steps:**
  - Configure environment variables on your chosen platform.
  - Set up CI/CD if required.
  - Provide a link to the deployed service once live.

