# Research: AI Agent Orchestration — Phase 4

## Research Tasks

### 1. Document Parsing Patterns for Educational Content

- **Decision**: Use Python `PyPDF2`/`pdfplumber` for PDF extraction, `python-docx` for DOCX, and plain `open()` for TXT. Normalize all extracted text into the unified `RetrievedChunk` format.
- **Rationale**: Educational documents are predominantly PDFs (textbooks, papers) and DOCX (lecture notes). `pdfplumber` handles tables and complex layouts better than PyPDF2. For OCR on scanned PDFs, fallback to `pytesseract` (Tesseract OCR) with image preprocessing via `Pillow`.
- **Alternatives Considered**: Apache Tika — rejected because it requires a separate Java service. Unstructured.io — viable but adds a large dependency for Phase 4 scope.
- **Key Finding**: Text cleaning pipeline: normalize whitespace, remove headers/footers, detect language, split into ~500-char chunks with overlap. Store metadata (page number, section header, position) for source references.

### 2. Hierarchical Chapter/Topic/Subtopic Extraction

- **Decision**: Use LLM-based structural analysis on cleaned text chunks. The Knowledge Structuring agent sends chunked text to the LLM with a structured output prompt requesting chapter→topic→subtopic hierarchy.
- **Rationale**: Educational documents have implicit structure (headings, sections, paragraphs). LLMs excel at identifying semantic boundaries. The output is a `ProcessingNode` tree with parent-child relationships.
- **Alternatives Considered**: Rule-based heading detection (regex for "Chapter 1", "1.1") — rejected because it fails on non-standard formatting. spaCy NLP parsing — insufficient for document-level structure.
- **Key Finding**: Prompt the LLM with `response_format=json_schema` to enforce a typed hierarchy output. Include the first 200 chars of each chunk as context for the LLM to classify. Store as `ProcessingNode` entities with `parent_id` FK for tree traversal.

### 3. Grounded Summarization with Source References

- **Decision**: Pass retrieval chunks as context to the Summary agent. The agent generates summaries and explicitly tags each paragraph/sentence with the source chunk_id it was derived from.
- **Rationale**: Grounding requires that every generated sentence traces back to source material. The `source_refs` field in `ResponseEnvelope` carries this linkage. The LLM prompt instructs: "For each section of your summary, include [source: chunk_id]" markers.
- **Alternatives Considered**: Post-hoc similarity matching to find source chunks — rejected because it's unreliable and doesn't guarantee grounding. RAG-only without explicit markers — rejected because it doesn't meet SC-007 (100% source references).
- **Key Finding**: Use a two-pass approach: (1) generate summary with inline source markers, (2) parse markers into `SourceRef` objects. This ensures every output paragraph has a traceable origin.

### 4. Quiz Generation with Difficulty Calibration

- **Decision**: Generate quizzes with explicit difficulty levels (easy/medium/hard) controlled by `agent_params.difficulty`. Use structured output to produce question, options, correct answer, explanation, and source reference per question.
- **Rationale**: SC-010 requires genuinely different question complexity. Easy = recall/factual, Medium = comprehension/application, Hard = analysis/synthesis. The LLM prompt includes difficulty-specific instructions and Bloom's taxonomy alignment.
- **Alternatives Considered**: Question bank with pre-written questions — rejected because it doesn't scale to arbitrary document content. Template-based generation — rejected because it produces repetitive, low-quality questions.
- **Key Finding**: Use `response_format=json_schema` with a `QuizQuestion` schema: `{question, options: [str], correct_index, explanation, difficulty, source_chunk_ids}`. Validate that difficulty distribution matches requested params.

### 5. Diagram Data Generation

- **Decision**: Generate Mermaid diagram syntax or Excalidraw JSON from text content. The Diagram agent analyzes relationships, processes, and concepts to produce visual representations.
- **Rationale**: Mermaid is text-based, version-controllable, and renders in most markdown viewers. Excalidraw provides editable hand-drawn style diagrams. Both are machine-readable and don't require image generation.
- **Alternatives Considered**: Direct image generation (DALL-E) — rejected because it's not editable and doesn't meet "editable diagram data" requirement. Graphviz DOT — less user-friendly than Mermaid.
- **Key Finding**: Output format: `{diagram_type: "mermaid"|"excalidraw", diagram_data: str, description: str, source_chunk_ids: []}`. Support flowcharts, sequence diagrams, and concept maps.

### 6. Progress Tracking Event Schema

- **Decision**: Record structured learning events as `ProgressEvent` entities: `{user_id, document_id, event_type, event_data, timestamp}`. Event types: `quiz_completed`, `document_viewed`, `revision Studied`, `explanation_requested`, `recommendation_dismissed`.
- **Rationale**: Progress data feeds the Recommendation agent. Events capture what the user studied, how they performed, and what they engaged with. Simple event-sourced design avoids complex state management.
- **Alternatives Considered**: Real-time session tracking — rejected because it adds WebSocket complexity. Aggregated metrics only — rejected because it loses granular detail needed for recommendations.
- **Key Finding**: Store events in PostgreSQL with index on `(user_id, document_id, event_type, created_at)`. Aggregate into `UserProgress` materialized view for fast recommendation queries.

### 7. Recommendation Engine Patterns

- **Decision**: Hybrid approach: (1) content-based filtering using document similarity and topic coverage, (2) performance-based filtering using quiz scores and completion rates, (3) collaborative filtering using peer performance patterns.
- **Rationale**: New users need content-based recommendations (no history). Established users benefit from performance-based targeting of weak areas. Collaborative filtering adds serendipity.
- **Alternatives Considered**: Pure collaborative filtering — cold start problem for new users. Rule-based recommendations — too rigid, doesn't adapt to individual patterns.
- **Key Finding**: Start with content-based + performance hybrid. Collaborative filtering can be added later. Recommendation output: `{recommendations: [{type, reason, confidence, source_doc_ids}], weak_areas: [{topic, score, suggested_action}]}`.

### 8. Multi-Agent Pipeline with Dependency DAG

- **Decision**: Define a static dependency graph: Document Processing → Knowledge Structuring → [Summary, Explanation, Translation, Diagram, Quiz, Revision] (parallel). Progress and Recommendation are standalone.
- **Rationale**: The mandatory pipeline (Document Processing → Knowledge Structuring) must complete before any content agent runs. Content agents are independent of each other and can run in parallel. Progress and Recommendation are user-scoped, not document-scoped.
- **Alternatives Considered**: Fully dynamic dependency resolution — rejected because it adds complexity without benefit for the fixed agent set. Sequential execution — rejected because it violates SC-001 (<60s pipeline target).
- **Key Finding**: Use `asyncio.gather()` for parallel content agent execution. Pipeline state tracked in `OrchestrationRun` entity. Each agent checks dependency completion before executing.

### 9. Incremental Processing with Output Caching

- **Decision**: Cache agent outputs in `AgentOutput` table keyed by `(document_id, agent_type, agent_params_hash)`. Before invoking an agent, check if a matching output exists and is still valid.
- **Rationale**: SC-003 requires 50% time reduction for incremental processing. Caching avoids re-running agents whose inputs haven't changed. `agent_params_hash` ensures different difficulty levels or parameters trigger re-execution.
- **Alternatives Considered**: Time-based cache expiry — rejected because document content doesn't expire. Version-based invalidation — viable but more complex than hash-based matching.
- **Key Finding**: Compute `params_hash = sha256(json.dumps(agent_params, sort_keys=True))`. Cache lookup: `SELECT * FROM agent_outputs WHERE document_id=? AND agent_type=? AND params_hash=?`. Invalidate on document re-processing.

## Technology Stack Decisions

| Component | Decision | Rationale |
|-----------|----------|-----------|
| PDF Extraction | pdfplumber | Better table/layout handling than PyPDF2 |
| OCR Fallback | pytesseract + Pillow | Free, well-supported, handles scanned docs |
| DOCX Parsing | python-docx | Native Python, no external services |
| Structured LLM Output | response_format=json_schema | Enforces typed output, no post-parsing |
| Diagram Format | Mermaid + Excalidraw | Text-based, editable, widely supported |
| Progress Storage | PostgreSQL events | Event-sourced, indexable, queryable |
| Recommendation | Content + Performance hybrid | Handles cold start, targets weak areas |
| Pipeline Execution | asyncio.gather() | Parallel content agents, <60s target |
| Output Caching | params_hash matching | Avoids redundant execution, deterministic |

## Integration Patterns

- **Document Processing → Knowledge Structuring**: Chunks from Document Processing become input to Knowledge Structuring. The structuring agent receives raw chunks and outputs a hierarchical ProcessingNode tree.
- **Knowledge Structuring → Content Agents**: Each content agent receives the ProcessingNode tree + relevant chunks via retrieval. They generate content anchored to specific nodes/chunks.
- **All Content Agents → ResponseEnvelope**: Every agent outputs a ResponseEnvelope with `source_refs` linking generated content to source chunks.
- **Progress Events → Recommendation Agent**: Progress events are aggregated into a UserProgress profile. The Recommendation agent analyzes this profile to suggest next steps.
- **Pipeline → Orchestrator**: The Orchestrator manages the full pipeline: validates dependencies, checks cache, dispatches agents in order, and collects results.
