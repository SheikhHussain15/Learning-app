import logging
import uuid

from openai import AsyncOpenAI
from sqlalchemy.orm import Session

from src.agents.registry import create_openai_provider
from src.models.progress_event import ProgressEvent, ProgressEventType
from src.models.tutor_conversation import TutorConversation
from src.retrieval.retriever import get_retriever
from src.schemas.agent import RetrievedChunk
from src.schemas.tutor import (
    SourceReference,
    TutorConversationResponse,
    TutorMessageRequest,
    TutorMessageResponse,
)

logger = logging.getLogger(__name__)

TUTOR_SYSTEM_PROMPT = """You are an AI tutor helping a student learn from their documents. You are knowledgeable, patient, and skilled at explaining complex topics clearly.

Guidelines:
- Use the provided document context to answer questions accurately.
- If the context doesn't contain enough information, use your general knowledge but clearly indicate when you are doing so.
- Provide clear explanations with examples when helpful.
- Break down complex topics step by step.
- Ask clarifying questions if the student's question is vague.
- Be concise but thorough.
- NEVER make up quotes or specific references not in the context.

Document Context:
{context}

Conversation History:
{history}"""


class TutorService:
    def __init__(self, db: Session):
        self.db = db

    async def send_message(self, user_id: str, request: TutorMessageRequest) -> TutorMessageResponse:
        conversation = self._get_or_create_conversation(user_id, request.document_id)

        messages = conversation.messages or []
        messages.append({"role": "user", "content": request.content})
        conversation.messages = messages

        retrieved_chunks: list[RetrievedChunk] = []
        try:
            retriever = get_retriever()
            retrieved_chunks = retriever.retrieve(
                f"doc_{request.document_id}", request.content, top_k=5
            )
        except Exception:
            logger.warning("Chunk retrieval failed for tutor chat", exc_info=True)

        sources = [
            SourceReference(
                chunk_id=c.chunk_id,
                document_id=request.document_id,
                chapter_title=c.metadata.get("chapter_title", ""),
                topic_title=c.metadata.get("topic_title", ""),
                content_preview=c.text[:200],
                relevance_score=c.score,
            )
            for c in retrieved_chunks
        ]

        ai_response = await self._generate_response(
            message=request.content,
            document_id=request.document_id,
            conversation_history=messages[:-1],
            chunks=retrieved_chunks,
        )
        messages.append({"role": "assistant", "content": ai_response})
        conversation.messages = messages

        event = ProgressEvent(
            id=str(uuid.uuid4()),
            user_id=user_id,
            event_type=ProgressEventType.tutor_used,
            document_id=request.document_id,
            event_data={"message_count": len(messages)},
        )
        self.db.add(event)
        self.db.commit()

        return TutorMessageResponse(
            message_id=str(uuid.uuid4()),
            role="assistant",
            content=ai_response,
            sources=sources,
            is_grounded=len(retrieved_chunks) > 0,
            confidence=0.8 if retrieved_chunks else 0.5,
        )

    async def get_conversation(self, user_id: str, document_id: str, limit: int = 50) -> TutorConversationResponse:
        conversation = self._get_or_create_conversation(user_id, document_id)
        messages = conversation.messages or []

        return TutorConversationResponse(
            id=conversation.id,
            document_id=document_id,
            user_id=user_id,
            title=conversation.title or "Conversation",
            message_count=len(messages),
            messages=[
                TutorMessageResponse(
                    message_id=str(i),
                    role=m.get("role", "user"),
                    content=m.get("content", ""),
                    sources=[],
                    is_grounded=True,
                    confidence=0.8,
                )
                for i, m in enumerate(messages)
            ],
        )

    def _get_or_create_conversation(self, user_id: str, document_id: str) -> TutorConversation:
        conversation = (
            self.db.query(TutorConversation)
            .filter(
                TutorConversation.user_id == user_id,
                TutorConversation.document_id == document_id,
            )
            .first()
        )

        if not conversation:
            conversation = TutorConversation(
                id=str(uuid.uuid4()),
                user_id=user_id,
                document_id=document_id,
                title="New Conversation",
                messages=[],
            )
            self.db.add(conversation)
            self.db.flush()

        return conversation

    async def _generate_response(
        self,
        message: str,
        document_id: str,
        conversation_history: list[dict] | None = None,
        chunks: list[RetrievedChunk] | None = None,
    ) -> str:
        try:
            context_text = "No specific document context available for this question."
            if chunks:
                context_text = "\n\n".join(
                    f"[{c.chunk_id}]: {c.text}" for c in chunks
                )

            history_text = "No previous conversation history."
            if conversation_history:
                lines = [
                    f'{m.get("role", "user")}: {m.get("content", "")}'
                    for m in conversation_history[-10:]
                ]
                history_text = "\n".join(lines)

            system_prompt = TUTOR_SYSTEM_PROMPT.format(
                context=context_text, history=history_text
            )

            provider = create_openai_provider()
            client = AsyncOpenAI(
                api_key=provider.api_key, base_url=provider.base_url
            )

            response = await client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=0.3,
                max_tokens=1024,
            )

            return (
                response.choices[0].message.content
                or "I'm sorry, I couldn't generate a response."
            )

        except Exception as e:
            logger.exception("Tutor LLM generation failed: %s", e)
            return "I'm having trouble processing your question right now. Please try again."
