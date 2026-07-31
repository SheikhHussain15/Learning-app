# Research: Learning Experience

**Feature**: 005-learning-experience  
**Date**: 2026-07-15  
**Phase**: 0 - Research & Unknowns

## Research Tasks

### 1. React State Management for 4-State AI Content Sections

**Decision**: Use React useState/useReducer with custom hooks for section state management

**Rationale**: 
- Each AI content section has 4 states: Not Requested, Processing, Failed, Completed
- State transitions are simple and don't require complex state management libraries
- Custom hooks (useWorkspace, useQuiz, etc.) encapsulate state logic per feature
- Local component state sufficient for UI state, server state managed via API calls

**Alternatives Considered**:
- Redux/Zustand: Overkill for this use case, adds unnecessary complexity
- React Query/TanStack Query: Good for server state but adds dependency; custom hooks sufficient
- Context API: Too granular for per-section state; custom hooks cleaner

### 2. Mermaid.js Integration with React

**Decision**: Use mermaid library directly with useEffect for rendering

**Rationale**:
- mermaid library provides `mermaid.render()` for SVG output
- useEffect hook triggers re-render when diagram data changes
- SVG output enables zoom/pan via CSS transforms
- No React wrapper needed; direct library usage simpler

**Alternatives Considered**:
- react-mermaid: Wrapper adds dependency, limited customization
- @mermaid-js/mermaid-react: Official wrapper but less control
- D3.js: Overkill for Mermaid diagram rendering

### 3. Spaced Repetition for Flashcards

**Decision**: Implement simplified SM-2 algorithm with 3 difficulty levels

**Rationale**:
- SM-2 is proven and simple to implement
- 3 levels (Easy, Medium, Hard) map to difficulty ratings
- Next review calculated based on performance: Easy = 2x interval, Medium = 1x, Hard = 0.5x
- Initial interval set to 1 day, grows with successful reviews

**Alternatives Considered**:
- Full SM-2: More complex, requires more parameters
- Leitner system: Box-based, less flexible
- Anki algorithm: Proprietary, complex

### 4. Streaming for AI Tutor Chat

**Decision**: Use Server-Sent Events (SSE) for streaming responses

**Rationale**:
- SSE simpler than WebSocket for unidirectional streaming
- Native browser support via EventSource API
- FastAPI supports SSE via StreamingResponse
- Enables real-time response display without polling

**Alternatives Considered**:
- WebSocket: Bidirectional but overkill for chat streaming
- Polling: High latency, inefficient
- GraphQL subscriptions: Adds complexity

### 5. Dashboard Data Fetching

**Decision**: Server-side rendering with API routes for dashboard data

**Rationale**:
- Dashboard data comes from Progress Agent records
- Server-side fetching ensures data freshness
- API routes handle Progress Agent communication
- Client-side updates for real-time changes via polling

**Alternatives Considered**:
- Client-side fetching: Simpler but data may be stale
- Static generation: Not suitable for dynamic user data
- ISR: Not applicable for personalized data

### 6. Quiz State Management

**Decision**: Local state with auto-save to server

**Rationale**:
- Quiz state is session-specific, doesn't need global management
- Auto-save prevents progress loss on page refresh
- Server stores incomplete attempts for resume
- Final submission records QuizAttempt in Progress Agent

**Alternatives Considered**:
- Global state: Unnecessary for session-specific data
- Local storage only: Risk of data loss
- No persistence: User loses progress on refresh

### 7. Real-time Section Status Updates

**Decision**: Polling with 2-second interval for processing sections

**Rationale**:
- Simple implementation, no WebSocket infrastructure needed
- 2-second interval provides near-real-time feedback
- Polling stops when section reaches terminal state (Completed/Failed)
- Can be upgraded to WebSocket later if needed

**Alternatives Considered**:
- WebSocket: More complex, requires infrastructure changes
- Long polling: More complex than simple polling
- Server push: Requires SSE/WebSocket infrastructure

### 8. Accessibility for Interactive Components

**Decision**: Follow WCAG AA with keyboard navigation and ARIA labels

**Rationale**:
- WCAG AA is industry standard
- Keyboard navigation for all interactive elements
- ARIA labels for screen reader support
- Focus management for modal-like components (quiz, flashcards)

**Alternatives Considered**:
- WCAG AAA: Higher standard but more complex
- Minimal accessibility: Legal and ethical risks
- Screen reader only: Insufficient for keyboard users

### 9. Performance Optimization

**Decision**: Lazy loading for diagrams, virtual scrolling for long lists

**Rationale**:
- Diagrams loaded on-demand to reduce initial bundle size
- Virtual scrolling for chapter/topic navigation with many items
- Code splitting per feature (quiz, flashcards, tutor)
- Image/asset optimization for diagram SVGs

**Alternatives Considered**:
- Eager loading: Slower initial load
- Infinite scroll: More complex than virtual scrolling
- No optimization: Poor performance with large documents

## Summary

All research tasks resolved. Key decisions:
- Custom hooks for state management (no external state library)
- Direct mermaid.js usage for diagram rendering
- Simplified SM-2 for flashcard scheduling
- SSE for AI Tutor streaming
- Server-side rendering for dashboard
- Polling for real-time updates
- WCAG AA compliance
- Lazy loading and code splitting for performance