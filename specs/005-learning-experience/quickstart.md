# Quickstart: Learning Experience

**Feature**: 005-learning-experience  
**Date**: 2026-07-15  
**Phase**: 1 - Design & Contracts

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed
- PostgreSQL running (or SQLite for dev)
- ChromaDB running
- Phase 4 AI Agents implemented

## Setup

### Backend

```bash
# Navigate to backend
cd app/backend

# Activate virtual environment
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn src.main:app --reload --port 8000
```

### Frontend

```bash
# Navigate to frontend
cd app/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## API Endpoints

### Learning Workspace

```bash
# Get workspace overview
curl http://localhost:8000/api/v1/workspace/{documentId}

# Get section status
curl http://localhost:8000/api/v1/workspace/{documentId}/sections/{sectionType}/status

# Request AI generation
curl -X POST http://localhost:8000/api/v1/workspace/{documentId}/sections/{sectionType}/request
```

### Dashboard

```bash
# Get dashboard data
curl http://localhost:8000/api/v1/dashboard

# Get learning statistics
curl http://localhost:8000/api/v1/dashboard/statistics

# Get learning streak
curl http://localhost:8000/api/v1/dashboard/streak
```

### Quiz

```bash
# Get quiz details
curl http://localhost:8000/api/v1/quiz/{quizId}

# Start quiz attempt
curl -X POST http://localhost:8000/api/v1/quiz/{quizId}/start

# Submit answer
curl -X POST http://localhost:8000/api/v1/quiz/attempts/{attemptId}/answer \
  -H "Content-Type: application/json" \
  -d '{"question_id": "uuid", "option_id": "uuid"}'

# Complete quiz
curl -X POST http://localhost:8000/api/v1/quiz/attempts/{attemptId}/complete
```

### Flashcards

```bash
# Get flashcard deck
curl http://localhost:8000/api/v1/flashcards/{documentId}

# Get cards for review
curl http://localhost:8000/api/v1/flashcards/{documentId}/review

# Submit review
curl -X POST http://localhost:8000/api/v1/flashcards/{flashcardId}/review \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "medium", "review_duration": 15}'
```

### AI Tutor

```bash
# Create conversation
curl -X POST http://localhost:8000/api/v1/tutor/{documentId}/conversations

# Send message
curl -X POST http://localhost:8000/api/v1/tutor/conversations/{conversationId}/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "What is the main concept in chapter 2?"}'

# Get conversation history
curl http://localhost:8000/api/v1/tutor/conversations/{conversationId}/history
```

### Progress

```bash
# Record progress event
curl -X POST http://localhost:8000/api/v1/progress/events \
  -H "Content-Type: application/json" \
  -d '{"event_type": "quiz_completed", "document_id": "uuid", "event_data": {"score": 85}}'

# Get progress summary
curl http://localhost:8000/api/v1/progress/summary

# Get learning streak
curl http://localhost:8000/api/v1/progress/streak
```

## Validation

### Test Learning Workspace

1. Open a processed document in the workspace
2. Verify all sections show "Not Requested" state
3. Request summary generation
4. Verify state changes to "Processing"
5. Wait for completion
6. Verify state changes to "Completed" and content displays

### Test Dashboard

1. Login with a user that has learning history
2. Verify all dashboard widgets load
3. Check recent activity displays correctly
4. Verify learning streak shows correct value
5. Check recommendations appear

### Test Quiz

1. Select a quiz from document workspace
2. Start quiz attempt
3. Answer questions and verify feedback
4. Complete quiz and verify score
5. Review answers in review mode

### Test Flashcards

1. Access flashcard deck for a document
2. Review cards and rate difficulty
3. Verify progress updates
4. Check spaced repetition scheduling

### Test AI Tutor

1. Open AI Tutor for a document
2. Ask a document-specific question
3. Verify response includes source citations
4. Ask an out-of-scope question
5. Verify tutor refuses to answer

### Test Progress Tracking

1. Perform various learning actions
2. Check progress events are recorded
3. Verify dashboard reflects progress data
4. Check learning streak updates

## Troubleshooting

### Backend Issues

- **Database connection error**: Check PostgreSQL is running and credentials are correct
- **Agent not found**: Ensure Phase 4 agents are implemented and registered
- **ChromaDB connection error**: Verify ChromaDB service is running

### Frontend Issues

- **API errors**: Check backend server is running on port 8000
- **Missing data**: Verify user has processed documents
- **State not updating**: Check polling interval for section status

### Common Issues

- **401 Unauthorized**: Re-login to refresh JWT token
- **404 Not Found**: Verify document/section IDs are correct
- **500 Server Error**: Check backend logs for details