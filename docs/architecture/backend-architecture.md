# TES Backend Architecture

**Project:** TruckerEase Solution (TES)  
**Document Version:** 0.1  
**Last Updated:** 2026-08-15  
**Status:** Draft

---

# 1. Purpose

This document defines the architectural standards, design principles, and development rules for the TES backend.

Every module, feature, service, API endpoint, and database object must follow the principles described in this document.

This architecture is intended to provide:

- Scalability
- Maintainability
- Testability
- Reusability
- Consistency
- Clear separation of responsibilities

---

# 2. High-Level Architecture

```
                Client
                   │
             REST API (FastAPI)
                   │
             API Routers
                   │
             Service Layer
                   │
          Repository Layer
                   │
        SQLAlchemy Session
                   │
          SQLAlchemy Engine
                   │
                MySQL
```

Each layer has a single responsibility.

---

# 3. Project Structure

```
app/
│
├── api/
│
├── core/
│
├── kernel/
│
├── modules/
│
└── shared/
```

---

# 4. Layer Responsibilities

## API Layer

Responsible for:

- HTTP routing
- Request validation
- Response formatting
- Authentication
- Dependency injection

The API layer must not contain business logic.

---

## Service Layer

Responsible for:

- Business rules
- Workflow orchestration
- Transaction management
- Calling repositories
- Calling external services

Business logic belongs here.

---

## Repository Layer

Responsible for:

- Database access
- CRUD operations
- Query construction

Repositories must never contain business rules.

Repositories must never call:

- commit()
- rollback()

---

## Database Layer

Responsible only for data persistence.

---

# 5. SQLAlchemy Architecture

## Engine

TES uses one SQLAlchemy Engine for the entire application.

Location:

```
app/core/database.py
```

There must never be multiple database engines.

---

## Session

One SQLAlchemy Session is created per HTTP request.

The session is injected using FastAPI dependency injection.

Repositories receive the session through dependency injection.

Repositories never create sessions.

---

## Transactions

Transactions are controlled only by the Service layer.

```
Service
    │
Repositories
    │
Database
```

Services perform:

- commit()
- rollback()

Repositories never do.

---

# 6. Module Architecture

Every business module follows the same structure.

```
module/
│
├── api/
├── models/
├── repositories/
├── schemas/
├── services/
├── policies/
└── tests/
```

Each module owns its business domain.

---

# 7. Domain Ownership

Business entities belong to the module that owns the business capability.

Example:

Identity

- Company
- User
- Role

Fleet

- Truck
- Trailer
- Maintenance

Operations

- Load
- Dispatch
- Stop

Finance

- Expense
- Settlement
- Payment

Business models must never be stored inside the kernel.

---

# 8. Kernel Responsibilities

The kernel contains reusable infrastructure only.

Examples:

- BaseModel
- Mixins
- Shared Enums
- Generic Repositories
- Utilities

The kernel must never contain business entities.

---

# 9. Mixins

Repeated model fields must be implemented using reusable mixins.

Example mixins:

- UUIDMixin
- TimestampMixin
- AuditMixin
- SoftDeleteMixin

Models compose only the mixins they require.

Example:

```
Company
    Base
    UUIDMixin
    TimestampMixin
    AuditMixin
```

Avoid duplicated fields across models.

---

# 10. Model Relationships

Each model owns its own SQLAlchemy relationships.

Relationships are defined inside the model that uses them.

There is no centralized relationships file.

Modules remain independent while referencing each other through foreign keys.

---

# 11. Database Design Principles

TES follows database normalization principles.

Avoid:

- Large tables
- Unrelated columns
- Many nullable fields

Instead:

Split data into business-focused tables.

Example:

Company

CompanyBillingSettings

CompanyNotificationSettings

CompanyAISettings

CompanyFactoringSettings

Each table represents one business responsibility.

---

# 12. Configuration Management

Sensitive configuration:

- Secrets

Stored in:

Kubernetes Secrets

Examples:

- passwords
- API keys
- database credentials

Non-sensitive configuration:

Stored in:

ConfigMaps

Examples:

- database name
- application configuration
- MySQL configuration
- feature flags

---

# 13. Kubernetes Architecture

Environment-independent resources belong in:

```
base/
```

Examples:

- StatefulSet
- Deployment
- Service

Environment-specific resources belong in:

```
overlays/
```

Examples:

- Namespace
- ConfigMap
- Secret
- Environment patches

---

# 14. Environment Strategy

Supported environments:

- Development
- QA
- Production

Each environment has its own overlay.

Example:

```
overlays/
    dev/
    qa/
    prod/
```

The base must never contain environment-specific values.

---

# 15. Git Workflow

Branch strategy:

```
main
    ▲
develop
    ▲
feature/*
```

Workflow:

Issue

↓

Feature Branch

↓

Development

↓

Pull Request

↓

Code Review

↓

Merge into develop

↓

Delete feature branch

Every feature branch should represent a single logical feature.

---

# 16. Pull Request Standards

Every Pull Request should include:

- Summary
- Related Issue
- Changes Made
- Testing Performed
- Checklist

Draft Pull Requests are encouraged for work in progress.

---

# 17. Coding Principles

Prefer:

- Composition over duplication
- Reusable infrastructure
- Dependency Injection
- Small focused classes
- Clear naming
- Modular design

Avoid:

- Business logic inside API routers
- Multiple database engines
- Repository-managed transactions
- Giant database tables
- Duplicate code

---

# 18. Testing Strategy

Testing levels:

- Unit Tests
- Integration Tests
- End-to-End Tests

Services should be tested independently of HTTP whenever possible.

---

# 19. Logging

Application logging should be centralized.

Every service should log:

- Errors
- Warnings
- Important business events

Sensitive information must never be logged.

---

# 20. Future Architecture

Planned future additions include:

- Redis
- Celery or asynchronous workers
- Event-driven architecture
- Message queues
- AWS deployment
- Observability
- Metrics
- Distributed tracing

These additions must follow the architectural principles defined in this document.

---

# 21. Architecture Principles

The TES backend follows these core principles:

1. One SQLAlchemy Engine for the application.
2. One SQLAlchemy Session per request.
3. Services own transactions.
4. Business logic belongs in Services.
5. Repositories only access data.
6. Business models belong to their modules.
7. Kernel contains reusable infrastructure only.
8. Shared behavior is implemented through Mixins.
9. Database follows normalization principles.
10. Environment-specific configuration belongs in Kubernetes overlays.
11. Infrastructure is reusable through Kustomize.
12. Every feature is developed using the Git feature branch workflow.

These principles are mandatory for all current and future development.

---

# Document Ownership

Project: TruckerEase Solution (TES)

Architecture Owner:
TES Development Team

Status:
Draft

This document should be updated whenever a significant architectural decision is made.