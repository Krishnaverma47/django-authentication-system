# Django User Authentication and Email Verification

This project is a Django-based user authentication system with email verification, JWT authentication, and Celery for asynchronous tasks.

## Features

- User registration with email verification
- User login with JWT authentication
- Password update
- Resend verification email
- Celery integration for sending emails asynchronously


## Setup

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a [.env](http://_vscodecontentref_/23) file in the root directory and add the following variables:
    ```env
    SECRET_KEY=<your-secret-key>
    DB_NAME=<your-database-name>
    DB_USER=<your-database-user>
    DB_PASSWORD=<your-database-password>
    DB_HOST=<your-database-host>
    DB_PORT=<your-database-port>
    EMAIL_HOST_USER=<your-email-host-user>
    EMAIL_HOST_PASSWORD=<your-email-host-password>
    ```

5. **Run database migrations:**
    ```sh
    python manage.py migrate
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

## Running Celery

To run Celery for asynchronous tasks, use the following command:
```sh
celery -A tcc worker --loglevel=info

7. API ENDPOINTS------

POST /api/account/registration/ - Register a new user
GET /api/account/users-list/ - Get the list of users
GET /api/account/verify-email/<token>/ - Verify user email
POST /api/account/resend-verification-email/ - Resend verification email
POST /api/account/login/ - User login
POST /api/account/get-access-token/ - Get access token using refresh token
POST /api/account/update-password/ - Update user password
