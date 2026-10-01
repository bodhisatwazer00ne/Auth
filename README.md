# Auth Web API

A FastAPI authentication API using PostgreSQL, SQLAlchemy, Pydantic, password hashing, and JWT-based authentication. The project is containerized using Docker.

---

# Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* PyJWT
* pwdlib
* Docker
* Docker Compose

---

# Project Structure

```text
Auth/
│
├── main.py
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

# Features

* User registration
* Secure password hashing
* User login
* JWT access tokens
* Protected `/me` endpoint
* PostgreSQL database
* SQLAlchemy ORM
* Dockerized application

---

# API Endpoints

| Method | Endpoint    | Purpose                               |
| ------ | ----------- | ------------------------------------- |
| POST   | `/register` | Create a new user                     |
| POST   | `/login`    | Authenticate a user and receive a JWT |
| GET    | `/me`       | Get the currently authenticated user  |

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

---

# Installation Using Docker

Docker allows the project to run without manually installing Python dependencies or configuring the Python environment.

## 1. Install Docker Desktop

Install Docker Desktop for your operating system.

After installation, start Docker Desktop.

Verify the installation:

```bash
docker version
```

You should see both:

```text
Client:
...

Server:
...
```

The `Server` section confirms that the Docker Engine is running.

---

# 2. Clone the Repository

Clone the project:

```bash
git clone <YOUR_REPOSITORY_URL>
```

Enter the project directory:

```bash
cd Auth
```

---

# 3. Environment Variables

Create a `.env` file in the project directory.

Example:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

## SECRET_KEY

Used to sign JWT tokens.

## DATABASE_URL

Used by SQLAlchemy to connect to PostgreSQL.

Do not commit `.env` to GitHub.

Add it to `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
venv/
.venv/
```

---

# 4. Run Using Docker Compose

If the project contains `docker-compose.yml`, run:

```bash
docker compose up --build
```

Docker Compose will:

```text
Read docker-compose.yml
        ↓
Build the Docker image
        ↓
Create the required containers
        ↓
Start the application
```

---

# 5. Run in the Background

To run the containers without keeping the terminal occupied:

```bash
docker compose up --build -d
```

Check the containers:

```bash
docker compose ps
```

---

# 6. Access the API

Once the application is running:

```text
http://localhost:8000
```

FastAPI's interactive documentation:

```text
http://localhost:8000/docs
```

You can use Swagger to test:

```text
POST /register
POST /login
GET /me
```

---

# 7. View Docker Logs

View logs:

```bash
docker compose logs
```

Continuously follow logs:

```bash
docker compose logs -f
```

---

# 8. Stop the Application

Stop the Docker Compose services:

```bash
docker compose down
```

Start them again:

```bash
docker compose up -d
```

---

# 9. Rebuild After Code Changes

If you change the application code or Docker configuration:

```bash
docker compose down
docker compose up --build
```

Or:

```bash
docker compose up --build -d
```

---

# Running the Docker Hub Image

The application image is available on Docker Hub as:

```text
bosatsu00/auth-web
```

## Pull the Image

```bash
docker pull bosatsu00/auth-web:latest
```

## Run the Container

```bash
docker run -d \
  --name auth-web \
  -p 8000:8000 \
  bosatsu00/auth-web:latest
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# Docker Container Commands

List running containers:

```bash
docker ps
```

List all containers:

```bash
docker ps -a
```

View logs:

```bash
docker logs auth-web
```

Follow logs:

```bash
docker logs -f auth-web
```

Stop the container:

```bash
docker stop auth-web
```

Start the container:

```bash
docker start auth-web
```

Remove the container:

```bash
docker rm auth-web
```

---

# Building the Docker Image

To build the image locally using the `Dockerfile`:

```bash
docker build -t auth-web .
```

Check the image:

```bash
docker images
```

Run it:

```bash
docker run -d \
  --name auth-web \
  -p 8000:8000 \
  auth-web
```

---

# Pushing to Docker Hub

Login:

```bash
docker login
```

Build and tag the image:

```bash
docker build -t bosatsu00/auth-web:latest .
```

Push it:

```bash
docker push bosatsu00/auth-web:latest
```

Other users can then download it with:

```bash
docker pull bosatsu00/auth-web:latest
```

---

# Code Explanation

This section explains the code in a concise way to help understand how the project works.

---

# 1. auth.py

`auth.py` handles authentication-related functionality:

* Password hashing
* Password verification
* JWT creation
* JWT verification
* OAuth2 bearer token extraction

## Imports

```python
import os
```

Used to access environment variables.

```python
import jwt
```

PyJWT library used to create and decode JWT tokens.

```python
from fastapi.security import OAuth2PasswordBearer
```

Provides FastAPI's OAuth2 bearer-token mechanism.

```python
from datetime import datetime, timedelta, timezone
```

Used to create the JWT expiration time.

```python
from dotenv import load_dotenv
```

Loads variables from the `.env` file.

```python
from pwdlib import PasswordHash
```

Provides secure password hashing and verification.

---

## Environment Variables

```python
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
```

`load_dotenv()` loads values from `.env`.

`SECRET_KEY` is used to sign JWT tokens.

---

## OAuth2 Scheme

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
```

Defines a bearer-token authentication scheme.

The client sends the JWT as:

```text
Authorization: Bearer <token>
```

`tokenUrl="login"` tells FastAPI that `/login` is the endpoint used to obtain the token.

It does not itself create or retrieve the token.

---

## Password Hashing

```python
password_hash = PasswordHash.recommended()
```

Creates a password hashing system using `pwdlib`.

```python
def hash_password(password: str):
    return password_hash.hash(password)
```

Converts a plain password into a secure hash.

```text
Plain password
      ↓
hash_password()
      ↓
Password hash
```

The plain password should not be stored in the database.

---

## Password Verification

```python
def verify_password(
    plain_password: str,
    hashed_password: str
):
    return password_hash.verify(
        plain_password,
        hashed_password
    )
```

Checks whether the entered password matches the stored password hash.

Returns:

```text
True
```

or:

```text
False
```

---

## JWT Configuration

```python
ALGORITHM = "HS256"
```

Defines the JWT signing algorithm.

---

## Creating an Access Token

```python
def create_access_token(username: str):
```

Creates a JWT for the authenticated user.

```python
expire = datetime.now(timezone.utc) + timedelta(minutes=30)
```

Sets the token to expire after 30 minutes.

```python
payload = {
    "sub": username,
    "exp": expire
}
```

The payload contains:

* `sub` — subject; here it stores the username
* `exp` — expiration time

```python
token = jwt.encode(
    payload,
    SECRET_KEY,
    ALGORITHM
)
```

Signs the payload using the secret key and HS256.

---

## Decoding the Access Token

```python
def decode_access_token(token: str):
```

Receives a JWT and verifies it.

```python
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)
```

Checks the JWT's:

* Signature
* Secret key
* Algorithm
* Expiration

If the token is invalid or expired, PyJWT raises an exception.

---

# 2. database.py

`database.py` manages the SQLAlchemy connection and database sessions.

## Imports

```python
import os
```

Used to access environment variables.

```python
from dotenv import load_dotenv
```

Loads `.env`.

```python
from sqlalchemy.orm import sessionmaker, DeclarativeBase
```

* `sessionmaker` creates database sessions.
* `DeclarativeBase` is used as the base class for SQLAlchemy models.

```python
from sqlalchemy import create_engine
```

Creates the SQLAlchemy database engine.

---

## Database URL

```python
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
```

Gets the PostgreSQL connection URL from `.env`.

---

## Engine

```python
engine = create_engine(DATABASE_URL)
```

Creates the connection mechanism between SQLAlchemy and PostgreSQL.

```text
Python
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

---

## Session Factory

```python
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
```

Creates a factory for database sessions.

A session is used to:

* Query data
* Insert data
* Update data
* Delete data
* Commit transactions

---

## Base Class

```python
class Base(DeclarativeBase):
    pass
```

All SQLAlchemy models inherit from `Base`.

Example:

```python
class User(Base):
```

This allows SQLAlchemy to recognize the model.

---

## Database Dependency

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Creates a database session for a request.

Flow:

```text
Request
   ↓
Create session
   ↓
Use database
   ↓
Request finishes
   ↓
Close session
```

`yield` allows FastAPI to manage the dependency.

---

# 3. models.py

`models.py` defines the database tables using SQLAlchemy.

## Imports

```python
from sqlalchemy import String
```

Used for string columns.

```python
from sqlalchemy.orm import Mapped, mapped_column
```

Used for SQLAlchemy's modern typed model definitions.

```python
from database import Base
```

Imports the SQLAlchemy base class.

---

## User Model

```python
class User(Base):
```

Creates a SQLAlchemy model representing a database table.

```python
__tablename__ = "users"
```

Specifies that the PostgreSQL table is called `users`.

---

## ID

```python
id: Mapped[int] = mapped_column(
    primary_key=True
)
```

Creates an integer primary key.

`primary_key=True` makes the value unique for each row.

---

## Username

```python
username: Mapped[str] = mapped_column(
    String(50),
    unique=True,
    index=True
)
```

Creates the username column.

* `String(50)` — maximum length
* `unique=True` — duplicate usernames are not allowed
* `index=True` — creates an index for faster searches

---

## Password Hash

```python
password_hash: Mapped[str] = mapped_column(
    String(255)
)
```

Stores the password hash.

The original password is not stored.

---

# 4. schemas.py

`schemas.py` defines the structure of API input using Pydantic.

## Import

```python
from pydantic import BaseModel
```

Pydantic validates incoming data.

---

## Registration Schema

```python
class UserRegister(BaseModel):
    username: str
    password: str
```

Defines the data expected by `/register`.

Example:

```json
{
    "username": "john",
    "password": "secret123"
}
```

---

## Login Schema

```python
class UserLogin(BaseModel):
    username: str
    password: str
```

Defines the data expected by `/login`.

---

## Schema vs Model

This distinction is important:

```text
schemas.py
     ↓
API input validation

models.py
     ↓
Database table structure
```

`UserRegister` and `UserLogin` are Pydantic schemas.

`User` is a SQLAlchemy database model.

---

# 5. main.py

`main.py` is the main FastAPI application.

It connects:

* API routes
* Schemas
* Database
* Models
* Authentication

---

## Imports

```python
from fastapi import FastAPI, Depends, HTTPException
```

* `FastAPI` creates the application.
* `Depends` provides dependencies.
* `HTTPException` returns HTTP errors.

```python
from sqlalchemy.orm import Session
```

Provides the SQLAlchemy session type.

```python
from database import engine, Base, get_db
```

Imports:

* `engine` — database connection
* `Base` — SQLAlchemy model base
* `get_db` — database session dependency

```python
from models import User
```

Imports the database `User` model.

```python
from schemas import UserRegister, UserLogin
```

Imports request-validation schemas.

```python
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    oauth2_scheme
)
```

Imports authentication functions and the OAuth2 scheme.

---

# Creating Database Tables

```python
Base.metadata.create_all(bind=engine)
```

SQLAlchemy checks the models registered with `Base` and creates their tables if they do not already exist.

For this project:

```text
User model
    ↓
users table
```

---

# Creating FastAPI

```python
app = FastAPI()
```

Creates the FastAPI application.

---

# Registration Endpoint

```python
@app.post("/register")
```

Creates:

```text
POST /register
```

Function:

```python
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
```

Two values are provided:

```text
user
 ↓
Validated request body

db
 ↓
Database session
```

---

## Check Existing User

```python
existing_user = db.query(User).filter(
    User.username == user.username
).first()
```

Searches the `users` table for the username.

Conceptually:

```sql
SELECT *
FROM users
WHERE username = '...'
LIMIT 1;
```

---

## Duplicate Username

```python
if existing_user:
    raise HTTPException(
        status_code=409,
        detail="Username already exists"
    )
```

Returns HTTP `409 Conflict`.

---

## Create User

```python
new_user = User(
    username=user.username,
    password_hash=hash_password(user.password)
)
```

The password is hashed before being stored.

```text
Plain password
      ↓
hash_password()
      ↓
Password hash
      ↓
User model
      ↓
PostgreSQL
```

---

## Save User

```python
db.add(new_user)
db.commit()
db.refresh(new_user)
```

* `add()` — adds the object to the session
* `commit()` — saves changes to the database
* `refresh()` — retrieves the latest database state

---

# Login Endpoint

```python
@app.post("/login")
```

Creates:

```text
POST /login
```

---

## Find User

```python
db_user = db.query(User).filter(
    User.username == user.username
).first()
```

Searches for the username.

---

## Check Username

```python
if not db_user:
```

If the user does not exist, the API returns:

```text
401 Unauthorized
```

---

## Verify Password

```python
verify_password(
    user.password,
    db_user.password_hash
)
```

Compares:

```text
Entered password
       ↓
verify_password()
       ↑
Stored password hash
```

---

## Create JWT

```python
access_token = create_access_token(
    db_user.username
)
```

Calls `create_access_token()` from `auth.py`.

The response contains:

```json
{
    "access_token": "...",
    "token_type": "bearer"
}
```

---

# `/me` Endpoint

```python
@app.get("/me")
```

Creates:

```text
GET /me
```

This endpoint requires a JWT.

---

## Extract Token

```python
def get_me(
    token: str = Depends(oauth2_scheme)
):
```

FastAPI extracts the token from:

```text
Authorization: Bearer <JWT>
```

---

## Decode Token

```python
payload = decode_access_token(token)
```

Calls `decode_access_token()` from `auth.py`.

The JWT is verified using:

```text
SECRET_KEY
+
HS256
+
Expiration
```

---

## Handle Invalid Token

```python
except jwt.InvalidTokenError:
```

Catches invalid or expired JWT errors.

Returns:

```text
401 Unauthorized
```

---

## Get Username

```python
username = payload.get("sub")
```

The JWT was created with:

```python
"sub": username
```

Therefore, `/me` retrieves the username from the token.

---

# Complete Authentication Flow

## Registration

```text
POST /register
      ↓
UserRegister schema
      ↓
Validate input
      ↓
Check username
      ↓
Hash password
      ↓
User model
      ↓
SQLAlchemy
      ↓
PostgreSQL
```

## Login

```text
POST /login
      ↓
UserLogin schema
      ↓
Find user
      ↓
Verify password
      ↓
Create JWT
      ↓
Return token
```

## Access Protected Endpoint

```text
GET /me
      +
Authorization: Bearer <JWT>
      ↓
oauth2_scheme
      ↓
Extract token
      ↓
decode_access_token()
      ↓
Verify JWT
      ↓
Read "sub"
      ↓
Return username
```

---

# Important Concepts

## FastAPI

Framework used to build the REST API.

## Pydantic

Used to validate and structure API input.

## SQLAlchemy

ORM used to communicate with PostgreSQL using Python objects.

## PostgreSQL

Database used to store users.

## pwdlib

Used to securely hash and verify passwords.

## JWT

JSON Web Token used for authentication.

## OAuth2 Bearer Token

The client sends the JWT using:

```text
Authorization: Bearer <token>
```

## Dependency Injection

FastAPI provides dependencies using:

```python
Depends(get_db)
```

This allows routes to receive a database session without manually creating one.

## Environment Variables

Sensitive configuration such as:

```text
SECRET_KEY
DATABASE_URL
```

is kept outside the source code.

---

# Docker Architecture

The Docker configuration allows the application and its required services to run in containers.

Conceptually:

```text
                Docker
                  |
        +---------+---------+
        |                   |
        v                   v
   FastAPI App         PostgreSQL
   Container            Container
        |
        v
     API Routes
```

The `Dockerfile` defines how the application image is built.

The `docker-compose.yml` defines how the required containers/services are configured and run together.

---

# File Responsibilities

| File                 | Responsibility                                 |
| -------------------- | ---------------------------------------------- |
| `main.py`            | FastAPI application and API routes             |
| `auth.py`            | Password hashing and JWT authentication        |
| `database.py`        | Database engine, sessions, and SQLAlchemy base |
| `models.py`          | Database table definitions                     |
| `schemas.py`         | API request validation                         |
| `Dockerfile`         | Builds the application Docker image            |
| `docker-compose.yml` | Runs and manages Docker services               |
| `.env`               | Stores configuration and secrets               |

---

# Quick Start

For someone who already has Docker installed:

```bash
git clone <YOUR_REPOSITORY_URL>  //Docker Repository yet to be uploaded ...(slow internet T_T)
cd Auth
docker compose up --build
```

Then open:

```text
http://localhost:8000/docs
```

To stop the application:

```bash
docker compose down
```

---

# Docker Hub

Docker image:

```text
bosatsu00/auth-web:latest
```

Pull:

```bash
docker pull bosatsu00/auth-web:latest
```

Run:

```bash
docker run -d \
  --name auth-web \
  -p 8000:8000 \
  bosatsu00/auth-web:latest
```

The API can then be accessed through:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```
