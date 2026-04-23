from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.base import Base
from app.core.fields import field

class AssetLocation(Base):
    __tablename__ = "asset_lending_location"
    __model__ = "asset_lending.location"
    
    name = field(String(100), required=True, public=True, info={"label": "Nombre"})
    code = field(String(20), required=True, public=True, info={"label": "Código"})
    is_active = field(Boolean, default=True, public=True, info={"label": "Activo"})

class Asset(Base):
    __tablename__ = "asset_lending_asset"
    __model__ = "asset_lending.asset"
    
    name = field(String(100), required=True, public=True, info={"label": "Recurso"})
    asset_code = field(String(50), required=True, public=True, info={"label": "Código Inventario"})
    status = field(String(20), default="available", public=True, info={
        "label": "Estado",
        "choices": [
            {"label": "Disponible", "value": "available"},
            {"label": "Prestado", "value": "loaned"},
            {"label": "Mantenimiento", "value": "maintenance"}
        ]
    })
    location_id = field(ForeignKey("asset_lending_location.id"), public=True)
    notes = field(Text, public=True)

class AssetLoan(Base):
    __tablename__ = "asset_lending_loan"
    __model__ = "asset_lending.loan"
    __service__ = "modules.asset_lending.services.lending.AssetLoanService"
    
    asset_id = field(ForeignKey("asset_lending_asset.id"), required=True, public=True)
    borrower_user_id = field(ForeignKey("core_user.id"), required=True, public=True)
    checkout_at = field(DateTime, public=True, info={"label": "Fecha Salida"})
    due_at = field(DateTime, public=True, info={"label": "Fecha Devolución Prevista"})
    returned_at = field(DateTime, public=True, info={"label": "Fecha Real Devolución"})
    status = field(String(20), default="open", public=True, info={
        "choices": [
            {"label": "Abierto", "value": "open"},
            {"label": "Devuelto", "value": "returned"},
            {"label": "Retrasado", "value": "overdue"}
        ]
    })