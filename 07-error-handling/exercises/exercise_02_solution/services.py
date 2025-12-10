"""
Solution Exercice 2 - Services
"""

from .repositories import RoomRepository, ReservationRepository
from .models import RoomCreate, ReservationCreate, RoomResponse, ReservationResponse
from .exceptions import RoomNotFoundError, RoomNotAvailableError, InvalidDateError


class RoomService:
    """Service pour les chambres."""
    
    # Solution TODO 2: Implémenter les méthodes
    
    @staticmethod
    def create_room(room_data: RoomCreate) -> RoomResponse:
        """Crée une chambre."""
        room_id = RoomRepository.create(
            name=room_data.name,
            capacity=room_data.capacity,
            price_per_night=room_data.price_per_night
        )
        
        return RoomResponse(
            id=room_id,
            name=room_data.name,
            capacity=room_data.capacity,
            price_per_night=room_data.price_per_night,
            available=True
        )
    
    @staticmethod
    def get_room(room_id: int) -> RoomResponse:
        """Récupère une chambre (lever RoomNotFoundError si non trouvé)."""
        room = RoomRepository.get_by_id(room_id)
        
        if not room:
            raise RoomNotFoundError(room_id)
        
        return RoomResponse(
            id=room["id"],
            name=room["name"],
            capacity=room["capacity"],
            price_per_night=room["price_per_night"],
            available=bool(room["available"])
        )


class ReservationService:
    """Service pour les réservations."""
    
    @staticmethod
    def create_reservation(reservation_data: ReservationCreate) -> ReservationResponse:
        """
        Crée une réservation.
        
        Vérifications :
        - nights > 0 (InvalidDateError)
        - Chambre existe (RoomNotFoundError)
        - Chambre disponible (RoomNotAvailableError)
        """
        # Vérifier le nombre de nuits
        if reservation_data.nights <= 0:
            raise InvalidDateError("Le nombre de nuits doit être supérieur à 0")
        
        # Récupérer la chambre
        room = RoomRepository.get_by_id(reservation_data.room_id)
        
        if not room:
            raise RoomNotFoundError(reservation_data.room_id)
        
        # Vérifier la disponibilité
        if not room["available"]:
            raise RoomNotAvailableError(room["id"], room["name"])
        
        # Calculer le prix total
        total_price = room["price_per_night"] * reservation_data.nights
        
        # Créer la réservation
        reservation_id = ReservationRepository.create(
            room_id=reservation_data.room_id,
            guest_name=reservation_data.guest_name,
            nights=reservation_data.nights,
            total_price=total_price
        )
        
        # Marquer la chambre comme indisponible
        RoomRepository.mark_unavailable(reservation_data.room_id)
        
        return ReservationResponse(
            id=reservation_id,
            room_id=reservation_data.room_id,
            guest_name=reservation_data.guest_name,
            nights=reservation_data.nights,
            total_price=total_price
        )