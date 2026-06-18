import sqlite3
import os
from contextlib import contextmanager

class DBManager:
    def __init__(self):
        # Definimos la ruta de la base de datos y del esquema
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.db_path = os.path.join(base_dir, 'database', 'control_gastos.db')

    @contextmanager
    def _get_connection(self):
        """Gestor de contexto para manejar la conexión de forma segura."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;") # Activar llaves foráneas
        conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
        try:
            yield conn
        finally:
            conn.close()

    def ejecutar_consulta(self, consulta, parametros=()):
        """Para INSERT, UPDATE, DELETE usando 'with'."""
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(consulta, parametros)
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                print(f"Error de base de datos: {e}")
                return None

    def consultar(self, consulta, parametros=()):
        """Para SELECT usando 'with'."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row  # convertir tuplas en objeto diccionario
            try:
                cursor = conn.cursor()
                cursor.execute(consulta, parametros)
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Error en consulta: {e}")
                return []