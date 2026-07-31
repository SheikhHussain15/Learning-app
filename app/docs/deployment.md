# Deployment Guide

## Environments

| Environment | Purpose | Data | Access |
|-------------|---------|------|--------|
| Development | Local development | Mock data | Developers |
| Staging | Pre-production validation | Anonymized data | QA, Tech Leads |
| Production | Live user-facing | Real data | End users |

## Deployment Process

### Staging (Automatic)

1. Code merged to `main` branch
2. CI pipeline runs (lint, test, build)
3. Database migrations applied
4. Backend deployed to staging
5. Frontend deployed to staging CDN
6. Health checks verified
7. Smoke tests run

### Production (Manual Approval)

1. Staging deployment successful
2. Manual approval in GitHub UI
3. Database migrations applied (backward-compatible)
4. Blue-green deployment
5. Health checks verified
6. Traffic gradually shifted to new version
7. Old version removed after stability period

## Zero-Downtime Deployment

1. **Pre-deployment**: Run backward-compatible migrations
2. **Deployment**: Deploy new version alongside old
3. **Traffic Switch**: Gradual canary deployment
4. **Post-deployment**: Health checks and smoke tests
5. **Cleanup**: Remove old version

## Rollback

### Automatic Rollback
- Triggered by error rate >10% or health check failure
- Previous version restored within 5 minutes

### Manual Rollback
```bash
# Via API
curl -X POST https://api.example.com/api/v1/deploy/rollback \
  -H "Content-Type: application/json" \
  -d '{"reason": "Performance degradation"}'
```

## Secrets Management

| Secret | Storage | Rotation |
|--------|---------|----------|
| AI Provider Keys | Environment variables | Quarterly |
| Database Credentials | Environment variables | Quarterly |
| JWT Secrets | Environment variables | Monthly |
| Langfuse Keys | Environment variables | Quarterly |

## Health Checks

```bash
# System health
curl http://localhost:8000/api/v1/health

# Component-specific
curl http://localhost:8000/api/v1/health/database
curl http://localhost:8000/api/v1/health/chromadb
```

## Monitoring

- **Langfuse**: AI traces, costs, latency
- **Health endpoints**: System component status
- **Alerting**: Error rate and latency thresholds
