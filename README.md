# Ticket Management System - Backend

This is the backend for the Help & Support Ticket Management System. It provides secure RESTful APIs built with Django and Django REST Framework (DRF) to handle ticket creation, tracking, status updates, and user authentication using HttpOnly JWT cookies.

## Features
- **JWT Authentication:** Secure login using HttpOnly cookies to prevent XSS attacks.
- **Role-Based Access Control:** Differentiates between standard users (can create/view own tickets) and admins (can view all, assign, resolve, and delete tickets).
- **Filtering & Search:** Full API support for searching ticket text and filtering by status, priority, and creation date.
- **API Documentation:** Auto-generated Swagger/OpenAPI documentation.

## Prerequisites
- Python 3.9+
- PostgreSQL (or SQLite for quick local testing)

## Local Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Favasabdulnassr/Ticket-management-backend.git
   ```

2. **Navigate to the backend folder**
   ```bash
   cd Ticket-management-backend
   ```

3. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**
   Create a `.env` file in the `backend` directory (if not already present) and configure your database and network settings:
   ```ini
   SECRET_KEY=your_secure_secret_key
   DEBUG=True
   DB_NAME=ticket_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ALLOWED_HOSTS=127.0.0.1,localhost
   CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
   ```

6. **Run Database Migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create a Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```
   *Follow the prompts to set an email, username, and password. This account will automatically be granted the `ADMIN` role.*

8. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   *The API will be available at `http://localhost:8000/api/v1/`*

## API Documentation
Once the server is running, you can view the complete API documentation at:
- **Swagger UI:** `http://localhost:8000/swagger/`
- **ReDoc:** `http://localhost:8000/redoc/`
