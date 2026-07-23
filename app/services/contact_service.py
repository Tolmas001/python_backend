from app.services.ai_service import (
    analyze_comment
)
from app.services.email_service import (
    send_email,
    create_contact_email_html,
    create_user_reply_html
)
from app.services.metrics_service import (
    update_metrics
)
from app.core.config import settings


async def process_contact(
        data
):

    ai = {
        "sentiment": "unknown",
        "category": "general",
        "auto_reply": "Thank you for contacting us."
    }

    try:
        ai = await analyze_comment(
            data.comment
        )
    except Exception:
        import traceback
        traceback.print_exc()

    update_metrics(
        ai["sentiment"]
    )

    if settings.OWNER_EMAIL:
        try:
            await send_email(
                settings.OWNER_EMAIL,
                "Новое обращение с сайта",
                create_contact_email_html(data, ai)
            )
            await send_email(
                data.email,
                "Спасибо за ваше обращение",
                create_user_reply_html(data, ai)
            )
        except Exception:
            import traceback
            traceback.print_exc()

    return ai
