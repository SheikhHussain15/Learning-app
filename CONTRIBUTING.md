# Contributing to AI Learning Platform

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

1. Fork and clone the repository
2. Follow the [Setup Guide](app/docs/setup.md) for local development
3. Create a feature branch from `develop`

## Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Individual feature development
- `hotfix/*`: Emergency production fixes

## Pull Request Process

1. Create a feature branch from `develop`
2. Make your changes following coding standards
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation if needed
6. Submit PR to `develop` branch
7. Request review from at least 1 team member

## Code Quality

### Before Submitting

```bash
# Backend
cd app/backend
ruff check src/
ruff format src/
pytest

# Frontend
cd app/frontend
npm run lint
npm run typecheck
npm test
```

### Quality Gates

- All tests must pass
- No decrease in code coverage
- No critical security vulnerabilities
- Code review approved

## Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

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

## Testing

### Writing Tests

- Write tests for all new functionality
- Follow existing test patterns
- Use descriptive test names
- Mock external dependencies

### Test Types

- **Unit tests**: Individual components
- **Contract tests**: Schema validation
- **Integration tests**: Component interactions
- **E2E tests**: User journeys

## Documentation

- Update documentation for behavior changes
- Add code examples where helpful
- Keep documentation current

## Getting Help

- Check [Troubleshooting Guide](app/docs/troubleshooting.md)
- Review [Architecture Overview](app/docs/architecture.md)
- Ask questions in team channels
