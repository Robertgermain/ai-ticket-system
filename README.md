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
- Authenticated password change endpoint

---

### 🔹 Metrics Endpoint (Admin Only)
Provides system-level insights:
- Ticket volume
- Technician workload distribution
- System activity overview

---

## 🏗️ Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migrations)
- JWT Authentication
- OpenAI API

---

## 🛠️ Setup

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
7. Change password via `/auth/change-password`

---

## 📈 What This Project Demonstrates

- Backend system design
- AI-powered automation workflows
- Secure authentication & authorization
- Intelligent routing algorithms
- Load balancing logic
- Real-world API architecture

---

## 🚧 Future Improvements

- Email-based password reset flow
- Notification system (email / Slack)
- Frontend dashboard (React)
- Advanced analytics & reporting

---

## 📌 Summary

This project is a production-style backend system showcasing how AI can be integrated into operational workflows to automate decision-making, improve efficiency, and reduce manual effort.
