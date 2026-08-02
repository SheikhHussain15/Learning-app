import json
import logging

from langfuse import observe
from openai import AsyncOpenAI

from src.agents.production_base import ProductionAgent
from src.agents.registry import create_openai_provider
from src.schemas.agent import ErrorInfo, RequestEnvelope, ResponseEnvelope, TokenUsage
from src.schemas.agent_outputs import Recommendation, RecommendationOutput, WeakArea
from src.services.progress_service import get_user_events, get_user_progress_summary

logger = logging.getLogger(__name__)

RECOMMENDATION_PROMPT = """Based on the user's learning progress, generate personalized study recommendations.

User Progress:
- Documents studied: {documents_studied}
- Quiz score: {total_quiz_score:.1%}
- Topics mastered: {topics_mastered}
- Areas needing review: {areas_needing_review}

Recent Activity:
{recent_activity}

Generate 3-5 recommendations covering study, review, quiz, and explore types.
Also identify weak areas that need attention.

Return ONLY valid JSON:
{{
  "recommendations": [
    {{
      "recommendation_type": "study|review|quiz|explore",
      "title": "string",
      "reason": "string",
      "confidence": 0.0-1.0,
      "source_doc_ids": ["string"]
    }}
  ],
  "weak_areas": [
    {{
      "topic": "string",
      "score": 0.0-1.0,
      "suggested_action": "string"
    }}
  ]
}}"""


class RecommendationAgent(ProductionAgent):
    agent_type: str = "recommendation"

    @observe(name="agent.recommendation.invoke", as_type="span")
    async def invoke(self, envelope: RequestEnvelope) -> ResponseEnvelope:
        validation_error = self.validate_envelope(envelope)
        if validation_error:
            return self.make_error_response(validation_error)

        try:
            user_id = envelope.agent_params.get("user_id", "anonymous")

            progress = get_user_progress_summary(user_id)
            recent_events = get_user_events(user_id, limit=10)

            recent_activity = "\n".join([
                f"- {e.event_type.value}: {e.event_data}" for e in recent_events
            ]) or "No recent activity"

            prompt = RECOMMENDATION_PROMPT.format(
                documents_studied=progress.get("documents_studied", 0),
                total_quiz_score=progress.get("total_quiz_score", 0.0),
                topics_mastered=progress.get("topics_mastered", []),
                areas_needing_review=progress.get("areas_needing_review", []),
                recent_activity=recent_activity,
            )

            provider = create_openai_provider()
            client = AsyncOpenAI(api_key=provider.api_key, base_url=provider.base_url)

            response = await client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.5,
                max_tokens=2000,
            )

            result = json.loads(response.choices[0].message.content)

            recommendations = [Recommendation(**r) for r in result.get("recommendations", [])]
            weak_areas = [WeakArea(**w) for w in result.get("weak_areas", [])]
            output = RecommendationOutput(
                recommendations=recommendations,
                weak_areas=weak_areas,
            )

            usage = response.usage
            return ResponseEnvelope(
                status="success",
                output=output.model_dump(),
                source_refs=[],
                usage=TokenUsage(
                    prompt_tokens=usage.prompt_tokens if usage else 0,
                    completion_tokens=usage.completion_tokens if usage else 0,
                    total_tokens=usage.total_tokens if usage else 0,
                ),
            )

        except Exception as e:
            logger.exception("RecommendationAgent failed: %s", e)
            return self.make_error_response(
                ErrorInfo(code="RECOMMENDATION_ERROR", message=str(e), retryable=False)
            )
