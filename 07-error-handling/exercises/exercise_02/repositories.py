"""Exercice 2 - Repositories"""

from .database import get_db_connection


class RoomRepository:
    """Repository pour les chambres."""
    
    @staticmethod
    def create(name: str, capacity: int, price_per_night: float) -> int:
        """Crée une chambre."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO rooms (name, capacity, price_per_night) VALUES (?, ?, ?)",
            (name, capacity, price_per_night)
        )
        room_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return room_id
    
    @staticmethod
    def get_by_id(room_id: int) -> dict | None:
        """Récupère une chambre par ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        return dict(row) if row else None
    
    @staticmethod
    def mark_unavailable(room_id: int) -> bool:
        """Marque une chambre comme indisponible."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE rooms SET available = 0 WHERE id = ?",
            (room_id,)
        )
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success


class ReservationRepository:
    """Repository pour les réservations."""
    
    @staticmethod
    def create(room_id: int, guest_name: str, nights: int, total_price: float) -> int:
        """Crée une réservation."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO reservations (room_id, guest_name, nights, total_price) VALUES (?, ?, ?, ?)",
            (room_id, guest_name, nights, total_price)
        )
        reservation_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return reservation_id