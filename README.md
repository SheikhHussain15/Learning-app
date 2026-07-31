# AI Learning Platform

A modern learning platform powered by AI.

## Quick Start

1. Start the database:
   ```bash
   docker-compose up -d
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development servers:
   ```bash
   npm run dev
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Project Structure

```
├── app/
│   ├── frontend/     # Next.js application
│   └── backend/      # FastAPI application
├── docker-compose.yml
└── package.json
```

## Requirements

- Node.js 18+
- Python 3.11+
- Docker (for PostgreSQL)