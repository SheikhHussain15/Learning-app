# Implementation Plan: Learning Experience

**Branch**: `005-learning-experience` | **Date**: 2026-07-15 | **Spec**: specs/005-learning-experience/spec.md
**Input**: Phase 5 — Learning Experience Specification

## Summary

Build the complete user-facing learning experience layer on top of the existing AI infrastructure: Learning Workspace with 4-state AI content sections, Dashboard with Progress Agent data, Quiz/Flashcard experiences with progress tracking, Diagram Viewer with zoom/pan, AI Tutor with grounded retrieval and citations, and full design system integration — all consuming outputs from Phase 4 agents.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/Next.js 15 (frontend)  
**Primary Dependencies**: FastAPI, React 18, Tailwind CSS, SQLAlchemy 2.x, Pydantic 2, Mermaid.js  
**Storage**: PostgreSQL (progress, quiz attempts, flashcard reviews), ChromaDB (vector retrieval for AI Tutor)  
**Testing**: pytest (backend), Vitest (frontend)  
**Target Platform**: Linux server (Docker), local development (Windows/PowerShell)  
**Project Type**: Web application (FastAPI backend + Next.js frontend)  
**Performance Goals**: Dashboard <2s, Workspace <3s, AI Tutor <5s, Diagrams <2s  
**Constraints**: <100ms quiz navigation, <300ms flashcard transitions, WCAG AA compliance  
**Scale/Scope**: 50 screens, 8 functional areas, 47 requirements

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against established project principles:

1. **User-Controlled AI Processing** — Respected. Users request AI generation for sections; no automatic processing without user action. Sections show Not Requested state until explicitly triggered.
2. **Grounded AI Generation** — Respected. AI Tutor restricted to user's uploaded documents via ChromaDB retrieval. Source citations required on all tutor responses. Quiz/Flashcard/Diagram content generated from document chunks.
3. **Incremental Processing** — Respected. Each AI content section processes independently. Users can request sections in any order. Progress tracked per section.
4. **Orchestrator as Single Source of Truth** — Respected. All AI generation requests route through existing Phase 4 orchestrator. No direct agent calls from frontend.
5. **Production-First Architecture** — Respected. Comprehensive error handling for all async operations. Loading/empty/failed states for every screen. Retry mechanisms for failed generations.
6. **Security by Default** — Respected. Document ownership validation before workspace access. User isolation via owner_id scoping. No cross-user data leakage.
7. **Observability by Default** — Respected. All learning interactions recorded as progress events. Quiz attempts, flashcard reviews, tutor usage tracked.
8. **Documentation as Code** — Respected. This plan, research, data model, contracts, and quickstart are generated artifacts.
9. **Type Safety** — Respected. Pydantic schemas for all API contracts. TypeScript types for frontend. State machine for section status.
10. **AI-Friendly Codebase** — Respected. Centralized state management for workspace sections. Consistent API patterns for all AI content retrieval.

**GATE RESULT: PASS** — No violations. All constitution constraints are met.

## Project Structure

### Documentation (this feature)

```text
specs/005-learning-experience/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── workspace.json
│   ├── dashboard.json
│   ├── quiz.json
│   ├── flashcard.json
│   ├── diagram.json
│   ├── ai-tutor.json
│   ├── progress.json
│   └── recommendation.json
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
app/frontend/src/
├── app/
│   ├── dashboard/
│   │   └── page.tsx              # Dashboard page
│   ├── workspace/
│   │   └── [documentId]/
│   │       └── page.tsx          # Learning Workspace page
│   ├── quiz/
│   │   └── [quizId]/
│   │       └── page.tsx          # Quiz taking page
│   ├── flashcards/
│   │   └── [documentId]/
│   │       └── page.tsx          # Flashcard review page
│   ├── tutor/
│   │   └── [documentId]/
│   │       └── page.tsx          # AI Tutor page
│   └── layout.tsx                # Root layout with navigation
├── components/
│   ├── workspace/
│   │   ├── DocumentOverview.tsx
│   │   ├── ChapterNavigation.tsx
│   │   ├── TopicNavigation.tsx
│   │   ├── AIContentSection.tsx
│   │   ├── SummarySection.tsx
│   │   ├── ExplanationSection.tsx
│   │   ├── TranslationSection.tsx
│   │   ├── DiagramSection.tsx
│   │   ├── QuizSection.tsx
│   │   ├── FlashcardSection.tsx
│   │   └── RevisionNotesSection.tsx
│   ├── dashboard/
│   │   ├── RecentLearning.tsx
│   │   ├── LearningStatistics.tsx
│   │   ├── StudyProgress.tsx
│   │   ├── LearningStreak.tsx
│   │   ├── Recommendations.tsx
│   │   ├── SavedNotes.tsx
│   │   ├── RecentlyViewed.tsx
│   │   └── QuickActions.tsx
│   ├── quiz/
│   │   ├── QuizSelector.tsx
│   │   ├── QuestionNavigator.tsx
│   │   ├── QuestionCard.tsx
│   │   ├── AnswerFeedback.tsx
│   │   ├── ScoreDisplay.tsx
│   │   └── ReviewMode.tsx
│   ├── flashcard/
│   │   ├── FlashcardDeck.tsx
│   │   ├── Flashcard.tsx
│   │   ├── DifficultyRating.tsx
│   │   └── ReviewProgress.tsx
│   ├── diagram/
│   │   ├── DiagramViewer.tsx
│   │   ├── MermaidRenderer.tsx
│   │   ├── ZoomControls.tsx
│   │   └── DiagramInspector.tsx
│   ├── tutor/
│   │   ├── ChatInterface.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── SourceCitation.tsx
│   │   └── ConversationHistory.tsx
│   ├── ui/
│   │   ├── Skeleton.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── EmptyState.tsx
│   │   ├── ErrorState.tsx
│   │   ├── StateIndicator.tsx
│   │   └── ProgressBar.tsx
│   └── navigation/
│       ├── Sidebar.tsx
│       ├── TopNav.tsx
│       └── MobileNav.tsx
├── hooks/
│   ├── useWorkspace.ts
│   ├── useDashboard.ts
│   ├── useQuiz.ts
│   ├── useFlashcard.ts
│   ├── useDiagram.ts
│   ├── useTutor.ts
│   └── useProgress.ts
├── services/
│   ├── api.ts                    # API client
│   ├── workspace.service.ts
│   ├── dashboard.service.ts
│   ├── quiz.service.ts
│   ├── flashcard.service.ts
│   ├── diagram.service.ts
│   ├── tutor.service.ts
│   └── progress.service.ts
├── stores/
│   ├── workspace.store.ts
│   ├── quiz.store.ts
│   └── flashcard.store.ts
├── types/
│   ├── workspace.ts
│   ├── dashboard.ts
│   ├── quiz.ts
│   ├── flashcard.ts
│   ├── diagram.ts
│   ├── tutor.ts
│   └── progress.ts
└── lib/
    ├── constants.ts
    ├── utils.ts
    └── validators.ts

app/backend/src/
├── api/v1/
│   ├── workspace/
│   │   └── routes.py             # Workspace endpoints
│   ├── dashboard/
│   │   └── routes.py             # Dashboard endpoints
│   ├── quiz/
│   │   └── routes.py             # Quiz endpoints
│   ├── flashcard/
│   │   └── routes.py             # Flashcard endpoints
│   ├── diagram/
│   │   └── routes.py             # Diagram endpoints
│   ├── tutor/
│   │   └── routes.py             # AI Tutor endpoints
│   └── progress/
│       └── routes.py             # Progress endpoints
├── services/
│   ├── workspace.service.py
│   ├── dashboard.service.py
│   ├── quiz.service.py
│   ├── flashcard.service.py
│   ├── diagram.service.py
│   ├── tutor.service.py
│   └── progress.service.py
├── schemas/
│   ├── workspace.py
│   ├── dashboard.py
│   ├── quiz.py
│   ├── flashcard.py
│   ├── diagram.py
│   ├── tutor.py
│   └── progress.py
└── models/
    ├── quiz_attempt.py
    ├── flashcard_review.py
    ├── progress_event.py
    └── tutor_conversation.py

app/backend/tests/
├── integration/
│   ├── test_workspace.py
│   ├── test_dashboard.py
│   ├── test_quiz.py
│   ├── test_flashcard.py
│   ├── test_diagram.py
│   ├── test_tutor.py
│   └── test_progress.py
└── unit/
    ├── test_workspace_service.py
    ├── test_dashboard_service.py
    ├── test_quiz_service.py
    ├── test_flashcard_service.py
    ├── test_diagram_service.py
    ├── test_tutor_service.py
    └── test_progress_service.py
```

**Structure Decision**: Frontend-heavy feature with new Next.js pages and components. Backend adds service layer for business logic and API routes. All new code extends existing patterns from Phases 1-4.

## Phase 0: Research & Unknowns

Research tasks:
1. React state management patterns for 4-state AI content sections
2. Mermaid.js integration with React for diagram rendering
3. Spaced repetition algorithms (simplified) for flashcard scheduling
4. Streaming response patterns for AI Tutor chat interface
5. Dashboard widget data fetching patterns with Progress Agent
6. Quiz state management with auto-save and resume
7. WebSocket/SSE patterns for real-time section status updates
8. Accessibility patterns for complex interactive components
9. Performance optimization for diagram rendering and quiz navigation

See `research.md` for consolidated findings.

## Phase 1: Design & Contracts

### Data Model

See `data-model.md` for full entity definitions including:
- QuizAttempt (quiz completion records)
- FlashcardReview (flashcard review records)
- ProgressEvent (learning interaction records)
- TutorConversation (AI tutor conversation threads)
- WorkspaceSection (AI content section states)

### API Contracts

See `contracts/` for:
- `workspace.json` — Learning workspace endpoints
- `dashboard.json` — Dashboard data endpoints
- `quiz.json` — Quiz management endpoints
- `flashcard.json` — Flashcard review endpoints
- `diagram.json` — Diagram rendering endpoints
- `ai-tutor.json` — AI Tutor conversation endpoints
- `progress.json` — Progress event recording endpoints
- `recommendation.json` — Recommendation display endpoints

### Quickstart

See `quickstart.md` for setup and validation instructions.

### Agent Context Update

Post-design, update the agent context file with new technology and architecture decisions.

## Complexity Tracking

> No Constitution violations detected. Complexity tracking section not required.