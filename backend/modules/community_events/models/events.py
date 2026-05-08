from __future__ import annotations
from sqlalchemy import Boolean, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.base import Base
from app.core.fields import field
import datetime

class Event(Base):
    __tablename__ = "community_event"
    __abstract__ = False
    __model__ = "community_event"
    __service__ = "modules.community_events.services.events.EventService"

    name = field(
        String(200), 
        required=True, 
        public=True, 
        editable=True,
        info={"label": "Nombre del Evento"}
    )
    description = field(
        Text, 
        public=True, 
        editable=True,
        info={"label": "Descripción"}
    )
    start_at = field(
        DateTime(timezone=True), 
        required=True, 
        public=True, 
        editable=True,
        info={"label": "Fecha Inicio"}
    )
    capacity = field(
        Integer, 
        default=0, 
        public=True, 
        editable=True,
        info={"label": "Capacidad máxima"}
    )
    current_participants = field(
        Integer,
        default=0,
        public=True,
        editable=False,
        info={"label": "Inscritos actuales"}
    )
    is_published = field(
        Boolean, 
        default=False, 
        public=True, 
        editable=True,
        info={"label": "Publicado"}
    )

class Registration(Base):
    __tablename__ = "community_events_registration"
    __model__ = "registration"
    __service__ = "modules.community_events.services.registration.RegistrationService"

    event_id = field(
        Integer, 
        ForeignKey("community_event.id", ondelete="CASCADE"), 
        required=True,
        info={"label": "Evento"}
    )
    
    attendee_name = field(
        String(180), 
        required=True, 
        public=True, 
        info={"label": "Nombre del Asistente"}
    )
    attendee_email = field(
        String(180), 
        required=True, 
        public=True, 
        info={"label": "Email"}
    )
    
    status = field(
        String(20),
        default="pending",
        required=True,
        info={
            "label": "Estado",
            "choices": [
                {"label": "Pendiente", "value": "pending"},
                {"label": "Confirmado", "value": "confirmed"},
                {"label": "En espera", "value": "waitlist"},
                {"label": "Check-in", "value": "checked_in"},
                {"label": "Cancelado", "value": "cancelled"}
            ]
        }
    )

    registered_at = field(
        DateTime(timezone=True), 
        default=datetime.datetime.utcnow, 
        info={"label": "Fecha Registro"}
    )
    checkin_at = field(
        DateTime(timezone=True), 
        required=False, 
        info={"label": "Fecha Check-in"}
    )
    notes = field(Text, required=False, info={"label": "Notas"})

    # Relación para navegación
    event = relationship("Event", backref="registrations")