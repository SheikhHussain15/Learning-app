
from pydantic import BaseModel, Field


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


class DocumentProcessingOutput(BaseModel):
    raw_text: str
    chunks: list[ProcessedChunk]
    metadata: DocumentMetadata
    language: str
    page_count: int


class ProcessingNodeData(BaseModel):
    node_id: str
    node_type: str  # "chapter", "topic", "subtopic"
    title: str
    content: str
    parent_id: str | None = None
    position: int
    chunk_ids: list[str]


class NodeRelationship(BaseModel):
    source_id: str
    target_id: str
    relationship_type: str  # "contains", "related_to", "depends_on"


class KnowledgeStructuringOutput(BaseModel):
    nodes: list[ProcessingNodeData]
    relationships: list[NodeRelationship]


class NodeSummary(BaseModel):
    node_id: str
    summary_text: str
    key_points: list[str]
    source_chunk_ids: list[str]


class SummaryOutput(BaseModel):
    summaries: list[NodeSummary]
    overall_summary: str


class ConceptExplanation(BaseModel):
    concept: str
    explanation: str
    examples: list[str]
    complexity_level: str  # "beginner", "intermediate", "advanced"
    source_chunk_ids: list[str]


class ExplanationOutput(BaseModel):
    explanations: list[ConceptExplanation]


class NodeTranslation(BaseModel):
    node_id: str
    translated_text: str
    source_chunk_ids: list[str]


class TranslationOutput(BaseModel):
    translations: list[NodeTranslation]
    source_language: str
    target_language: str


class DiagramData(BaseModel):
    diagram_type: str  # "mermaid", "excalidraw"
    diagram_data: str
    description: str
    source_chunk_ids: list[str]


class DiagramOutput(BaseModel):
    diagrams: list[DiagramData]


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_index: int = Field(ge=0, le=3)
    explanation: str
    difficulty: str  # "easy", "medium", "hard"
    source_chunk_ids: list[str]


class QuizMetadata(BaseModel):
    total_questions: int
    difficulty_distribution: dict[str, int]
    coverage_nodes: list[str]


class QuizOutput(BaseModel):
    questions: list[QuizQuestion]
    metadata: QuizMetadata


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


class RevisionOutput(BaseModel):
    notes: list[RevisionNote]
    flashcards: list[Flashcard]


class UserProgressSummary(BaseModel):
    documents_studied: int
    total_quiz_score: float
    topics_mastered: list[str]
    areas_needing_review: list[str]


class ProgressOutput(BaseModel):
    events_recorded: int
    user_progress: UserProgressSummary


class Recommendation(BaseModel):
    recommendation_type: str  # "study", "review", "quiz", "explore"
    title: str
    reason: str
    confidence: float = Field(ge=0.0, le=1.0)
    source_doc_ids: list[str]


class WeakArea(BaseModel):
    topic: str
    score: float = Field(ge=0.0, le=1.0)
    suggested_action: str


class RecommendationOutput(BaseModel):
    recommendations: list[Recommendation]
    weak_areas: list[WeakArea]
