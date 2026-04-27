# AI Ticket Processing & Routing System

An AI-powered backend ticketing system that automatically classifies incoming support tickets, assigns them to the most appropriate technician based on skill and workload, and provides admin-level operational metrics.

---

## 🚀 Overview

This project simulates a real-world IT support / MSP ticketing system with intelligent automation.

When a ticket is created:
1. AI analyzes the ticket content
2. Extracts structured metadata (priority, category, issue type)
3. Routes the ticket to the best technician
4. Balances workload across technicians
5. Tracks system performance via admin metrics

---

## 🌐 Live Demo

API Base URL:  
https://ai-ticket-system-n7ot.onrender.com

Interactive Swagger Docs:  
https://ai-ticket-system-n7ot.onrender.com/docs

---

## 🧠 Key Features

### 🔹 AI Ticket Classification
- Uses OpenAI to analyze ticket title and description
- Generates:
  - Summary
  - Priority (low / medium / high)
  - Category (network, security, etc.)
  - Issue type & sub-issue type
  - Ticket type (incident, request)

---

### 🔹 Intelligent Technician Assignment
- Routes tickets based on:
  - Category → department mapping
  - Priority → skill level (junior / mid / senior)
  - Current workload (load balancing)
- Automatically assigns the best available technician

---

### 🔹 Load Balancing System
- Tracks active ticket count per technician
- Increments on assignment
- Decrements when tickets are closed
- Ensures fair distribution of work

---

### 🔹 Authentication & Security

#### JWT Authentication
- Secure login system using bearer tokens

#### Role-Based Access Control (RBAC)
- Admin-only access to sensitive endpoints

#### Secure Password Management
- Passwords hashed using bcrypt
- Password reset functionality implemented

---

### 🔹 Metrics Endpoint (Admin Only)
Provides system-level insights:
- Ticket volume
- Technician workload distribution
- System activity overview

---

## 🏗️ Tech Stack

- FastAPI
- PostgreSQL (Render)
- SQLAlchemy
- Alembic (database migrations)
- JWT Authentication
- OpenAI API
- Docker
- Render (Deployment)

---

## 🐳 Docker Support

Build and run the application using Docker:

```bash
docker build -t ai-ticket-system .
docker run --env-file .env -p 8000:8000 ai-ticket-system
```

---

## ☁️ Deployment

This application is fully containerized and deployed on Render.

Deployment includes:
- Dockerized FastAPI backend
- Managed PostgreSQL database
- Environment variable configuration
- Automated database migrations using Alembic

---

## 🛠️ Local Setup

```bash
git clone https://github.com/yourusername/ai-ticket-system.git
cd ai-ticket-system

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

---

## 🧪 How to Use (Demo Flow)

1. Register a user
2. Login to obtain JWT token
3. Authorize in `/docs`
4. Create a ticket → AI auto-classifies + assigns technician
5. View tickets
6. (Admin only) Access `/metrics`
7. Reset password via `/auth/reset-password`

---

## 📈 What This Project Demonstrates

- Production-style backend architecture
- AI-powered automation workflows
- Secure authentication & authorization
- Intelligent routing algorithms
- Load balancing logic
- RESTful API design
- Database schema management with migrations
- Containerization using Docker
- Cloud deployment (Render)

---

## 🚧 Future Improvements

- Email-based notifications (ticket updates, password reset)
- Slack / Teams integration
- Frontend dashboard (React)
- Advanced analytics & reporting
- Role-based UI

---

## 📌 Summary

This project demonstrates how AI can be integrated into backend systems to automate ticket classification, optimize workload distribution, and streamline operational workflows.

It reflects real-world backend engineering practices including API design, authentication, database management, containerization, and cloud deployment.
