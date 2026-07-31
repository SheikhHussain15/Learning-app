# Data Model: AI Agent Orchestration — Phase 4

## Extended Enum: AgentType

| Value | Description | Pipeline Position |
|-------|-------------|-------------------|
| echo | Echo (placeholder) agent | N/A (testing) |
| document_processing | Document parsing, OCR, text cleaning | Step 1 (mandatory) |
| knowledge_structuring | Chapter/topic/subtopic hierarchy | Step 2 (mandatory) |
| summary | Content summarization | Step 3 (optional, parallel) |
| explanation | Concept explanation | Step 3 (optional, parallel) |
| translation | Multilingual translation | Step 3 (optional, parallel) |
| diagram | Diagram data generation | Step 3 (optional, parallel) |
| quiz | Quiz/assessment generation | Step 3 (optional, parallel) |
| revision | Revision notes & flashcards | Step 3 (optional, parallel) |
| progress | Learning event recording | Standalone |
| recommendation | Personalized study recommendations | Standalone |

## Entity: ProcessingNode

Represents a hierarchical unit of document structure (chapter, topic, subtopic).

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | UUID (PK) | Yes | Auto | Unique identifier |
| document_id | UUID (FK) | Yes | — | Source document |
| parent_id | UUID (FK) | No | null | Parent node (null = root) |
| node_type | Enum(NodeType) | Yes | — | chapter, topic, subtopic |
| title | String | Yes | — | Node title |
| content | Text | No | null | Extracted text content |
| position | Integer | Yes | — | Order within parent |
| metadata | JSON | No | {} | Page numbers, section headers |
| chunk_ids | JSON | No | [] | Associated retrieval chunk IDs |
| created_at | DateTime | Yes | now() | Record creation |
| updated_at | DateTime | Yes | now() | Last update |

### Validation Rules

- `parent_id` must reference an existing ProcessingNode with the same `document_id`
- `node_type` hierarchy: chapter → topic → subtopic (no skipping levels)
- `position` must be >= 0 and unique within the same parent
- `content` is populated by Document Processing agent, refined by Knowledge Structuring

### Indexes

- Primary: `id`
- Query: `(document_id, parent_id)` for tree traversal
- Query: `(document_id, node_type)` for filtering by level

## Enum: NodeType

| Value | Description |
|-------|-------------|
| chapter | Top-level document section |
| topic | Mid-level section within a chapter |
| subtopic | Detailed section within a topic |

## Entity: AgentOutput

Caches agent execution results for incremental processing.

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | UUID (PK) | Yes | Auto | Unique identifier |
| document_id | UUID (FK) | Yes | — | Source document |
| agent_type | Enum(AgentType) | Yes | — | Which agent produced this |
| params_hash | String | Yes | — | SHA256 of agent_params |
| output_data | JSON | Yes | — | Agent-specific output content |
| source_refs | JSON | No | [] | Source references |
| token_usage | JSON | No | {} | Token consumption |
| created_at | DateTime | Yes | now() | When output was generated |

### Validation Rules

- `params_hash` is deterministic: `sha256(json.dumps(agent_params, sort_keys=True))`
- `output_data` must conform to the agent-specific output schema
- Cache invalidation: delete when document is re-processed

### Indexes

- Primary: `id`
- Query: `(document_id, agent_type, params_hash)` for cache lookup (UNIQUE)

## Entity: ProgressEvent

Records user learning events for recommendation engine.

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | UUID (PK) | Yes | Auto | Unique identifier |
| user_id | UUID (FK) | Yes | — | Learning user |
| document_id | UUID (FK) | No | null | Related document |
| event_type | Enum(EventType) | Yes | — | Type of learning event |
| event_data | JSON | No | {} | Event-specific payload |
| created_at | DateTime | Yes | now() | When event occurred |

### Validation Rules

- `event_data` schema varies by `event_type`:
  - `quiz_completed`: `{score, total_questions, difficulty, duration_ms}`
  - `document_viewed`: `{node_id, time_spent_ms, scroll_depth}`
  - `revision_studied`: `{card_id, mastery_level, review_count}`
  - `explanation_requested`: `{node_id, complexity_level}`
  - `recommendation_dismissed`: `{recommendation_id, reason}`

### Indexes

- Primary: `id`
- Query: `(user_id, event_type, created_at)` for progress queries
- Query: `(user_id, document_id)` for document-specific progress

## Enum: EventType

| Value | Description |
|-------|-------------|
| quiz_completed | User completed a quiz |
| document_viewed | User viewed document content |
| revision_studied | User studied revision flashcards |
| explanation_requested | User requested concept explanation |
| recommendation_dismissed | User dismissed a recommendation |

## Schema: DocumentProcessingOutput

```python
class DocumentProcessingOutput(BaseModel):
    raw_text: str
    chunks: list[ProcessedChunk]
    metadata: DocumentMetadata
    language: str
    page_count: int

class ProcessedChunk(BaseModel):
    chunk_id: str
    text: str
    position: int
    page_number: int | None = None
    section_header: str | None = None

class DocumentMetadata(BaseModel):
    title: str | None = None
    author: str | None = None
    format: str
    character_count: int
    word_count: int
```

## Schema: KnowledgeStructuringOutput

```python
class KnowledgeStructuringOutput(BaseModel):
    nodes: list[ProcessingNodeData]
    relationships: list[NodeRelationship]

class ProcessingNodeData(BaseModel):
    node_id: str
    node_type: NodeType
    title: str
    content: str
    parent_id: str | None = None
    position: int
    chunk_ids: list[str]

class NodeRelationship(BaseModel):
    source_id: str
    target_id: str
    relationship_type: str  # "contains", "related_to", "depends_on"
```

## Schema: SummaryOutput

```python
class SummaryOutput(BaseModel):
    summaries: list[NodeSummary]
    overall_summary: str

class NodeSummary(BaseModel):
    node_id: str
    summary_text: str
    key_points: list[str]
    source_chunk_ids: list[str]
```

## Schema: ExplanationOutput

```python
class ExplanationOutput(BaseModel):
    explanations: list[ConceptExplanation]

class ConceptExplanation(BaseModel):
    concept: str
    explanation: str
    examples: list[str]
    complexity_level: str  # "beginner", "intermediate", "advanced"
    source_chunk_ids: list[str]
```

## Schema: TranslationOutput

```python
class TranslationOutput(BaseModel):
    translations: list[NodeTranslation]
    source_language: str
    target_language: str

class NodeTranslation(BaseModel):
    node_id: str
    translated_text: str
    source_chunk_ids: list[str]
```

## Schema: DiagramOutput

```python
class DiagramOutput(BaseModel):
    diagrams: list[DiagramData]

class DiagramData(BaseModel):
    diagram_type: str  # "mermaid", "excalidraw"
    diagram_data: str
    description: str
    source_chunk_ids: list[str]
```

## Schema: QuizOutput

```python
class QuizOutput(BaseModel):
    questions: list[QuizQuestion]
    metadata: QuizMetadata

class QuizQuestion(BaseModel):
    question: str
    options: list[str]  # 4 options
    correct_index: int
    explanation: str
    difficulty: str  # "easy", "medium", "hard"
    source_chunk_ids: list[str]

class QuizMetadata(BaseModel):
    total_questions: int
    difficulty_distribution: dict[str, int]
    coverage_nodes: list[str]
```

## Schema: RevisionOutput

```python
class RevisionOutput(BaseModel):
    notes: list[RevisionNote]
    flashcards: list[Flashcard]

class RevisionNote(BaseModel):
    node_id: str
    note_text: str
    key_formulas: list[str]
    source_chunk_ids: list[str]

class Flashcard(BaseModel):
    front: str
    back: str
    difficulty: str
    category: str
    source_chunk_ids: list[str]
```

## Schema: ProgressOutput

```python
class ProgressOutput(BaseModel):
    events_recorded: int
    user_progress: UserProgressSummary

class UserProgressSummary(BaseModel):
    documents_studied: int
    total_quiz_score: float
    topics_mastered: list[str]
    areas_needing_review: list[str]
```

## Schema: RecommendationOutput

```python
class RecommendationOutput(BaseModel):
    recommendations: list[Recommendation]
    weak_areas: list[WeakArea]

class Recommendation(BaseModel):
    recommendation_type: str  # "study", "review", "quiz", "explore"
    title: str
    reason: str
    confidence: float  # 0.0 - 1.0
    source_doc_ids: list[str]

class WeakArea(BaseModel):
    topic: str
    score: float  # 0.0 - 1.0
    suggested_action: str
```

## Schema: PipelineRequest

```python
class PipelineRequest(BaseModel):
    document_id: str
    user_id: str
    requested_agents: list[AgentType] = Field(default_factory=list)
    agent_params: dict[str, dict[str, Any]] = Field(default_factory=dict)
    force_reprocess: bool = False

class PipelineResponse(BaseModel):
    pipeline_id: str
    status: str  # "queued", "running", "succeeded", "partial", "failed"
    agent_results: dict[str, AgentRunResponse]
    duration_ms: int | None = None
```
