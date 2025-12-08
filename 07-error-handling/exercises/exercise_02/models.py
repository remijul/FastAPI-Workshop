"""Exercice 2 - Modèles"""

from pydantic import BaseModel, Field


class RoomCreate(BaseModel):
    """Modèle pour créer une chambre."""
    name: str = Field(..., min_length=1)
    capacity: int = Field(..., ge=1)
    price_per_night: float = Field(..., gt=0)


class ReservationCreate(BaseModel):
    """Modèle pour créer une réservation."""
    room_id: int
    guest_name: str = Field(..., min_length=2)
    nights: int = Field(..., ge=1)


class RoomResponse(BaseModel):
    """Modèle de réponse pour une chambre."""
    id: int
    name: str
    capacity: int
    price_per_night: float
    available: bool


class ReservationResponse(BaseModel):
    """Modèle de réponse pour une réservation."""
    id: int
    room_id: int
    guest_name: str
    nights: int
    total_price: float