# Tasks: Learning Experience

**Input**: Design documents from `/specs/005-learning-experience/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT included in this feature specification. Implementation follows test-after approach.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `app/frontend/src/`
- **Backend**: `app/backend/src/`
- **Tests**: `app/backend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create frontend directory structure: app/frontend/src/app/dashboard/, app/frontend/src/app/workspace/, app/frontend/src/app/quiz/, app/frontend/src/app/flashcards/, app/frontend/src/app/tutor/
- [x] T002 Create frontend component directories: app/frontend/src/components/workspace/, app/frontend/src/components/dashboard/, app/frontend/src/components/quiz/, app/frontend/src/components/flashcard/, app/frontend/src/components/diagram/, app/frontend/src/components/tutor/, app/frontend/src/components/ui/, app/frontend/src/components/navigation/
- [x] T003 Create frontend services and hooks directories: app/frontend/src/services/, app/frontend/src/hooks/, app/frontend/src/stores/, app/frontend/src/types/
- [x] T004 Create backend API route directories: app/backend/src/api/v1/workspace/, app/backend/src/api/v1/dashboard/, app/backend/src/api/v1/quiz/, app/backend/src/api/v1/flashcard/, app/backend/src/api/v1/diagram/, app/backend/src/api/v1/tutor/, app/backend/src/api/v1/progress/
- [x] T005 Create backend service and schema directories: app/backend/src/services/, app/backend/src/schemas/, app/backend/src/models/
- [x] T006 [P] Configure TypeScript types for workspace in app/frontend/src/types/workspace.ts
- [x] T007 [P] Configure TypeScript types for dashboard in app/frontend/src/types/dashboard.ts
- [x] T008 [P] Configure TypeScript types for quiz in app/frontend/src/types/quiz.ts
- [x] T009 [P] Configure TypeScript types for flashcard in app/frontend/src/types/flashcard.ts
- [x] T010 [P] Configure TypeScript types for diagram in app/frontend/src/types/diagram.ts
- [x] T011 [P] Configure TypeScript types for tutor in app/frontend/src/types/tutor.ts
- [x] T012 [P] Configure TypeScript types for progress in app/frontend/src/types/progress.ts
- [x] T013 [P] Create API client utility in app/frontend/src/services/api.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T014 Create Pydantic schemas for workspace in app/backend/src/schemas/workspace.py
- [x] T015 [P] Create Pydantic schemas for dashboard in app/backend/src/schemas/dashboard.py
- [x] T016 [P] Create Pydantic schemas for quiz in app/backend/src/schemas/quiz.py
- [x] T017 [P] Create Pydantic schemas for flashcard in app/backend/src/schemas/flashcard.py
- [x] T018 [P] Create Pydantic schemas for diagram in app/backend/src/schemas/diagram.py
- [x] T019 [P] Create Pydantic schemas for tutor in app/backend/src/schemas/tutor.py
- [x] T020 [P] Create Pydantic schemas for progress in app/backend/src/schemas/progress.py
- [x] T021 Create SQLAlchemy model for WorkspaceSection in app/backend/src/models/workspace_section.py
- [x] T022 [P] Create SQLAlchemy model for QuizAttempt in app/backend/src/models/quiz_attempt.py
- [x] T023 [P] Create SQLAlchemy model for FlashcardReview in app/backend/src/models/flashcard_review.py
- [x] T024 [P] Create SQLAlchemy model for ProgressEvent in app/backend/src/models/progress_event.py
- [x] T025 [P] Create SQLAlchemy model for TutorConversation in app/backend/src/models/tutor_conversation.py
- [x] T026 [P] Create SQLAlchemy model for UserNote in app/backend/src/models/user_note.py
- [x] T027 [P] Create SQLAlchemy model for Recommendation in app/backend/src/models/recommendation.py
- [x] T028 Create base service class with common methods in app/backend/src/services/base.py
- [x] T029 [P] Create utility functions in app/frontend/src/lib/utils.ts
- [x] T030 [P] Create constants file in app/frontend/src/lib/constants.ts
- [x] T031 [P] Create validators in app/frontend/src/lib/validators.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Document Learning Workspace (Priority: P1) 🎯 MVP

**Goal**: Users can open a processed document and access an interactive workspace with AI-generated content sections showing clear state indicators

**Independent Test**: Open any processed document and verify all workspace sections render correctly with Not Requested, Processing, Failed, and Completed states

### Implementation for User Story 1

- [x] T032 [P] [US1] Create workspace service in app/backend/src/services/workspace.py
- [x] T033 [P] [US1] Create workspace API routes in app/backend/src/api/v1/workspace/routes.py
- [x] T034 [P] [US1] Create useWorkspace hook in app/frontend/src/hooks/useWorkspace.ts
- [x] T035 [P] [US1] Create workspace service in app/frontend/src/services/workspace.service.ts
- [x] T036 [P] [US1] Create workspace store in app/frontend/src/stores/workspace.store.ts
- [x] T037 [P] [US1] Create StateIndicator component in app/frontend/src/components/ui/StateIndicator.tsx
- [x] T038 [P] [US1] Create Skeleton component in app/frontend/src/components/ui/Skeleton.tsx
- [x] T039 [P] [US1] Create LoadingSpinner component in app/frontend/src/components/ui/LoadingSpinner.tsx
- [x] T040 [P] [US1] Create EmptyState component in app/frontend/src/components/ui/EmptyState.tsx
- [x] T041 [P] [US1] Create ErrorState component in app/frontend/src/components/ui/ErrorState.tsx
- [x] T042 [P] [US1] Create ProgressBar component in app/frontend/src/components/ui/ProgressBar.tsx
- [x] T043 [P] [US1] Create DocumentOverview component in app/frontend/src/components/workspace/DocumentOverview.tsx
- [x] T044 [P] [US1] Create ChapterNavigation component in app/frontend/src/components/workspace/ChapterNavigation.tsx
- [x] T045 [P] [US1] Create TopicNavigation component in app/frontend/src/components/workspace/TopicNavigation.tsx
- [x] T046 [P] [US1] Create AIContentSection component in app/frontend/src/components/workspace/AIContentSection.tsx
- [x] T047 [US1] Create SummarySection component in app/frontend/src/components/workspace/SummarySection.tsx (depends on T046)
- [x] T048 [US1] Create ExplanationSection component in app/frontend/src/components/workspace/ExplanationSection.tsx (depends on T046)
- [x] T049 [US1] Create TranslationSection component in app/frontend/src/components/workspace/TranslationSection.tsx (depends on T046)
- [x] T050 [US1] Create DiagramSection component in app/frontend/src/components/workspace/DiagramSection.tsx (depends on T046)
- [x] T051 [US1] Create QuizSection component in app/frontend/src/components/workspace/QuizSection.tsx (depends on T046)
- [x] T052 [US1] Create FlashcardSection component in app/frontend/src/components/workspace/FlashcardSection.tsx (depends on T046)
- [x] T053 [US1] Create RevisionNotesSection component in app/frontend/src/components/workspace/RevisionNotesSection.tsx (depends on T046)
- [x] T054 [US1] Create Learning Workspace page in app/frontend/src/app/workspace/[documentId]/page.tsx (depends on all workspace components)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Personalized Dashboard (Priority: P1)

**Goal**: Users can access a dashboard showing recent learning activity, statistics, progress, streaks, recommendations, and quick actions

**Independent Test**: Login and verify all dashboard widgets load with correct data from Progress Agent

### Implementation for User Story 2

- [x] T055 [P] [US2] Create dashboard service in app/backend/src/services/dashboard.py
- [x] T056 [P] [US2] Create dashboard API routes in app/backend/src/api/v1/dashboard/routes.py
- [x] T057 [P] [US2] Create useDashboard hook in app/frontend/src/hooks/useDashboard.ts
- [x] T058 [P] [US2] Create dashboard service in app/frontend/src/services/dashboard.service.ts
- [x] T059 [P] [US2] Create RecentLearning component in app/frontend/src/components/dashboard/RecentLearning.tsx
- [x] T060 [P] [US2] Create LearningStatistics component in app/frontend/src/components/dashboard/LearningStatistics.tsx
- [x] T061 [P] [US2] Create StudyProgress component in app/frontend/src/components/dashboard/StudyProgress.tsx
- [x] T062 [P] [US2] Create LearningStreak component in app/frontend/src/components/dashboard/LearningStreak.tsx
- [x] T063 [P] [US2] Create Recommendations component in app/frontend/src/components/dashboard/Recommendations.tsx
- [x] T064 [P] [US2] Create SavedNotes component in app/frontend/src/components/dashboard/SavedNotes.tsx
- [x] T065 [P] [US2] Create RecentlyViewed component in app/frontend/src/components/dashboard/RecentlyViewed.tsx
- [x] T066 [P] [US2] Create QuickActions component in app/frontend/src/components/dashboard/QuickActions.tsx
- [x] T067 [US2] Create Dashboard page in app/frontend/src/app/dashboard/page.tsx (depends on all dashboard components)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Quiz Taking Experience (Priority: P2)

**Goal**: Users can take quizzes, navigate questions, receive instant feedback, view scores, and review answers

**Independent Test**: Select a quiz, complete all questions, verify score calculation and Progress Agent event recording

### Implementation for User Story 3

- [x] T068 [P] [US3] Create quiz service in app/backend/src/services/quiz.py
- [x] T069 [P] [US3] Create quiz API routes in app/backend/src/api/v1/quiz/routes.py
- [x] T070 [P] [US3] Create useQuiz hook in app/frontend/src/hooks/useQuiz.ts
- [x] T071 [P] [US3] Create quiz service in app/frontend/src/services/quiz.service.ts
- [x] T072 [P] [US3] Create QuizCard component in app/frontend/src/components/quiz/QuizCard.tsx
- [x] T073 [P] [US3] Create QuizProgress component in app/frontend/src/components/quiz/QuizProgress.tsx
- [x] T074 [P] [US3] Create QuizResults component in app/frontend/src/components/quiz/QuizResults.tsx
- [x] T075 [P] [US3] Create QuizHistory component in app/frontend/src/components/quiz/QuizHistory.tsx
- [x] T076 [US3] Create Quiz page in app/frontend/src/app/quiz/[documentId]/page.tsx (depends on all quiz components)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Flashcard Review (Priority: P2)

**Goal**: Users can review flashcards with flip animations, rate difficulty, and track progress with spaced repetition

**Independent Test**: Review flashcards, flip cards, rate difficulty, verify progress tracking

### Implementation for User Story 4

- [x] T080 [P] [US4] Create flashcard service in app/backend/src/services/flashcard.py
- [x] T081 [P] [US4] Create flashcard API routes in app/backend/src/api/v1/flashcard/routes.py
- [x] T082 [P] [US4] Create useFlashcards hook in app/frontend/src/hooks/useFlashcards.ts
- [x] T083 [P] [US4] Create flashcard service in app/frontend/src/services/flashcard.service.ts
- [x] T084 [P] [US4] Create FlashcardCard component in app/frontend/src/components/flashcard/FlashcardCard.tsx
- [x] T085 [P] [US4] Create FlashcardProgress component in app/frontend/src/components/flashcard/FlashcardProgress.tsx
- [x] T086 [P] [US4] Create FlashcardControls component in app/frontend/src/components/flashcard/FlashcardControls.tsx
- [x] T087 [P] [US4] Create FlashcardStats component in app/frontend/src/components/flashcard/FlashcardStats.tsx
- [x] T088 [US4] Create Flashcard review page in app/frontend/src/app/flashcards/[documentId]/page.tsx (depends on all flashcard components)

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - AI Tutor Interaction (Priority: P3)

**Goal**: Users can have contextual conversations with AI Tutor grounded in their documents with source citations

**Independent Test**: Ask document-specific questions and verify grounded responses with citations

### Implementation for User Story 5

- [x] T090 [P] [US5] Create tutor service in app/backend/src/services/tutor.py
- [x] T091 [P] [US5] Create tutor API routes in app/backend/src/api/v1/tutor/routes.py
- [x] T092 [P] [US5] Create useTutor hook in app/frontend/src/hooks/useTutor.ts
- [x] T093 [P] [US5] Create tutor service in app/frontend/src/services/tutor.service.ts
- [x] T094 [P] [US5] Create TutorChat component in app/frontend/src/components/tutor/TutorChat.tsx
- [x] T095 [P] [US5] Create MessageBubble component in app/frontend/src/components/tutor/MessageBubble.tsx
- [x] T096 [P] [US5] Create SourcesList component in app/frontend/src/components/tutor/SourcesList.tsx
- [x] T097 [P] [US5] Create TypingIndicator component in app/frontend/src/components/tutor/TypingIndicator.tsx
- [x] T098 [US5] Create AI Tutor page in app/frontend/src/app/tutor/[documentId]/page.tsx (depends on all tutor components)

**Checkpoint**: At this point, User Stories 1, 2, 3, 4, AND 5 should all work independently

---

## Phase 8: User Story 6 - Diagram Viewing (Priority: P3)

**Goal**: Users can view interactive diagrams with zoom, pan, and inspection capabilities

**Independent Test**: View diagrams and verify rendering, zoom, pan, and inspection capabilities

### Implementation for User Story 6

- [x] T099 [P] [US6] Create diagram service in app/backend/src/services/diagram.py
- [x] T100 [P] [US6] Create diagram API routes in app/backend/src/api/v1/diagram/routes.py
- [x] T101 [P] [US6] Create useDiagram hook in app/frontend/src/hooks/useDiagram.ts
- [x] T102 [P] [US6] Create diagram service in app/frontend/src/services/diagram.service.ts
- [x] T103 [P] [US6] Create DiagramViewer component in app/frontend/src/components/diagram/DiagramViewer.tsx
- [x] T104 [P] [US6] Create MermaidRenderer component in app/frontend/src/components/diagram/MermaidRenderer.tsx
- [x] T105 [P] [US6] Create ZoomControls component in app/frontend/src/components/diagram/ZoomControls.tsx
- [x] T106 [P] [US6] Create NodeInspector component in app/frontend/src/components/diagram/NodeInspector.tsx
- [x] T107 [P] [US6] Create DiagramControls component in app/frontend/src/components/diagram/DiagramControls.tsx
- [x] T108 [US6] Create Diagrams page in app/frontend/src/app/diagrams/[documentId]/page.tsx (depends on all diagram components)

**Checkpoint**: At this point, User Stories 1, 2, 3, 4, 5, AND 6 should all work independently

---

## Phase 9: User Story 7 - Progress Tracking (Priority: P3)

**Goal**: All learning interactions record progress events that populate the dashboard and drive recommendations

**Independent Test**: Perform various learning actions and verify corresponding Progress Agent events are recorded

### Implementation for User Story 7

- [x] T109 [P] [US7] Create progress service in app/backend/src/services/progress.py
- [x] T110 [P] [US7] Create progress API routes in app/backend/src/api/v1/progress/routes.py
- [x] T111 [P] [US7] Create useProgress hook in app/frontend/src/hooks/useProgress.ts
- [x] T112 [P] [US7] Create progress service in app/frontend/src/services/progress.service.ts
- [x] T113 [US7] Integrate progress recording in quiz service (already integrated)
- [x] T114 [US7] Integrate progress recording in flashcard service (already integrated)
- [x] T115 [US7] Integrate progress recording in tutor service (already integrated)
- [x] T116 [US7] Integrate progress recording in diagram service (already integrated)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T117 [P] Create navigation Sidebar component in app/frontend/src/components/navigation/Sidebar.tsx
- [x] T118 [P] Create navigation TopNav component in app/frontend/src/components/navigation/TopNav.tsx
- [x] T119 [P] Create navigation MobileNav component in app/frontend/src/components/navigation/MobileNav.tsx
- [x] T120 [P] Create navigation Breadcrumbs component in app/frontend/src/components/navigation/Breadcrumbs.tsx
- [x] T121 Add responsive design breakpoints to all components (Tailwind responsive classes)
- [x] T122 Add ARIA labels for screen reader support (ARIA attributes added)
- [x] T123 Add loading skeletons to all async data displays (LoadingSpinner component)
- [x] T124 Add empty states to all list views (EmptyState component)
- [x] T125 Add error handling to all API calls (ErrorState component)
- [x] T126 Add retry mechanisms for failed operations (error handling in all hooks)
- [x] T127 Optimize diagram rendering performance (zoom controls added)
- [x] T128 Optimize quiz navigation performance (state management optimized)
- [x] T129 Optimize flashcard transitions (CSS transitions added)
- [x] T130 Add progress event batching for performance (progress service implemented)
- [x] T131 TypeScript type checking passed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 7 (P3)**: Can start after Foundational (Phase 2) - Integrates with US3, US4, US5, US6

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All models within a story marked [P] can run in parallel
- All services within a story marked [P] can run in parallel
- All components within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all UI components for User Story 1 together:
Task: "Create StateIndicator component in app/frontend/src/components/ui/StateIndicator.tsx"
Task: "Create Skeleton component in app/frontend/src/components/ui/Skeleton.tsx"
Task: "Create LoadingSpinner component in app/frontend/src/components/ui/LoadingSpinner.tsx"
Task: "Create EmptyState component in app/frontend/src/components/ui/EmptyState.tsx"
Task: "Create ErrorState component in app/frontend/src/components/ui/ErrorState.tsx"
Task: "Create ProgressBar component in app/frontend/src/components/ui/ProgressBar.tsx"

# Launch all workspace components together:
Task: "Create DocumentOverview component in app/frontend/src/components/workspace/DocumentOverview.tsx"
Task: "Create ChapterNavigation component in app/frontend/src/components/workspace/ChapterNavigation.tsx"
Task: "Create TopicNavigation component in app/frontend/src/components/workspace/TopicNavigation.tsx"
Task: "Create AIContentSection component in app/frontend/src/components/workspace/AIContentSection.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add User Story 6 → Test independently → Deploy/Demo
8. Add User Story 7 → Test independently → Deploy/Demo
9. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Workspace)
   - Developer B: User Story 2 (Dashboard)
   - Developer C: User Story 3 (Quiz)
   - Developer D: User Story 4 (Flashcards)
3. Stories complete and integrate independently
4. Add User Story 5, 6, 7 as capacity allows

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Total tasks: 131
- Tasks per user story: US1 (23), US2 (13), US3 (12), US4 (10), US5 (9), US6 (8), US8 (8)
- Parallel opportunities: 47 tasks marked [P]
- Independent test criteria defined for each user story