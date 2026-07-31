# Implementation Plan: AI Learning Platform Foundation

**Branch**: `1-foundation` | **Date**: 2026-07-01 | **Spec**: `/specs/1-foundation/spec.md`
**Input**: Feature specification from `/specs/1-foundation/spec.md`

## Summary

Build the foundational infrastructure for the AI Learning Platform including a monorepo with Next.js frontend and FastAPI backend, PostgreSQL database with SQLAlchemy ORM, and Better Auth integration for user authentication and profile management.

## Technical Context

**Language/Version**: TypeScript 5.x (Next.js), Python 3.11 (FastAPI)
**Primary Dependencies**: Next.js 14, FastAPI 0.100+, PostgreSQL 15, Better Auth, SQLAlchemy 2.x, Pydantic, Tailwind CSS, shadcn/ui
**Storage**: PostgreSQL (local development: Docker container, future: managed service)
**Testing**: Jest (frontend), pytest (backend), Supertest (API)
**Target Platform**: Single project monorepo, web application
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Sub-30s setup time, <1s API response, hot-reload development
**Constraints**: Must follow Constitution (Type Safety, Security by Default, Production-First Architecture)
**Scale/Scope**: Initial user authentication and profile management foundation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| User-Controlled AI Processing | N/A | Foundation phase, no AI processing yet |
| Stable Agent Contracts | ✅ | Shared schemas ensure contract stability |
| Grounded AI Generation | N/A | No AI outputs yet |
| Incremental Processing | ✅ | Phase-based approach supports incremental work |
| Orchestrator as Single Source of Truth | ✅ | All workflow coordination through spec system |
| Production-First Architecture | ✅ | Security, logging, error handling built-in |
| Type Safety & Schema Validation | ✅ | TypeScript Strict Mode, Pydantic models |
| Observability by Default | ✅ | Structured logging for all operations |
| Security & Privacy | ✅ | Better Auth, CSRF, CORS configured |
| AI Cost Awareness | N/A | No AI usage in foundation phase |
| Modular Agent Architecture | ✅ | Clean layer separation in backend |
| Documentation as Code | ✅ | README.md, ARCHITECTURE.md required |
| Spec-Driven Development | ✅ | Following constitution-mandated workflow |
| Conventional Commits | ✅ | CI enforced via commitlint |
| Code Quality Standards | ✅ | ESLint, Prettier, Type Checking in CI |
| Testing Requirements | ✅ | Unit, integration, contract tests required |
| Design System Consistency | ✅ | shadcn/ui, Tailwind CSS, WCAG AA |
| AI-Friendly Codebase | ✅ | Predictable structure, descriptive naming |

## Project Structure

### Documentation (this feature)

```text
specs/1-foundation/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── openapi.yaml     # API contracts
└── tasks.md             # Phase 2 output
```

### Source Code (monorepo structure)

```text
app/
├── frontend/            # Next.js application
│   ├── src/
│   │   ├── app/         # App Router pages
│   │   ├── components/  # shadcn/ui components
│   │   ├── lib/         # Utilities, types
│   │   └── hooks/       # React hooks
│   ├── package.json
│   └── tsconfig.json
└── backend/             # FastAPI application
    ├── src/
    │   ├── api/         # API routers
    │   ├── core/        # Config, middleware
    │   ├── models/      # SQLAlchemy models
    │   ├── services/    # Business logic
    │   ├── schemas/     # Pydantic schemas
    │   └── main.py      # FastAPI app entry
    ├── requirements.txt
    └── pyproject.toml
```

**Structure Decision**: Monorepo with separate `app/frontend` and `app/backend` directories. This provides:
- Shared configuration (root `.eslintrc`, `tsconfig.json`)
- Independent deployment capability
- Clear separation of concerns
- Easier CI/CD pipeline configuration

## Complexity Tracking

No Constitution violations - all principles satisfied by this architecture.

## Phase 0: Research

### Research Tasks

1. **Research Better Auth integration with Next.js and FastAPI**
   - Decision: Better Auth with custom access token validation
   - Rationale: Better Auth provides comprehensive auth with FastAPI compatibility
   - Alternatives: NextAuth.js (less FastAPI friendly), custom JWT

2. **Research SQLAlchemy best practices for FastAPI**
   - Decision: SQLAlchemy 2.x with async support
   - Rationale: Mature ORM, excellent FastAPI integration, async support
   - Alternatives: SQLModel (less mature), Prisma (not recommended for FastAPI)

3. **Research shadcn/ui integration with Next.js App Router**
   - Decision: Standard shadcn/ui installation with dark mode
   - Rationale: Component library follows WCAG AA, integrates seamlessly
   - Alternatives: Tailwind UI (paid), custom component library

4. **Research PostgreSQL local development with Docker**
   - Decision: Official PostgreSQL Docker image with docker-compose
   - Rationale: Consistent environment, easy setup via quickstart
   - Alternatives: Local PostgreSQL install, SQLite for development

## Phase 1: Design

### Data Model

**User Entity**:
- `id`: UUID (primary key)
- `email`: String (unique, indexed)
- `email_verified`: Boolean
- `password_hash`: String
- `created_at`: DateTime
- `updated_at`: DateTime
- `last_login`: DateTime (optional)

### API Contracts

**Auth Endpoints**:
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user
- `PATCH /api/auth/profile` - Update profile

**Protected Endpoints** (require Bearer token):
- All `/api/auth/*` except register/login

### Architecture Layers

**Frontend (Next.js)**:
- App Router for routing
- shadcn/ui for components
- Context API for auth state
- Axios for API client

**Backend (FastAPI)**:
- API Layer: Route definitions
- Service Layer: Business logic
- Model Layer: SQLAlchemy models
- Schema Layer: Pydantic validation
- Core Layer: Configuration, middleware

### Authentication Boundary

- **Next.js owns**: UI, session cookie management, login/logout flows
- **FastAPI owns**: Token validation, user data, session verification
- **Communication**: Bearer token (access token) in Authorization header
- **Session storage**: httpOnly cookie in Next.js, server-side in database

## Phase 1 Deliverables

- [ ] research.md with all decisions documented
- [ ] data-model.md with User entity
- [ ] contracts/openapi.yaml with API specifications
- [ ] quickstart.md with setup instructions
- [ ] Constitution re-check (all gates pass)