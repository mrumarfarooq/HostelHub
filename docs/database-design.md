# HostelHub – Database Design

## 1. Overview

HostelHub uses PostgreSQL with a shared-database,
shared-schema multi-tenant architecture.

## 2. Organization and Authentication

- User
- Organization
- OrganizationMembership
- ManagerPropertyAssignment

## 3. Property Management

- Property
- Room
- Bed

Building and floor information is optional.

## 4. Resident Management

- Resident
- BedAllocation

Resident login accounts are optional.

## 5. Rent and Payments

- Invoice
- Payment
- PaymentAllocation

## 6. Daily Operations

- Complaint
- Notice

## 7. Critical Database Rules

- Organization data must remain isolated.
- Managers can access only assigned properties.
- One resident can have at most one active bed allocation
  within an organization.
- One bed can have at most one active allocation.
- Allocation history must be preserved.
- Financial amounts must use precise decimal values.
- Payment history must be preserved.

## 8. Pending Design

- Primary and foreign keys
- Detailed columns and data types
- Unique and check constraints
- ER diagram
- Indexes
- Financial transaction rules

## 9. Organization and Property Schema

### User

- id: UUID, primary key
- email: unique, required
- password: securely hashed by Django
- is_active: boolean
- is_email_verified: boolean
- created_at: timestamp

### Organization

- id: UUID, primary key
- name: string, required
- slug: unique string
- is_active: boolean
- created_at: timestamp

### OrganizationMembership

- id: UUID, primary key
- user_id: foreign key to User
- organization_id: foreign key to Organization
- role: OWNER or MANAGER
- is_active: boolean

Constraint:
- Unique combination of user_id and organization_id.

### Property

- id: UUID, primary key
- organization_id: foreign key to Organization
- name: string, required
- address: text
- is_active: boolean
- created_at: timestamp

### ManagerPropertyAssignment

- id: UUID, primary key
- membership_id: foreign key to OrganizationMembership
- property_id: foreign key to Property

Constraints:
- Membership must have MANAGER role.
- Membership and Property must belong to the same organization.
- Unique combination of membership_id and property_id.

## 10. Room, Bed and Resident Schema

### Room

- id: UUID, primary key
- property_id: foreign key to Property
- room_number: string, required
- floor_label: optional string
- is_active: boolean

Constraint:
- Unique combination of property_id and room_number.

### Bed

- id: UUID, primary key
- room_id: foreign key to Room
- bed_number: string, required
- is_active: boolean

Constraint:
- Unique combination of room_id and bed_number.

### Resident

- id: UUID, primary key
- organization_id: foreign key to Organization
- user_id: optional foreign key to User
- full_name: string, required
- phone: string
- created_at: timestamp

Rules:
- Resident registration does not require a login account.
- Resident portal access may be activated later.
- Resident data must remain organization-scoped.

### BedAllocation

- id: UUID, primary key
- resident_id: foreign key to Resident
- bed_id: foreign key to Bed
- start_date: date
- end_date: optional date
- status: ACTIVE or ENDED

Constraints:
- One active allocation per bed.
- One active allocation per resident.
- Resident and bed must belong to the same organization.
- End date cannot be earlier than start date.

Operations:
- Allocation must use a database transaction.
- Transfers must end the previous allocation and create a new one.
- Checkout must end the active allocation.
- Historical allocations must not be deleted.

## 11. Rent, Invoice and Payment Schema

### RentAgreement (Proposed)

- id: UUID, primary key
- resident_id: foreign key to Resident
- property_id: foreign key to Property
- monthly_rent: decimal(12, 2), required
- billing_mode: ADVANCE or POSTPAID
- effective_from: date
- effective_to: optional date

Rules:
- Rent terms must belong to the resident's organization.
- Historical rent terms must be preserved.
- Overlapping active agreements must be prevented.

### Invoice

- id: UUID, primary key
- organization_id: foreign key to Organization
- resident_id: foreign key to Resident
- property_id: foreign key to Property
- billing_month: date
- due_date: date
- base_rent: decimal(12, 2)
- extra_charges: decimal(12, 2)
- discount: decimal(12, 2)
- total_amount: decimal(12, 2)
- status: DRAFT, ISSUED, VOID
- created_at: timestamp

Constraints:
- Monetary amounts cannot be negative.
- Total amount = base rent + extra charges - discount.
- Discount cannot exceed base rent plus extra charges.
- Prevent duplicate regular monthly invoices for the same
  resident and billing month within an organization.
- Invoice resident and property must belong to its organization.

### Payment

- id: UUID, primary key
- organization_id: foreign key to Organization
- resident_id: foreign key to Resident
- amount: decimal(12, 2)
- payment_method: CASH, UPI, BANK_TRANSFER, OTHER
- reference_number: optional string
- received_at: timestamp
- recorded_by: foreign key to User
- created_at: timestamp

Rules:
- Payment amount must be greater than zero.
- Payments are recorded manually in the MVP.
- Unapplied payment amounts represent available credit.
- Payment history must be preserved.

### PaymentAllocation

- id: UUID, primary key
- payment_id: foreign key to Payment
- invoice_id: foreign key to Invoice
- amount: decimal(12, 2)
- created_at: timestamp

Constraints:
- Allocation amount must be greater than zero.
- Payment and invoice must belong to the same organization.
- Payment and invoice must belong to the same resident.
- Total allocated amount cannot exceed payment amount.
- Total applied payments cannot exceed invoice total.
- Concurrent allocation operations must be transaction-safe.

### Financial Calculations

Invoice total:
base_rent + extra_charges - discount

Invoice outstanding:
invoice total - applied payments

Payment available credit:
payment amount - total payment allocations

### Financial Integrity

- Use Decimal values, never floating-point arithmetic.
- Use database transactions for payment allocation.
- Lock affected financial records during concurrent updates.
- Preserve financial history.
- Define audited reversal/correction operations before implementation.
