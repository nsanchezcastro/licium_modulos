from sqlalchemy import String, Text, Boolean, DateTime, Integer
from app.core.base import Base
from app.core.fields import field

class Event(Base):
    __tablename__ = "community_event"
    __abstract__ = False
    __model__ = "community_event"
    __service__ = "modules.community_events.services.events.EventService"

    name = field(String(200), required=True, public=True, editable=True)
    description = field(Text, public=True, editable=True)
    start_at = field(DateTime, required=True, public=True, editable=True)
    capacity = field(Integer, default=0, public=True, editable=True)
    is_published = field(Boolean, default=False, public=True, editable=True)