# Data Model: Learning Experience

**Feature**: 005-learning-experience  
**Date**: 2026-07-15  
**Phase**: 1 - Design & Contracts

## Entities

### WorkspaceSection

Represents the state of an AI-generated content section within a document workspace.

**Fields**:
- `id`: Unique identifier (UUID)
- `document_id`: Reference to processed document
- `section_type`: Enum (summary, explanation, translation, diagram, quiz, flashcard, revision_notes)
- `status`: Enum (not_requested, processing, failed, completed)
- `content`: Generated content (JSON for structured data, text for summaries)
- `error_message`: Error details if status is failed
- `requested_at`: Timestamp when generation was requested
- `completed_at`: Timestamp when generation completed
- `created_at`: Record creation timestamp
- `updated_at`: Record last update timestamp

**Relationships**:
- Belongs to Document (via document_id)
- Has many Quiz (if section_type = quiz)
- Has many Flashcard (if section_type = flashcard)
- Has many Diagram (if section_type = diagram)

**State Transitions**:
```
not_requested → processing (on user request)
processing → completed (on success)
processing → failed (on error)
failed → processing (on retry)
```

### QuizAttempt

Records a user's quiz completion with score and answers.

**Fields**:
- `id`: Unique identifier (UUID)
- `quiz_id`: Reference to quiz section
- `user_id`: Reference to user
- `score`: Final score (0-100)
- `total_questions`: Number of questions in quiz
- `correct_answers`: Number of correct answers
- `answers`: JSON array of user answers
- `time_spent`: Duration in seconds
- `status`: Enum (in_progress, completed, abandoned)
- `started_at`: Timestamp when quiz started
- `completed_at`: Timestamp when quiz completed
- `created_at`: Record creation timestamp

**Relationships**:
- Belongs to WorkspaceSection (quiz type)
- Belongs to User
- Has many ProgressEvent (on completion)

### FlashcardReview

Records a user's flashcard review session with performance ratings.

**Fields**:
- `id`: Unique identifier (UUID)
- `flashcard_id`: Reference to flashcard
- `user_id`: Reference to user
- `difficulty_rating`: Enum (easy, medium, hard)
- `review_duration`: Time spent on card in seconds
- `reviewed_at`: Timestamp when reviewed
- `next_review_at`: Calculated next review timestamp
- `review_count`: Number of times reviewed
- `created_at`: Record creation timestamp

**Relationships**:
- Belongs to WorkspaceSection (flashcard type)
- Belongs to User
- Has many ProgressEvent (on review)

**Spaced Repetition Logic**:
```python
def calculate_next_review(review_count: int, difficulty: str) -> datetime:
    base_interval = 1  # days
    multiplier = {"easy": 2, "medium": 1, "hard": 0.5}[difficulty]
    interval = base_interval * (multiplier ** review_count)
    return datetime.now() + timedelta(days=interval)
```

### ProgressEvent

Records any learning interaction for analytics and dashboard.

**Fields**:
- `id`: Unique identifier (UUID)
- `user_id`: Reference to user
- `event_type`: Enum (quiz_completed, flashcard_reviewed, chapter_completed, reading_progress, tutor_used, diagram_interacted, revision_completed)
- `document_id`: Reference to document
- `section_id`: Reference to workspace section (optional)
- `event_data`: JSON payload with event-specific data
- `duration`: Time spent in seconds (optional)
- `created_at`: Record creation timestamp

**Relationships**:
- Belongs to User
- Belongs to Document (optional)
- Belongs to WorkspaceSection (optional)

**Event Data Examples**:
```json
// Quiz completion
{
  "quiz_id": "uuid",
  "score": 85,
  "total_questions": 10,
  "correct_answers": 8
}

// Flashcard review
{
  "flashcard_id": "uuid",
  "difficulty": "medium",
  "review_duration": 15
}

// Chapter completion
{
  "chapter_id": "uuid",
  "chapter_title": "Introduction"
}
```

### TutorConversation

Stores AI Tutor conversation history per document.

**Fields**:
- `id`: Unique identifier (UUID)
- `document_id`: Reference to document
- `user_id`: Reference to user
- `messages`: JSON array of conversation messages
- `created_at`: Record creation timestamp
- `updated_at`: Record last update timestamp

**Relationships**:
- Belongs to Document
- Belongs to User
- Has many ProgressEvent (on usage)

**Message Structure**:
```json
{
  "role": "user" | "assistant",
  "content": "Message text",
  "sources": ["chunk_id_1", "chunk_id_2"],  // for assistant messages
  "timestamp": "2026-07-15T10:00:00Z"
}
```

### UserNote

Personal annotations or summaries created by users.

**Fields**:
- `id`: Unique identifier (UUID)
- `user_id`: Reference to user
- `document_id`: Reference to document
- `section_id`: Reference to workspace section (optional)
- `title`: Note title
- `content`: Note content (markdown)
- `created_at`: Record creation timestamp
- `updated_at`: Record last update timestamp

**Relationships**:
- Belongs to User
- Belongs to Document
- Belongs to WorkspaceSection (optional)

### Recommendation

Personalized learning suggestions based on progress data.

**Fields**:
- `id`: Unique identifier (UUID)
- `user_id`: Reference to user
- `recommendation_type`: Enum (document, quiz, flashcard, review)
- `document_id`: Reference to document (optional)
- `section_id`: Reference to workspace section (optional)
- `reason`: Explanation of why recommended
- `priority`: Integer (1-10, higher = more relevant)
- `created_at`: Record creation timestamp

**Relationships**:
- Belongs to User
- Belongs to Document (optional)
- Belongs to WorkspaceSection (optional)

## Relationships Diagram

```
User
├── has many QuizAttempt
├── has many FlashcardReview
├── has many ProgressEvent
├── has many TutorConversation
├── has many UserNote
└── has many Recommendation

Document
├── has many WorkspaceSection
├── has many QuizAttempt (via WorkspaceSection)
├── has many FlashcardReview (via WorkspaceSection)
├── has many ProgressEvent
├── has many TutorConversation
└── has many UserNote

WorkspaceSection
├── belongs to Document
├── has many Quiz (if quiz type)
├── has many Flashcard (if flashcard type)
├── has many Diagram (if diagram type)
└── has many ProgressEvent

QuizAttempt
├── belongs to WorkspaceSection (quiz)
├── belongs to User
└── has many ProgressEvent

FlashcardReview
├── belongs to WorkspaceSection (flashcard)
├── belongs to User
└── has many ProgressEvent
```

## Validation Rules

### WorkspaceSection
- `section_type` must be valid enum value
- `status` must follow state transition rules
- `content` required when status = completed
- `error_message` required when status = failed

### QuizAttempt
- `score` must be between 0 and 100
- `correct_answers` must be <= total_questions
- `answers` must match quiz question count
- `completed_at` required when status = completed

### FlashcardReview
- `difficulty_rating` must be valid enum value
- `review_duration` must be positive
- `next_review_at` must be in future

### ProgressEvent
- `event_type` must be valid enum value
- `event_data` structure must match event_type
- `document_id` required for most event types

### TutorConversation
- `messages` must alternate user/assistant roles
- `sources` required for assistant messages
- `content` must not be empty

## Indexes

- WorkspaceSection: (document_id, section_type), (status)
- QuizAttempt: (user_id, quiz_id), (completed_at)
- FlashcardReview: (user_id, flashcard_id), (next_review_at)
- ProgressEvent: (user_id, created_at), (event_type), (document_id)
- TutorConversation: (user_id, document_id)
- UserNote: (user_id, document_id)
- Recommendation: (user_id, priority), (created_at)