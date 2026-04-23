from __future__ import annotations
from fastapi import HTTPException
from app.core.base import BaseService
from app.core.services import exposed_action
from ..models.moderation import Suggestion

class SuggestionService(BaseService):
    
    @exposed_action("write", groups=["feedback_group_moderator", "core_group_superadmin"])
    def publish(self, id: int) -> dict:
        """Marca una sugerencia como publicada y la hace pública."""
        suggestion = self.repo.session.get(Suggestion, int(id))
        if not suggestion:
            raise HTTPException(404, "Sugerencia no encontrada")
        
        suggestion.status = "published"
        suggestion.is_public = True
        
        self.repo.session.add(suggestion)
        self.repo.session.commit()
        #objeto actualizado
        return {"id": suggestion.id, "status": suggestion.status, "is_public": suggestion.is_public}

    @exposed_action("write", groups=["feedback_group_moderator", "core_group_superadmin"])
    def reject(self, id: int, reason: str | None = None) -> dict:
        """Rechaza una sugerencia."""
        suggestion = self.repo.session.get(Suggestion, int(id))
        if not suggestion:
            raise HTTPException(404, "Sugerencia no encontrada")
            
        suggestion.status = "rejected"
        suggestion.is_public = False
        
        self.repo.session.add(suggestion)
        self.repo.session.commit()
        return {"id": suggestion.id, "status": suggestion.status}