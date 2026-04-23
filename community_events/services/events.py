from __future__ import annotations
from fastapi import HTTPException
from app.core.base import BaseService
from app.core.services import exposed_action
from ..models.events import Event

class EventService(BaseService):
    
    @exposed_action("write", groups=["core_group_authenticated"])
    def register(self, event_id: int) -> dict:
        """Acción para que un usuario se apunte a un evento."""
        event = self.repo.session.get(Event, int(event_id))
        if not event:
            raise HTTPException(404, "Evento no encontrado")
        
        if not event.is_published:
            raise HTTPException(400, "El evento no acepta inscripciones aún")

        
        return {"status": "success", "message": f"Te has inscrito correctamente en {event.name}"}

    @exposed_action("write", groups=["community_group_staff", "core_group_superadmin"])
    def toggle_publish(self, id: int):
        """Acción para que el staff publique o retire un evento."""
        event = self.repo.session.get(Event, int(id))
        if not event:
            raise HTTPException(404, "Evento no encontrado")
        event.is_published = not event.is_published
        self.repo.session.commit()
        return {"id": event.id, "is_published": event.is_published}