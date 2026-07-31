# Quickstart: AI Learning Platform Foundation

**Date**: 2026-07-04
**Estimated Setup Time**: Under 10 minutes

## Prerequisites

Ensure you have the following installed:

- **Node.js**: Version 18.x or higher
- **Python**: Version 3.11 or higher
- **Docker**: Latest version (for PostgreSQL)
- **npm** or **yarn**: Package manager

## Step 1: Clone and Navigate

```bash
git clone <repository-url>
cd learning-app
git checkout 1-foundation
```

## Step 2: Start Database

```bash
docker-compose up -d
```

This starts PostgreSQL on port 5432 with:
- Database: `ai_learning`
- User: `postgres`
- Password: `password`

## Step 3: Setup Backend

```bash
cd app/backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Initialize the database:
```bash
python -c "from src.main import Base, engine; Base.metadata.create_all(engine)"
```

Start the backend:
```bash
uvicorn src.main:app --reload
```

API available at: http://localhost:8000
Docs available at: http://localhost:8000/docs

## Step 4: Setup Frontend

```bash
cd app/frontend
npm install  # or yarn install
```

Create `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=<generate-a-secret>
```

Start the frontend:
```bash
npm run dev  # or yarn dev
```

Application available at: http://localhost:3000

## Step 5: Verify Setup

1. Open http://localhost:3000
2. Navigate to Registration page
3. Register a new account
4. Login and verify profile access

## Development Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start frontend dev server |
| `uvicorn src.main:app --reload` | Start backend with hot reload |
| `docker-compose up -d` | Start database container |
| `docker-compose down` | Stop database container |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login user |
| GET | `/health` | Health check |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Change port in `app/backend/uvicorn` config |
| Database connection failed | Wait for container to start, check credentials |
| Frontend blank page | Check browser console for errors |