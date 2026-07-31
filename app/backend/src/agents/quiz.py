import json
import logging

from langfuse import observe
from openai import AsyncOpenAI

from src.agents.production_base import ProductionAgent
from src.agents.registry import create_openai_provider
from src.schemas.agent import ErrorInfo, RequestEnvelope, ResponseEnvelope, TokenUsage
from src.schemas.agent_outputs import QuizMetadata, QuizOutput, QuizQuestion

logger = logging.getLogger(__name__)

QUIZ_PROMPT = """Generate a quiz based on the following text content.

Create {num_questions} multiple-choice questions with 4 options each.
Difficulty level: {difficulty}
- easy: Recall/factual questions
- medium: Comprehension/application questions
- hard: Analysis/synthesis questions

For each question:
1. Provide the question text
2. Provide exactly 4 options
3. Indicate the correct answer index (0-3)
4. Provide an explanation
5. Reference source chunk IDs

Text content:
{chunks}

Return ONLY valid JSON:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "correct_index": 0,
      "explanation": "string",
      "difficulty": "easy|medium|hard",
      "source_chunk_ids": ["string"]
    }}
  ],
  "metadata": {{
    "total_questions": {num_questions},
    "difficulty_distribution": {{"easy": 0, "medium": 0, "hard": 0}},
    "coverage_nodes": ["string"]
  }}
}}"""


class QuizAgent(ProductionAgent):
    agent_type: str = "quiz"

    @observe(name="agent.quiz.invoke", as_type="span")
    async def invoke(self, envelope: RequestEnvelope) -> ResponseEnvelope:
        validation_error = self.validate_envelope(envelope)
        if validation_error:
            return self.make_error_response(validation_error)

        try:
            chunks = []
            if envelope.context and envelope.context.chunks:
                chunks = envelope.context.chunks

            if not chunks:
                return self.make_error_response(
                    ErrorInfo(code="NO_INPUT", message="No chunks provided for quiz generation", retryable=False)
                )

            num_questions = envelope.agent_params.get("question_count", 5)
            difficulty = envelope.agent_params.get("difficulty", "medium")

            chunk_text = "\n\n".join([
                f"[{c.chunk_id}]: {c.text}" for c in chunks[:15]
            ])

            prompt = QUIZ_PROMPT.format(
                chunks=chunk_text,
                num_questions=num_questions,
                difficulty=difficulty,
            )

            provider = create_openai_provider()
            client = AsyncOpenAI(api_key=provider.api_key, base_url=provider.base_url)

            response = await client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3,
            )

            result = json.loads(response.choices[0].message.content)

            questions = [QuizQuestion(**q) for q in result.get("questions", [])]
            metadata = QuizMetadata(**result.get("metadata", {
                "total_questions": len(questions),
                "difficulty_distribution": {},
                "coverage_nodes": [],
            }))

            output = QuizOutput(questions=questions, metadata=metadata)

            source_refs = self.make_source_refs(
                [c.chunk_id for c in chunks],
                envelope.document_id,
            )

            usage = response.usage
            return ResponseEnvelope(
                status="success",
                output=output.model_dump(),
                source_refs=source_refs,
                usage=TokenUsage(
                    prompt_tokens=usage.prompt_tokens if usage else 0,
                    completion_tokens=usage.completion_tokens if usage else 0,
                    total_tokens=usage.total_tokens if usage else 0,
                ),
            )

        except Exception as e:
            logger.exception("QuizAgent failed: %s", e)
            return self.make_error_response(
                ErrorInfo(code="QUIZ_ERROR", message=str(e), retryable=False)
            )
