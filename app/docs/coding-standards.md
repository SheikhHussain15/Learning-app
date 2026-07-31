# Coding Standards

## Python (Backend)

### Linting & Formatting
- **Tool**: Ruff
- **Line length**: 120 characters
- **Target**: Python 3.11+

### Rules
- Use type hints for all function signatures
- Prefer f-strings over `.format()`
- Use `snake_case` for variables, functions, and methods
- Use `PascalCase` for classes
- Use `UPPER_SNAKE_CASE` for constants
- Docstrings for all public functions (Google style)

### Imports
- Sort imports with Ruff isort
- Group: stdlib → third-party → local
- Use absolute imports from `src.`

## TypeScript (Frontend)

### Linting & Formatting
- **Lint**: ESLint with Next.js config
- **Format**: Prettier
- **TypeScript**: Strict mode

### Rules
- Use `interface` for object types (not `type`)
- Use `camelCase` for variables and functions
- Use `PascalCase` for components and types
- Prefer `const` over `let`
- No `any` types - use proper typing

### React
- Use functional components with hooks
- Use `'use client'` directive for client components
- Props interfaces should be co-located with components

## Git Commits

Follow Conventional Commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `chore:` Maintenance

### Examples
```
feat: add health check endpoint
fix: resolve agent timeout issue
docs: update setup guide
test: add contract tests for agent schemas
```

## Code Review

- All PRs require at least 1 reviewer
- Tests must pass before merge
- No decrease in code coverage
- No critical security vulnerabilities
