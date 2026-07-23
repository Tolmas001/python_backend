import json

from openai import AsyncOpenAI
from app.core.config import settings


_client = None


def get_ai_client():
    global _client
    if not settings.OPENAI_API_KEY:
        return None
    if _client is None:
        _client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )
    return _client


async def analyze_comment(comment: str):

    client = get_ai_client()
    fallback = {
        "sentiment": "unknown",
        "category": "general",
        "auto_reply": "Thank you for contacting us."
    }

    if not client:
        return fallback

    try:

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Analyze this customer message. "
                        "Return ONLY valid JSON: "
                        '{"sentiment": "positive/negative/neutral", '
                        '"category": "support/sales/general", '
                        '"auto_reply": "short polite reply"}'
                    )
                },
                {
                    "role": "user",
                    "content": comment
                }
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        import traceback

        print("\n========== AI ERROR ==========")
        print(e)
        traceback.print_exc()
        print("==================================\n")

        return fallback
