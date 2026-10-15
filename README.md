# E-Commerce REST API Application

A simplified, full-stack e-commerce web application designed to demonstrate and practice RESTful API fundamentals, JWT authentication, relational database modeling, and asynchronous task processing with Celery and Redis.

## Overview

The primary objective of this project is to serve as a practical learning reference for understanding API logic:
- How frontend applications consume backend REST APIs asynchronously via standard HTTP methods (GET, POST, PATCH, DELETE).
- How authentication and authorization are handled using JSON Web Tokens (JWT).
- How database transactions protect data integrity against race conditions during checkout (atomic operations and row-level locking).
- How background tasks and job queues (Celery with Redis) are structured in a containerized environment.

## Tech Stack

| Layer | Technology | Description |
| --- | --- | --- |
| Backend | Python 3.11, Django 4.2, Django REST Framework | RESTful API endpoints, serialization, business logic |
| Database | PostgreSQL 15 | Relational data persistence |
| Cache & Message Broker | Redis | In-memory message broker and caching layer |
| Task Queue | Celery & Celery Beat | Asynchronous workers and scheduled background jobs |
| Monitoring & Admin | Flower, pgAdmin 4 | Worker inspection and database management UI |
| Authentication | SimpleJWT | Stateless JSON Web Token authentication |
| API Documentation | OpenAPI 3.0 / Swagger UI (drf-spectacular) | Interactive API exploration and schema generation |
| Frontend | Vanilla HTML5, Modern CSS, JavaScript (Fetch API) | Lightweight UI consuming REST endpoints |
| Containerization | Docker & Docker Compose | Multi-container local deployment |

## Key Features

- Product and Category Management: Hierarchical categories, product listings, search filters, and stock tracking.
- Shopping Cart and Checkout: Client-side cart persistence, stock validation, and atomic order creation.
- Order Management: Order history tracking, status transitions, and order cancellation with automatic stock restoration.
- Authentication: User registration, JWT login (access and refresh tokens), and profile management.
- Automated Test Suite: Unit and integration tests covering authentication, catalog permissions, and atomic checkout logic.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.
- Git.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. Configure environment variables:
   Copy the example environment file and adjust values if necessary:
   ```bash
   cp env-example .env
   ```

3. Build and start containers:
   ```bash
   docker compose up -d --build
   ```

4. Apply database migrations:
   ```bash
   docker compose exec backend python manage.py migrate
   ```

5. Create a superuser (optional, for admin access):
   ```bash
   docker compose exec backend python manage.py createsuperuser
   ```

## Running Automated Tests

The project includes an automated test suite verifying authentication, permissions, stock deduction, and cancellation mechanics.

Run the entire test suite using Docker:
```bash
docker compose exec backend python manage.py test
```

To run tests for a specific module:
```bash
docker compose exec backend python manage.py test apps.orders
```

## Directory Structure

```text
├── apps/
│   ├── users/        # Custom user model, JWT authentication, profile endpoints
│   ├── products/     # Category and product catalog, search, permissions
│   └── orders/       # Cart checkout, atomic transactions, stock management
├── main/             # Project settings, root routing, Celery configuration
├── templates/        # Frontend HTML templates
├── docker-compose.yml# Multi-container orchestration definition
├── Dockerfile        # Backend container build specification
└── requirements.txt  # Python package dependencies
```
