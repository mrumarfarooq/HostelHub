# HostelHub – System Architecture

## 1. Overview

HostelHub is a multi-tenant Hostel/PG Management SaaS.

## 2. Technology Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS
- Backend: Django, Django REST Framework
- Database: PostgreSQL

## 3. Multi-Tenant Architecture

Shared PostgreSQL database and shared schema.

Each organization represents a tenant.

Backend queries and permissions must enforce organization isolation.

## 4. Core Domain

- Organization
- Property
- Room
- Bed
- Resident
- Allocation
- Invoice
- Payment
- Complaint
- Notice

## 5. Security Requirements

- Authentication and role-based access control
- Organization-level tenant isolation
- Property-level manager permissions
- Transaction-safe bed allocation
- Financial transaction validation
- Automated security and isolation tests

## 6. Pending Design

- Detailed database schema
- Authentication strategy
- API conventions
- Audit logging scope
- Deployment architecture
