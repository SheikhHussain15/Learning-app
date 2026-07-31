# Research: AI Learning Platform Foundation

**Date**: 2026-07-01
**Phase**: Phase 0 - Research

## Research Findings

### 1. Better Auth Integration with Next.js and FastAPI

**Decision**: Better Auth with custom access token validation

**Rationale**:
- Better Auth provides comprehensive authentication with first-class Next.js support
- Custom access tokens can be validated by FastAPI via the Better Auth API
- Session management stays in Next.js (httpOnly cookies)
- FastAPI validates Bearer tokens for protected endpoints

**Alternatives Considered**:
- NextAuth.js: Less friendly FastAPI integration, requires custom server
- Custom JWT: More development time, potential security issues
- Supabase Auth: Locked into Supabase ecosystem

### 2. SQLAlchemy Best Practices for FastAPI

**Decision**: SQLAlchemy 2.x with async support

**Rationale**:
- Mature ORM with excellent FastAPI integration
- Native async support for high-performance APIs
- Strong typing with SQLAlchemy 2.x
- Flexible enough for future AI components (ChromaDB, etc.)

**Alternatives Considered**:
- SQLModel: Based on Pydantic, less mature than SQLAlchemy
- Prisma: Not recommended for FastAPI (designed for Node.js)
- Direct psycopg: More boilerplate, no ORM benefits

### 3. shadcn/ui Integration with Next.js App Router

**Decision**: Standard shadcn/ui installation with dark mode

**Rationale**:
- Component library follows WCAG AA accessibility standards
- Seamless integration with Tailwind CSS
- Zero-config dark mode support
- TypeScript support out of the box

**Alternatives Considered**:
- Tailwind UI: Paid library, less customizable
- Custom component library: More development time

### 4. PostgreSQL Local Development with Docker

**Decision**: Official PostgreSQL Docker image with docker-compose

**Rationale**:
- Consistent environment across all developers
- Easy setup via quickstart documentation
- Can mirror production configuration
- Volume persistence for development data

**Alternatives Considered**:
- Local PostgreSQL install: Version conflicts, setup complexity
- SQLite: Not production-representative

## Technical Stack Summary

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | Next.js | 14.x |
| Frontend | TypeScript | 5.x |
| Frontend | Tailwind CSS | 3.x |
| Frontend | shadcn/ui | latest |
| Backend | FastAPI | 0.100+ |
| Backend | Python | 3.11 |
| Backend | SQLAlchemy | 2.x |
| Backend | Pydantic | 2.x |
| Database | PostgreSQL | 15 |
| Auth | Better Auth | latest |
| Testing | Jest | 29.x |
| Testing | pytest | 7.x |
| Testing | Supertest | 6.x |