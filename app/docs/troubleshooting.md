# Troubleshooting Guide

## Common Issues

### Database Connection Failed

```bash
# Check PostgreSQL is running
docker compose ps postgres

# Check connection
psql -h localhost -U postgres -d ai_learning

# Verify environment variable
echo $DATABASE_URL
```

### Langfuse Not Recording Traces

```bash
# Check Langfuse is running
docker compose ps langfuse

# Check environment variables
echo $LANGFUSE_PUBLIC_KEY
echo $LANGFUSE_SECRET_KEY

# Verify Langfuse connectivity
curl -f https://cloud.langfuse.com/api/health
```

### Tests Failing

```bash
# Run with verbose output
pytest -v

# Run specific test
pytest tests/unit/test_specific.py -v

# Run with coverage
pytest --cov=src --cov-report=html

# Check test database
rm -f test.db  # Remove stale test database
pytest
```

### Frontend Build Errors

```bash
# Clear node_modules
rm -rf node_modules
npm install

# Check TypeScript
npm run typecheck

# Check ESLint
npm run lint
```

### Docker Issues

```bash
# Rebuild containers
docker compose down
docker compose up --build

# Check logs
docker compose logs backend
docker compose logs frontend

# Clean Docker cache
docker system prune -a
```

### API Validation Errors

- Check request body matches Pydantic schema
- Verify Content-Type header is `application/json`
- Check required fields are present

### Authentication Errors

- Verify JWT token is valid and not expired
- Check `Authorization: Bearer <token>` header
- Ensure CORS is configured for your origin

### Rate Limiting

- Wait for rate limit window to reset
- Check `Retry-After` header in 429 response
- Reduce request frequency

## Performance Issues

### Slow API Responses

1. Check database query performance
2. Verify ChromaDB indexing
3. Check AI provider latency in Langfuse
4. Review application logs for bottlenecks

### High Memory Usage

1. Check for memory leaks in long-running processes
2. Verify connection pool settings
3. Monitor ChromaDB memory usage

## Getting Help

- Check logs: `docker compose logs -f`
- Review health: `curl localhost:8000/api/v1/health`
- Check Langfuse dashboard for traces
- Review error messages in structured logs
