import datetime as dt
from app.core.base import BaseService
from app.core.decorators import exposed_action
from app.core.exceptions import ValidationError
from ..models.events import Registration 

class RegistrationService(BaseService):
    
    @exposed_action("write", groups=["community_events_group_staff"])
    def bulk_checkin(self, ids: list[int]):
        """
        Acción masiva para registrar la entrada de varios asistentes a la vez.
        """
        session = self.app.repo.session
        #inscripciones seleccionadas
        registrations = session.query(Registration).filter(Registration.id.in_(ids)).all()
        
        count = 0
        for reg in registrations:
            if reg.status == "confirmed":
                reg.status = "checked_in"
                reg.checkin_at = dt.datetime.now(dt.timezone.utc)
                count += 1
        
        session.commit()
        return {
            "status": "success",
            "message": f"Check-in completado para {count} personas."
        }

    @exposed_action("write", groups=["community_events_group_staff"])
    def confirm(self, id: int):
        """Confirma una inscripción pendiente."""
        session = self.app.repo.session
        reg = session.get(Registration, id)
        if reg:
            reg.status = "confirmed"
            session.commit()
            return {"status": "success", "message": "Inscripción confirmada."}