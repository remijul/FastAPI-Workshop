"""Exercice 2 - Routes"""

from fastapi import APIRouter
from .models import RoomCreate, ReservationCreate, RoomResponse, ReservationResponse
from .services import RoomService, ReservationService

router = APIRouter(tags=["hotel"])


@router.post("/rooms", response_model=RoomResponse, status_code=201)
def create_room(room: RoomCreate):
    """Crée une chambre."""
    return RoomService.create_room(room)


@router.get("/rooms/{room_id}", response_model=RoomResponse)
def get_room(room_id: int):
    """Récupère une chambre."""
    return RoomService.get_room(room_id)


@router.post("/reservations", response_model=ReservationResponse, status_code=201)
def create_reservation(reservation: ReservationCreate):
    """Crée une réservation."""
    return ReservationService.create_reservation(reservation)