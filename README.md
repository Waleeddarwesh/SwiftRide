# 🚍 SwiftRide Application — v1.0 (Production Ready)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![DRF](https://img.shields.io/badge/DRF-Rest_Framework-red)
![Daphne](https://img.shields.io/badge/Server-Daphne_HTTP%2F2-blueviolet)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📌 Overview

**SwiftRide** is a comprehensive transport and ticket reservation platform designed to provide a seamless booking experience for passengers and robust management tools for transport suppliers.

The platform integrates several advanced systems into a unified architecture, including:

- 🎫 Ticket Booking & Lifecycle
- 💺 Real-time Seat Reservation (Concurrency-Safe)
- 💳 Secure Stripe Payment Integration
- 🔔 Real-time Notifications & Async Emails
- 📊 Supplier Financial Management
- 📈 Trip & Schedule Tracking

The project follows scalable backend architecture principles using Django and modern development technologies, optimized for high-concurrency production environments.

---

# 🆕 What's New in V1.0

| Enhancement | Details |
|---|---|
| **Production Security** | HSTS, XSS protection, CSRF hardening, and SSL redirect configured for production. |
| **ASGI Server** | Native support for WebSockets and HTTP/2 via Daphne. |
| **Database Optimization** | Persistent connection pooling for efficient traffic handling. |
| **Static Files** | Automated serving and compression via WhiteNoise. |
| **Environment Management** | Professional configuration using `python-dotenv` with development/production toggle. |
| **Cloud Ready** | Optimized for Railway deployment with pre-configured environment handling. |
| **Background Tasks** | Asynchronous email and notification processing using Celery and Redis. |

---

# 📋 Table of Contents

- [Key Features](#-key-features)
- [Technical Architecture](#-technical-architecture)
- [Prerequisites](#-prerequisites)
- [Installation Using Docker](#-installation-using-docker)
- [Manual Installation](#-manual-installation)
- [Environment Configuration](#-environment-configuration)
- [Production Deployment (Railway)](#-production-deployment-railway)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

# 🚀 Key Features

## 🎫 Ticket Reservation System
- Search trips by station and date.
- Real-time seat availability and selection.
- Ticket booking and automated cancellation handling.
- Concurrency-safe seat reservations preventing double bookings.
- Secure ticket number and QR code generation.

## 💳 Payment & Billing
- Integrated Stripe payment gateway for ticket purchases.
- Support for refunds and cancellation policies.
- Automated invoicing and payment receipts.

## 🔔 Real-time Notifications & Background Tasks
- Real-time notifications for booking confirmations and updates.
- Powered by Django Channels and WebSockets.
- Background asynchronous tasks handled by Celery & Redis.

## 👥 Supplier & Admin Management
- Multi-vendor support for transport suppliers.
- Supplier revenue tracking and financial reporting.
- Professional administrative dashboard (Jazzmin) for system-wide monitoring.

---

# 🛠 Technical Architecture

| Component | Technology |
|---|---|
| Backend Framework | Django 5.0 |
| REST API Layer | Django REST Framework |
| ASGI Server | Daphne |
| Primary Database | PostgreSQL / SQLite (Dev) |
| Cache & Message Broker | Redis |
| Background Tasks | Celery |
| Real-Time Notifications | Django Channels |
| Static File Serving | WhiteNoise |
| Containerization | Docker & Docker Compose |
| Authentication | JWT (SimpleJWT) |
| API Documentation | Swagger (drf-yasg) |

---

# ⚙️ Prerequisites

Before running the project, ensure you have:

- Python 3.11+
- PostgreSQL (for production usage)
- Redis Server (for Celery and Channels)
- Docker & Docker Compose (Recommended)
- Git

---

# 🐳 Installation Using Docker

The recommended way to run the project locally. The provided `docker-compose.yml` spins up Django (Daphne), PostgreSQL, Redis, and Celery Worker.

## 1️⃣ Clone Repository
```bash
git clone https://github.com/Waleeddarwesh/SwiftRide.git
cd SwiftRide
```

## 2️⃣ Create Environment File
Create a `.env` file in the root directory (refer to the [Environment Configuration](#-environment-configuration) section).

## 3️⃣ Build and Run Containers
```bash
docker compose up --build -d
```

---

# 🔧 Manual Installation

## 1️⃣ Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

## 2️⃣ Install Dependencies
```bash
pip install -r SwiftRide/requirements.txt
```

## 3️⃣ Environment Configuration
Create a `.env` file in the root directory. Refer to the [Environment Configuration](#-environment-configuration) section below.

## 4️⃣ Apply Database Migrations
```bash
python SwiftRide/manage.py migrate
```

## 5️⃣ Create Superuser
```bash
python SwiftRide/manage.py createsuperuser
```

## 6️⃣ Run Development Server
```bash
daphne -b 0.0.0.0 -p 8000 SwiftRide.asgi:application
```

---

# 🔐 Environment Configuration

Create a `.env` file in the project root.

```ini
# Project Config
DEBUG=True
SECRET_KEY=your_secret_key

# Database
USE_SQLITE=True  # Set to False to use PostgreSQL
DATABASE_URL=postgres://user:password@localhost:5432/swiftride_db

# Redis & Celery
CELERY_BROKER_URL=redis://localhost:6379/0
REDIS_URL=redis://localhost:6379/0

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email Service
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_HOST_USER=your_user
EMAIL_HOST_PASSWORD=your_password
```

---

# ☁️ Production Deployment (Railway)

SwiftRide is optimized for deployment on **Railway**.

*   **ASGI Native:** Handles WebSockets via Daphne out of the box.
*   **Static Assets:** Served efficiently using WhiteNoise with compression.
*   **Background Workers:** Celery worker configuration ready in the `Procfile`.
*   **Security:** Production settings include HSTS and security hardening.

**To deploy:** Connect your repo to Railway, add PostgreSQL and Redis services, and configure the variables in the dashboard.

---

# 📖 API Documentation

After running the server:

### Swagger UI
http://localhost:8000/docs/

### Redoc
http://localhost:8000/redoc/

---

# 🤝 Contributing

1️⃣ Fork the repository  
2️⃣ Create a feature branch (`git checkout -b feature/AmazingFeature`)  
3️⃣ Commit your changes (`git commit -m 'Add Amazing Feature'`)  
4️⃣ Push to the branch (`git push origin feature/AmazingFeature`)  
5️⃣ Open a Pull Request  

---

# 📞 Contact

## Waleed Darwesh
Backend Software Engineer | Django Developer | Cloud DevOps Engineer

📧 Email: [Waleeddarwesh2002@gmail.com](mailto:Waleeddarwesh2002@gmail.com)  
🔗 LinkedIn: [linkedin.com/in/waleeddarwesh1/](https://www.linkedin.com/in/waleeddarwesh1/)  
🔗 GitHub: [github.com/Waleeddarwesh](https://github.com/Waleeddarwesh)
