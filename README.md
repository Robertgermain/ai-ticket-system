# AI Ticket Processing & Routing System

An AI-powered backend ticketing system that automatically classifies incoming support tickets, assigns them to the most appropriate technician based on skill and workload, and provides admin-level operational metrics.

---

## 🚀 Overview

This project simulates a real-world IT support / MSP ticketing system with intelligent automation.

When a ticket is created:
1. The system uses AI to analyze the ticket content
2. Extracts structured metadata (priority, category, issue type)
3. Assigns the ticket to the best available technician
4. Tracks workload distribution across technicians
5. Provides admin-only metrics for system insights

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

### 🔹 Intelligent Technician Assignment
- Routes tickets based on:
  - Category (department matching)
  - Priority → skill level mapping
  - Current workload (load balancing)
- Automatically assigns the best available technician

### 🔹 Load Balancing System
- Tracks active ticket count per technician
- Increments on assignment
- Decrements when tickets are closed

### 🔹 JWT Authentication
- Secure login system
- Token-based authentication

### 🔹 Role-Based Access Control (RBAC)
- Admin-only access to sensitive endpoints like /metrics

### 🔹 Metrics Endpoint (Admin Only)
Provides:
- Ticket volume
- Technician workload
- System activity overview

---

## 🏗️ Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- OpenAI API
- Alembic

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

## 📌 Summary

This project demonstrates:
- Backend system design
- AI integration
- Authentication & RBAC
- Intelligent routing & load balancing
