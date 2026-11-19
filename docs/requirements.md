# HostelHub – Project Requirements (MVP v1.0)

**Status:** Initial approved requirements baseline  
**Product:** Multi-tenant Hostel/PG Management SaaS  
**Development approach:** Quality-first, scope-controlled, free-resource development

## 1. Project Objective

Build a secure, responsive and maintainable SaaS platform that enables independent hostel and PG businesses to manage properties, rooms, beds, residents, allocations, rent, payments and daily operations.

The system must work efficiently for both a small PG owner with one property and an organization managing multiple hostel properties.

## 2. User Roles

- **Platform Admin:** Manage platform organizations and suspension controls.
- **Hostel Owner:** Manage their organization, properties, managers, residents and finances.
- **Hostel Manager:** Manage only properties explicitly assigned by their owner.
- **Resident:** Access their own accommodation, invoices, payment history, complaints and notices when portal access is activated.

## 3. Approved Business Rules

**BR-001 – Multi-property support:** One organization may manage multiple properties.

**BR-002 – Manager access:** A manager may be assigned to multiple properties within an authorized organization and may access only those assigned properties.

**BR-003 – Bed allocation:** A resident may have at most one active bed allocation within an organization. Allocation, transfer and checkout history must be preserved.

**BR-004 – Rent management:** Support monthly invoices, due dates, partial payments, outstanding dues, discounts, additional charges and advance rent. Cash, UPI, bank transfers and other applicable payment methods may be recorded manually with relevant references. Actual payment gateway processing is outside the initial MVP.

**BR-005 – Complaints:** Residents can submit complaints and authorized staff can update their status. Advanced assignment and maintenance workflows are excluded from the MVP.

**BR-006 – Notices:** Authorized users can publish property-specific notices with priority, expiry and preserved history.

**BR-007 – Owner onboarding:** Self-service owner registration with secure verification, organization creation and Platform Admin suspension controls.

**BR-008 – Account creation:** Managers use owner-controlled invitations. Resident records may exist without login accounts; verified resident portal activation is optional.

**BR-009 – Property structure:** Support optional building/floor details, mandatory rooms/beds, customizable sharing and bed availability.

**BR-010 – Resident lifecycle:** Support bed transfers, checkout, bed release and preserved history. Security deposit deductions and refund settlement workflows are outside the MVP.

**BR-011 – Dashboards:** Provide four role-specific dashboards with real database-driven KPIs, occupancy and rent analytics, appropriate filters and basic reports.

## 4. Usability Requirements

- Small PG owners must be able to use the platform without creating managers or unnecessary building/floor records.
- Onboarding must guide owners through organization, property, rooms/beds and first resident setup.
- Interfaces must be simple, clean, responsive and role-specific.
- Previously approved UI/UX designs and visual decisions must be preserved.

## 5. Security & Reliability Requirements

- Enforce authentication and role-based authorization on the backend.
- Enforce organization isolation and property-level manager permissions.
- Prevent double bed allocation using transactional database operations and appropriate constraints.
- Validate financial transactions and preserve payment history.
- Record essential security-sensitive and financial changes; finalize the general audit logging scope during architecture review.
- Use secure password handling, environment-based secrets and input validation.
- Write automated tests for critical business rules and tenant isolation.

## 6. MVP Exclusions

- Public hostel search and booking
- SaaS subscription billing
- Integrated payment gateway processing
- Automated WhatsApp/SMS messaging
- Advanced maintenance assignment workflows
- Complex security deposit settlement
- AI chatbot and unnecessary microservices

## 7. Development & Deployment Constraints

- Use free and open-source development tools wherever possible.
- Avoid mandatory paid APIs, hosting, domains or subscriptions.
- Verify actual free-tier limitations before selecting deployment providers.
- Use Git/GitHub from the beginning with meaningful commits, documentation and appropriate feature branches.
- Implement and verify features incrementally.

## 8. Pending Architecture Decisions

- Final frontend and backend framework selection
- Database and tenant isolation implementation
- Authentication/session strategy
- ER diagram and database constraints
- API conventions
- Exact audit log scope
- Deployment providers and free-tier limitations
- Final verification of previously approved dashboard/page designs
