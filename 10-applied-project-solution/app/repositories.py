"""
Repository pour l'accès aux données (couche SQL).
SOLUTION COMPLÈTE
"""

from app.database import get_db_connection
from typing import Optional


class CharacterRepository:
    """Repository pour l'accès aux données des personnages."""
    
    @staticmethod
    def create(name: str, character_class: str, level: int, health_points: int,
               attack: int, defense: int, speed: int, 
               special_ability: Optional[str] = None,
               image_url: Optional[str] = None) -> int:
        """Crée un nouveau personnage."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO characters (name, class, level, health_points, attack, defense, speed, special_ability, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, character_class, level, health_points, attack, defense, speed, special_ability, image_url))
        
        character_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return character_id
    
    @staticmethod
    def get_by_id(character_id: int) -> dict | None:
        """Récupère un personnage par ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM characters WHERE id = ?", (character_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        return dict(row) if row else None
    
    @staticmethod
    def get_all() -> list[dict]:
        """Récupère tous les personnages."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM characters ORDER BY id")
        rows = cursor.fetchall()
        
        conn.close()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def update(character_id: int, **updates) -> bool:
        """Met à jour un personnage."""
        if not updates:
            return False
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Construire la requête dynamiquement
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [character_id]
        
        cursor.execute(f"""
            UPDATE characters 
            SET {set_clause}
            WHERE id = ?
        """, values)
        
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    @staticmethod
    def delete(character_id: int) -> bool:
        """Supprime un personnage."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM characters WHERE id = ?", (character_id,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    # ==================== NIVEAU 2 ====================
    
    @staticmethod
    def get_by_filters(character_class: Optional[str] = None,
                       min_level: Optional[int] = None,
                       max_level: Optional[int] = None) -> list[dict]:
        """Récupère les personnages avec filtres."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM characters WHERE 1=1"
        params = []
        
        if character_class:
            query += " AND class = ?"
            params.append(character_class)
        
        if min_level is not None:
            query += " AND level >= ?"
            params.append(min_level)
        
        if max_level is not None:
            query += " AND level <= ?"
            params.append(max_level)
        
        query += " ORDER BY id"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        conn.close()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_stats() -> dict:
        """Calcule les statistiques globales."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Nombre total
        cursor.execute("SELECT COUNT(*) as total FROM characters")
        total = cursor.fetchone()["total"]
        
        # Nombre par classe
        cursor.execute("""
            SELECT class, COUNT(*) as count 
            FROM characters 
            GROUP BY class
        """)
        by_class = {row["class"]: row["count"] for row in cursor.fetchall()}
        
        # Niveau moyen, min, max
        cursor.execute("""
            SELECT 
                AVG(level) as avg_level,
                MIN(level) as min_level,
                MAX(level) as max_level
            FROM characters
        """)
        level_stats = cursor.fetchone()
        
        # Attaque moyenne par classe
        cursor.execute("""
            SELECT class, AVG(attack) as avg_attack
            FROM characters
            GROUP BY class
        """)
        avg_attack_by_class = {row["class"]: round(row["avg_attack"], 2) for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            "total_characters": total,
            "characters_by_class": by_class,
            "average_level": round(level_stats["avg_level"], 2),
            "min_level": level_stats["min_level"],
            "max_level": level_stats["max_level"],
            "average_attack_by_class": avg_attack_by_class
        }


# ==================== NIVEAU 3 - OPTION AUTH ====================

class UserRepository:
    """Repository pour les utilisateurs."""
    
    @staticmethod
    def create(username: str, hashed_password: str) -> int:
        """Crée un utilisateur."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            (username, hashed_password)
        )
        user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return user_id
    
    @staticmethod
    def get_by_username(username: str) -> dict | None:
        """Récupère un utilisateur par username."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        conn.close()
        
        return dict(row) if row else None