from sqlalchemy import String, Text, Boolean, DateTime
from app.core.base import Base
from app.core.fields import field

class Suggestion(Base):
    __tablename__ = "feedback_suggestion"
    __abstract__ = False
    __model__ = "suggestion"
    __service__ = "modules.feedback_moderation.services.moderation.SuggestionService"

    title = field(String(200), required=True, public=True, editable=True)
    content = field(Text, required=True, public=True, editable=True)
    status = field(
        String(20), 
        default="pending", 
        public=True,
        info={"choices": [
            {"label": "Pendiente", "value": "pending"},
            {"label": "Publicada", "value": "published"},
            {"label": "Rechazada", "value": "rejected"}
        ]}
    )
    is_public = field(Boolean, default=False, public=True, editable=True)