"""
Solution Exercice 2 - Exceptions personnalisées
"""


# Solution TODO 1: Créer les exceptions

class RoomNotFoundError(Exception):
    """Exception levée quand une chambre n'existe pas."""
    def __init__(self, room_id: int):
        self.room_id = room_id
        self.message = f"Chambre {room_id} non trouvée"
        super().__init__(self.message)


class RoomNotAvailableError(Exception):
    """Exception levée quand une chambre n'est pas disponible."""
    def __init__(self, room_id: int, room_name: str):
        self.room_id = room_id
        self.room_name = room_name
        self.message = f"La chambre '{room_name}' (ID: {room_id}) n'est pas disponible"
        super().__init__(self.message)


class InvalidDateError(Exception):
    """Exception levée quand les dates sont invalides."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)