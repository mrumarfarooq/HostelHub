# HostelHub – Hostel & PG Management SaaS

A multi-tenant Hostel and Paying Guest (PG) Management SaaS application designed to simplify property management, resident administration, room and bed allocation, rent tracking, and daily hostel operations.

**Project Status:** In Development

## Overview

HostelHub aims to provide a centralized management platform for independent PG owners and businesses operating multiple hostel properties.

The application is designed to support both small single-property PGs and growing hostel organizations through a simple, responsive, and role-based interface.

## Planned Features

- Multi-tenant organization and property management
- Role-based authentication and authorization
- Platform Admin, Hostel Owner, Hostel Manager, and Resident dashboards
- Building, floor, room, and bed management
- Resident registration and bed allocation
- Resident transfers and checkout
- Monthly rent invoices and payment tracking
- Partial payments, advance rent, and outstanding dues
- Complaint management
- Property-specific notices and announcements
- Occupancy analytics and financial reports
- Tenant isolation and essential audit logging

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| Styling | Tailwind CSS |
| Backend | Python, Django, Django REST Framework |
| Database | PostgreSQL |
| API | REST API |
| Version Control | Git and GitHub |
| Testing | Automated backend and frontend tests (planned) |

## Project Structure

```text
HostelHub/
├── backend/          # Django backend (planned)
├── frontend/         # React frontend (planned)
├── docs/             # Project documentation
├── .env.example      # Environment configuration template
├── .gitignore        # Git exclusions
└── README.md         # Project overview
```

## Architecture

HostelHub uses a planned multi-tenant architecture with a shared PostgreSQL database and organization-scoped data access.

The backend will enforce role-based permissions, property assignments, and tenant isolation.

Detailed architecture and database documentation will be added as development progresses.

## Development Roadmap

- [x] Define MVP requirements
- [x] Approve technology stack
- [x] Initialize local Git repository
- [ ] Publish initial project documentation to GitHub
- [ ] Design database schema and API architecture
- [ ] Implement authentication and organization management
- [ ] Implement property, room, and bed management
- [ ] Implement resident registration and allocation
- [ ] Implement rent and payment management
- [ ] Implement complaints and notices
- [ ] Implement dashboards and analytics
- [ ] Complete automated testing
- [ ] Deploy the application using suitable free resources

## Getting Started

Local installation instructions will be added after the Django and React applications are initialized.

## Security

The application is being designed with backend-enforced authorization, organization-level data isolation, secure environment configuration, and validation of critical operations.

Never commit credentials, API keys, or production environment files.

## License

No license has been selected yet.

---

**HostelHub is an actively developed portfolio project focused on practical full-stack engineering, maintainability, and real-world SaaS architecture.**