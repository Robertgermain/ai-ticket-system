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

## 🧱 System Architecture

The system is designed as a modular backend API with clear separation of concerns:

- **API Layer (FastAPI)** — Handles request routing and validation  
- **Service Layer** — Business logic for ticket processing and assignment  
- **AI Layer (OpenAI)** — Extracts structured data from ticket content  
- **Database Layer (PostgreSQL + SQLAlchemy)** — Stores users, tickets, and assignments  
- **Auth Layer (JWT)** — Secure authentication and role-based access  

Workflow:

1. Incoming request hits FastAPI endpoint  
2. Ticket data is processed by the AI service  
3. Structured metadata is generated  
4. Assignment logic selects the best technician  
5. Data is stored and returned to the client  

---

## 🌐 Live Demo

API Base URL:  
https://ai-ticket-system-n7ot.onrender.com/health

Interactive Swagger Docs:  
https://ai-ticket-system-n7ot.onrender.com/docs  

---

## ⚡ Example API Usage

### Create a Ticket

**Request**
```json
POST /tickets

{
  "title": "User cannot connect to VPN",
  "description": "Remote employee unable to access company network"
}
```

**Response**
```json
{
  "id": 2,
  "title": "Account hacked",
  "description": "My account has been hacked",
  "summary": "Account compromised",
  "status": "open",
  "priority": "high",
  "category": "security",
  "issue_type": "account_hack",
  "sub_issue_type": "account_compromise",
  "ticket_type": "incident",
  "owner_id": 1,
  "assigned_technician_id": 10,
  "created_at": "2026-04-29T17:45:02.041378Z",
  "updated_at": "2026-04-29T17:45:02.041378Z",
  "is_deleted": false
}
```

This demonstrates how the system uses AI to transform unstructured input into structured, actionable data and automatically assigns the most appropriate technician.

The `assigned_technician_id` field represents the technician selected by the system’s assignment logic.

Technician assignment is based on:
- Ticket category (e.g., network, security, application)
- Issue type and sub-issue type
- Priority level
- Technician role, skill set, and availability

If no suitable technician is found, this field will return `null`.

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

This project simulates a production-style backend system for IT ticket automation.

It demonstrates how AI can be integrated into real-world workflows to:
- Reduce manual triage effort
- Improve response time
- Optimize technician workload distribution

The system is fully deployed, containerized, and accessible via a live API, reflecting real-world backend engineering practices.
