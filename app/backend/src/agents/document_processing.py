import logging
import re
import uuid
from pathlib import Path

from langfuse import observe

from src.agents.production_base import ProductionAgent
from src.schemas.agent import ErrorInfo, RequestEnvelope, ResponseEnvelope, TokenUsage
from src.schemas.agent_outputs import DocumentMetadata, DocumentProcessingOutput, ProcessedChunk

logger = logging.getLogger(__name__)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def extract_text_from_pdf(file_path: str) -> tuple[str, int]:
    """Extract text from PDF using pdfplumber."""
    try:
        import pdfplumber
        text_parts = []
        page_count = 0
        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n\n".join(text_parts), page_count
    except ImportError:
        logger.warning("pdfplumber not installed, falling back to basic extraction")
        return "", 0


def extract_text_from_docx(file_path: str) -> tuple[str, int]:
    """Extract text from DOCX using python-docx."""
    try:
        from docx import Document
        doc = Document(file_path)
        text = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text, 1
    except ImportError:
        logger.warning("python-docx not installed")
        return "", 0


def extract_text_from_txt(file_path: str) -> tuple[str, int]:
    """Extract text from plain text file."""
    with open(file_path, encoding="utf-8") as f:
        return f.read(), 1


def clean_text(text: str) -> str:
    """Normalize whitespace, remove headers/footers."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()
    return text


def detect_language(text: str) -> str:
    """Simple language detection based on common words."""
    english_words = {'the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'for'}
    words = set(text.lower().split())
    overlap = len(words.intersection(english_words))
    return "en" if overlap > 3 else "unknown"


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[dict]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    position = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]

        if chunk_text.strip():
            chunks.append({
                "chunk_id": f"chunk-{uuid.uuid4().hex[:8]}",
                "text": chunk_text.strip(),
                "position": position,
                "page_number": None,
                "section_header": None,
            })
            position += 1

        start = end - overlap
        if start >= len(text):
            break

    return chunks


class DocumentProcessingAgent(ProductionAgent):
    agent_type: str = "document_processing"

    @observe(name="agent.document_processing.invoke", as_type="span")
    async def invoke(self, envelope: RequestEnvelope) -> ResponseEnvelope:
        validation_error = self.validate_envelope(envelope)
        if validation_error:
            return self.make_error_response(validation_error)

        try:
            file_path = envelope.context.source_doc_id if envelope.context else None
            if not file_path:
                file_path = envelope.document_id

            text = ""
            page_count = 1

            path = Path(file_path)
            if path.exists():
                suffix = path.suffix.lower()
                if suffix == '.pdf':
                    text, page_count = extract_text_from_pdf(str(path))
                elif suffix == '.docx':
                    text, page_count = extract_text_from_docx(str(path))
                elif suffix == '.txt':
                    text, page_count = extract_text_from_txt(str(path))
                else:
                    text = file_path
            else:
                text = file_path

            cleaned_text = clean_text(text)
            language = detect_language(cleaned_text)
            chunks = split_into_chunks(cleaned_text)

            word_count = len(cleaned_text.split())
            char_count = len(cleaned_text)

            output = DocumentProcessingOutput(
                raw_text=cleaned_text,
                chunks=[ProcessedChunk(**c) for c in chunks],
                metadata=DocumentMetadata(
                    format=path.suffix.lower() if path.exists() else "text",
                    character_count=char_count,
                    word_count=word_count,
                ),
                language=language,
                page_count=page_count,
            )

            source_refs = self.make_source_refs(
                [c.chunk_id for c in output.chunks],
                envelope.document_id,
            )

            return ResponseEnvelope(
                status="success",
                output=output.model_dump(),
                source_refs=source_refs,
                usage=TokenUsage(prompt_tokens=char_count, completion_tokens=0, total_tokens=char_count),
            )

        except Exception as e:
            logger.exception("DocumentProcessingAgent failed: %s", e)
            return self.make_error_response(
                ErrorInfo(code="PROCESSING_ERROR", message=str(e), retryable=False)
            )
