from flask import (
    Blueprint,
    request,
    jsonify,
    session
)

from flask_login import (
    login_required,
    current_user
)

from services.ai_service import generate_response
from services.sentiment_service import analyze_sentiment

from database.db import db
from database.models import ChatHistory


# ---------------------------------------------------
# Blueprint
# ---------------------------------------------------

chat_bp = Blueprint(
    "chat",
    __name__
)


MAX_HISTORY = 20


# ---------------------------------------------------
# Chat Route
# ---------------------------------------------------

@chat_bp.route(
    "/get_response",
    methods=["POST"]
)
@login_required
def get_response():

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({

                "error": "No data received"

            }), 400

        user_message = data.get(
            "message",
            ""
        ).strip()

        if not user_message:

            return jsonify({

                "error": "Empty message"

            }), 400


        # ---------------------------------------------------
        # Session History
        # ---------------------------------------------------

        history = session.get(
            "history",
            []
        )

        history.append({

            "role": "user",
            "content": user_message

        })

        if len(history) > MAX_HISTORY:

            history = history[-MAX_HISTORY:]


        # ---------------------------------------------------
        # Sentiment Analysis
        # ---------------------------------------------------

        sentiment = analyze_sentiment(
            user_message
        )


        # ---------------------------------------------------
        # AI Response
        # ---------------------------------------------------

        reply = generate_response(
            user_message
        )


        # ---------------------------------------------------
        # Save Assistant Reply
        # ---------------------------------------------------

        history.append({

            "role": "assistant",
            "content": reply

        })

        session["history"] = history


        # ---------------------------------------------------
        # Save Chat To Database
        # ---------------------------------------------------

        chat_log = ChatHistory(

            user_id=current_user.id,

            user_message=user_message,

            ai_response=reply,

            sentiment=sentiment

        )

        db.session.add(
            chat_log
        )

        db.session.commit()


        return jsonify({

            "reply": reply,

            "sentiment": sentiment

        })


    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# ---------------------------------------------------
# Clear Chat History
# ---------------------------------------------------

@chat_bp.route(
    "/clear",
    methods=["POST"]
)
@login_required
def clear_history():

    session["history"] = []

    return jsonify({

        "status": "cleared"

    })