from models.db_manager import DBManager
import models.permisos as mp  # Importamos el módulo con un alias corto

class Rol:
    def __init__(self, nombre_rol, id_rol=None, descripcion_rol=None):
        self.id_rol = id_rol
        self.nombre_rol = nombre_rol
        self.descripcion_rol = descripcion_rol
        self.db = DBManager()

    @classmethod
    def obtener_permisos(cls, id_rol):
        db = DBManager()
        query = """
            SELECT p.id_permiso, p.nombre_permiso, p.slug
            FROM Permisos p
            INNER JOIN Rol_Permisos rp ON p.id_permiso = rp.id_permiso
            WHERE rp.id_rol = ?
        """
        res = db.consultar(query, (id_rol,))
        return [
            mp.Permisos(
                id_permiso=f['id_permiso'], 
                nombre_permiso=f['nombre_permiso'], 
                slug=f['slug']
            ) for f in res
        ]

    def crear(self):
        query = """
            INSERT INTO Rol (nombre_rol, descripcion_rol)
            VALUES (?, ?)
        """
        params = (self.nombre_rol, self.descripcion_rol)
        nuevo_id = self.db.ejecutar_consulta(query, params)
        if nuevo_id:
            self.id_rol = nuevo_id
            return True
        return False

    @classmethod
    def obtener_por_id(cls, id_rol):
        db = DBManager()
        query = """
            SELECT * FROM Rol WHERE id_rol = ?
        """
        res = db.consultar(query, (id_rol,))

        if not res:
            return None

        return cls(
            nombre_rol=res[0]['nombre_rol'],
            descripcion_rol=res[0]['descripcion_rol'],
            id_rol=res[0]['id_rol']
        )