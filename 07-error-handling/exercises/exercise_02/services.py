"""
Exercice 2 - Services

TODO 2: Implémenter les services avec gestion d'erreurs
- create_room : Créer une chambre
- get_room : Récupérer une chambre (lever RoomNotFoundError)
- create_reservation : Créer une réservation
  * Vérifier que nights > 0 (lever InvalidDateError si non)
  * Vérifier que la chambre existe (lever RoomNotFoundError)
  * Vérifier que la chambre est disponible (lever RoomNotAvailableError)
  * Calculer total_price = price_per_night * nights
  * Marquer la chambre comme indisponible
"""

from .repositories import RoomRepository, ReservationRepository
from .models import RoomCreate, ReservationCreate, RoomResponse, ReservationResponse
from .exceptions import RoomNotFoundError, RoomNotAvailableError, InvalidDateError


class RoomService:
    """Service pour les chambres."""
    
    # TODO 2: Implémenter les méthodes
    
    @staticmethod
    def create_room(room_data: RoomCreate) -> RoomResponse:
        """Crée une chambre."""
        pass
    
    @staticmethod
    def get_room(room_id: int) -> RoomResponse:
        """Récupère une chambre (lever RoomNotFoundError si non trouvé)."""
        pass


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
        pass