from __future__ import annotations
import datetime as dt
from fastapi import HTTPException
from app.core.base import BaseService
from app.core.services import exposed_action
from app.core.serializer import serialize
from ..models.lending import Asset, AssetLoan

class AssetLoanService(BaseService):
    from ..models.lending import AssetLoan

    @exposed_action("write")
    def checkout(self, asset_id: int, borrower_user_id: int, due_at: str, note: str | None = None) -> dict:
        #validar recurso
        asset = self.repo.session.get(Asset, int(asset_id))
        if not asset or asset.status != "available":
            raise HTTPException(400, "El recurso no está disponible para préstamo")

        #crear registro 
        loan_data = {
            "asset_id": asset_id,
            "borrower_user_id": borrower_user_id,
            "checkout_at": dt.datetime.now(dt.timezone.utc),
            "due_at": dt.datetime.fromisoformat(due_at) if isinstance(due_at, str) else due_at,
            "status": "open",
            "notes": note
        }
        loan = self.create(loan_data)

        #marcar como prestado
        asset.status = "loaned"
        self.repo.session.add(asset)
        self.repo.session.commit()
        
        return loan

    @exposed_action("write")
    def return_asset(self, id: int, note: str | None = None) -> dict:
        # 1. Validar el préstamo (el 'id' es el del registro AssetLoan)
        loan = self.repo.session.get(AssetLoan, int(id))
        if not loan or loan.status != "open":
            raise HTTPException(400, "El préstamo no existe o ya ha sido cerrado")

        #actualizar préstamo
        loan.returned_at = dt.datetime.now(dt.timezone.utc)
        loan.status = "returned"
        if note:
            loan.notes = f"{loan.notes or ''}\n[Devolución]: {note}".strip()

        #liberar recurso 
        asset = self.repo.session.get(Asset, loan.asset_id)
        if asset:
            asset.status = "available"
            self.repo.session.add(asset)

        self.repo.session.add(loan)
        self.repo.session.commit()
        self.repo.session.refresh(loan)
        
        return serialize(loan)