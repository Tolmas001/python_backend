import json
from openai import OpenAI
from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


async def analyze_comment(
        comment: str
):

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    """
                    Analyze user comment.

                    Return JSON:

                    {
                        "sentiment":"",
                        "category":"",
                        "auto_reply":""
                    }
                    """
                },
                {
                    "role": "user",
                    "content": comment
                }
            ]
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        return json.loads(
            content
        )

    except Exception:

        return {
            "sentiment": "unknown",
            "category": "general",
            "auto_reply":
            "Thank you for contacting us."
        }